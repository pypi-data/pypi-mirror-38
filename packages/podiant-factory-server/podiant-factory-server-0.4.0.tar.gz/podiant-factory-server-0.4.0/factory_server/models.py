from api.helpers import generate_api_key
from datetime import timedelta
from django.db import models
from django.utils import timezone
from hashlib import md5, sha512
from importlib import import_module
from logging import getLogger
from . import bundling, exceptions, query, settings
from .links import ResourceLinkJSONEncoder
from .signals import operation_request, operation_status, process_status
import django_rq
import json
import pickle
import requests


class Machine(models.Model):
    name = models.SlugField(max_length=50, unique=True, db_index=True)
    creator = models.ForeignKey(
        'auth.User',
        related_name='factory_machines',
        on_delete=models.CASCADE
    )

    key = models.CharField(max_length=64, db_index=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = generate_api_key(64)

        super().save(*args, **kwargs)

    def enqueue(self, func, args=(), kwargs={}):
        queue = django_rq.get_queue('factory')
        return queue.enqueue(func, args=args, kwargs=kwargs)

    def enabled_for_process(self, process):
        meta = json.loads(process.meta or '{}')

        for matcher in settings.MACHINE_PROCESS_MATCHERS:
            module, func = matcher.rsplit('.', 1)
            module = import_module(module)
            func = getattr(module, func)

            if func(self, meta.get('data', {}), *meta.get('tags', [])):
                return True

        return False

    def schedule_operation(self, operation):
        for operator in self.operators.filter(
            namespace=operation.namespace,
            function=operation.function
        ).distinct():
            return operator.schedule_operation(operation)

        q = models.Q(
            function__isnull=True
        ) | models.Q(
            function=''
        )

        for operator in self.operators.filter(
            namespace=operation.namespace
        ).filter(q).distinct():
            return operator.schedule_operation(operation)

    def retry_operation(self, operation):
        exclude_operators = operation.results.values_list(
            'operator_id',
            flat=True
        )

        for operator in self.operators.filter(
            namespace=operation.namespace,
            function=operation.function
        ).exclude(
            pk__in=exclude_operators
        ).distinct():
            return operator.schedule_operation(operation)

        q = models.Q(
            function__isnull=True
        ) | models.Q(
            function=''
        )

        for operator in self.operators.filter(
            namespace=operation.namespace
        ).exclude(
            pk__in=exclude_operators
        ).filter(q).distinct():
            return operator.schedule_operation(operation)


class Operator(models.Model):
    machine = models.ForeignKey(
        Machine,
        related_name='operators',
        on_delete=models.CASCADE
    )

    namespace = models.SlugField(max_length=50, db_index=True)
    function = models.SlugField(
        max_length=50,
        db_index=True,
        null=True,
        blank=True
    )

    url = models.URLField('URL', max_length=255)

    def __str__(self):
        return '%s.%s' % (self.namespace, self.function or '*')

    def post(self, data, verb):
        digest = md5(
            pickle.dumps(data)
        ).hexdigest()

        signed_digest = sha512(
            (digest + self.machine.key).encode('utf-8')
        ).hexdigest()

        meta = data.get('meta', {})
        meta.update(
            {
                'requested': timezone.now().isoformat(),
                'verb': verb,
                'digest': digest,
                'signed-digest': signed_digest
            }
        )

        data['meta'] = meta

        try:
            response = requests.post(
                self.url,
                data=json.dumps(
                    data,
                    cls=ResourceLinkJSONEncoder
                ),
                headers={
                    'Content-Type': 'application/vnd.api+json',
                    'Accepts': 'application/vnd.api+json'
                }
            )

            response.raise_for_status()
        except Exception as ex:
            raise exceptions.OperationResponseError(
                str(ex)
            )

        try:
            return response.json()
        except Exception as ex:
            raise exceptions.OperationResponseError(
                str(ex)
            )

    def schedule_operation(self, operation):
        if operation.scheduling == 'auto':
            operation.status = 'scheduling'
            operation_status.send(
                type(self),
                operation=operation,
                status='scheduling'
            )

            operation.save()

            operation.process.info(
                'Status of operation "%s" changed to "scheduling".' % operation
            )

            self.machine.enqueue(
                self.perform,
                args=[operation]
            )

            return True

        OperationRequest.objects.create(
            operator=self,
            operation=operation
        )

        return True

    def perform(self, operation):
        data = self.post(
            operation.to_json(),
            'start'
        )

        if not isinstance(data, dict):
            raise exceptions.OperationResponseError(
                'Machine did not provide a JSON object.'
            )

        if 'data' not in data:
            raise exceptions.OperationResponseError(
                'Machine did not provide a data object.'
            )

        data = data['data']
        attrs = {}

        if 'attributes' in data:
            if isinstance(data['attributes'], dict):
                attrs = data['attributes']
            else:
                raise exceptions.OperationResponseError(
                    'Expected attributes to be an object.'
                )
        else:
            raise exceptions.OperationResponseError(
                'Expected an attributes object.'
            )

        if data.get('type') != 'operations':
            raise exceptions.OperationResponseError(
                (
                    'Machine replied with incorrect object type '
                    '(%s).'
                ) % (
                    data.get('type') and (
                        '"%(type)s"' % data
                    ) or (
                        'null'
                    )
                )
            )

        if data.get('id') != str(operation.pk):
            raise exceptions.OperationResponseError(
                (
                    'Machine replied with incorrect operation ID '
                    '(%s).'
                ) % (
                    data.get('id') and (
                        '"%(id)s"' % data
                    ) or (
                        'null'
                    )
                )
            )

        status = attrs.get('status')
        result = attrs.get('result', {})

        if not isinstance(result, dict):
            raise exceptions.OperationResponseError(
                'Expected result to be an object.'
            )

        tags = result.pop('tags', [])
        if not isinstance(tags, list):
            raise exceptions.OperationResponseError(
                'Expected tags to be an array.'
            )

        if status in settings.OPERATION_STATUSES:
            if status not in ('pending', 'scheduling'):
                operation.set_status(
                    status,
                    self,
                    result,
                    tags
                )

                return True

        raise exceptions.OperationResponseError(
            (
                'Machine replied with incorrect status '
                '("%s").'
            ) % status
        )

    class Meta:
        unique_together = ('function', 'namespace', 'machine')


class Bundle(models.Model):
    objects = query.BundleQuerySet.as_manager()

    def create_item(self, key, parent_bundle, kind, mime_type=None):
        obj = Item(
            bundle=self,
            key=key,
            kind=kind,
            mime_type=mime_type
        )

        if parent_bundle is not None:
            try:
                obj.parent = parent_bundle.items.get(key=key)
            except Item.DoesNotExist:
                pass

        obj.full_clean()
        obj.save()

        return obj

    def update_items(self, **kwargs):
        for name, value in kwargs.items():
            try:
                obj = self.items.get(key=name)
            except Item.DoesNotExist:
                continue

            if not value:
                raise exceptions.BundleConfigurationError(
                    name,
                    'Missing value definition.'
                )

            obj.set_value(value)
            obj.full_clean()
            obj.save()


class Item(models.Model):
    bundle = models.ForeignKey(
        Bundle,
        related_name='items',
        on_delete=models.CASCADE
    )

    key = models.SlugField(max_length=255, db_index=True)
    value = models.TextField(null=True, blank=True)
    kind = models.CharField(
        max_length=7,
        choices=[(k, k) for k in settings.BUNDLE_ITEM_KINDS]
    )

    mime_type = models.CharField(max_length=30, null=True, blank=True)
    parent = models.ForeignKey(
        'self',
        related_name='children',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def as_dict(self):
        d = {
            'type': self.kind
        }

        if self.kind == 'media':
            d['mime-type'] = self.mime_type

        if self.value:
            d['value'] = json.loads(self.value)

        return d

    def set_value(self, value):
        bundler_cls_name = '%sBundler' % self.kind.capitalize()
        bundler_cls = getattr(bundling, bundler_cls_name)
        meta = {}

        if self.kind == 'media':
            meta['mime_type'] = self.mime_type
            if self.parent:
                meta['mime_type'] = self.parent.mime_type

        bundler = bundler_cls(value, **meta)
        bundler.check()

        if self.kind == 'media' and self.parent is not None:
            self.mime_type = bundler.meta['mime_type']

        self.value = bundler.pack()

    class Meta:
        unique_together = ('key', 'bundle')


class Process(models.Model):
    input_bundle = models.ForeignKey(
        Bundle,
        on_delete=models.CASCADE,
        related_name='input_processes'
    )

    output_bundle = models.ForeignKey(
        Bundle,
        on_delete=models.CASCADE,
        related_name='output_processes'
    )

    status = models.CharField(
        max_length=10,
        choices=[
            (s, s)
            for s in settings.OPERATION_SCHEDULES
        ],
        default='pending'
    )

    progress = models.PositiveIntegerField(default=0)
    meta = models.TextField()

    objects = query.ProcessQuerySet.as_manager()

    def _log(self, kind, text, **extra):
        logger = getLogger('factory_server')
        method = getattr(logger, 'info' if kind == 'success' else kind)
        method(text, extra=extra)

        return self.log.create(
            kind=kind,
            text=text,
            extra=json.dumps(extra)
        )

    def debug(self, text, **extra):
        return self._log('debug', text, **extra)

    def info(self, text, **extra):
        return self._log('info', text, **extra)

    def warning(self, text, **extra):
        return self._log('warning', text, **extra)

    def warn(self, text, **extra):
        return self.warning(text, **extra)

    def success(self, text, **extra):
        return self._log('success', text, **extra)

    def error(self, text, **extra):
        return self._log('error', text, **extra)

    def start(self, **input_bundle_data):
        for key, value in input_bundle_data.items():
            try:
                bundle_item = self.input_bundle.items.get(key=key)
            except Item.DoesNotExist:
                raise TypeError(
                    (
                        '\'start() got an unexpected keyword argument '
                        '\'%s\''
                    ) % key
                )

            bundle_item.set_value(value)
            bundle_item.save()

        self.info('Starting process.')
        self.set_status('running')

        for operation in self.operations.all()[:1]:
            return operation.schedule()

    def next(self):
        for operation in self.operations.filter(
            status='pending'
        ):
            if operation.schedule():
                return True

        statuses = sorted(
            set(
                self.operations.values_list('status', flat=True).distinct()
            )
        )

        self.set_status('successful')
        message = 'Process complete'
        if 'failed' in statuses:
            message += ', with one or more warnings'

        self.info('%s.' % message)

    def set_status(self, status=None, progress=None):
        if status is not None:
            methods = {
                'pending': 'info',
                'running': 'info',
                'failed': 'error',
                'successful': 'success'
            }

            if self.status in methods:
                del methods[self.status]

            try:
                logger = methods[status]
            except KeyError:
                raise TypeError(
                    (
                        '"%s" is not a valid process status '
                        '(status is already %s).'
                    ) % (
                        status,
                        self.status
                    )
                )

            self.status = status

        if progress is not None:
            self.progress = int(round(progress, 0))
        else:
            finished = float(
                self.operations.filter(
                    status='successful'
                ).count()
            )

            remaining = float(
                self.operations.exclude(
                    status__in=('cancelled', 'successful')
                ).count()
            )

            total = float(finished + remaining)
            if total:
                self.progress = int(
                    round(finished / total * 100.0, 0)
                )

        self.save()

        if status is not None and status != 'successful':
            logger = getattr(self, logger)
            logger(
                'Status changed to "%s".' % status
            )

        if status is not None or progress is not None:
            process_status.send(
                type(self),
                process=self,
                status=self.status,
                progress=self.progress
            )

    def cancel(self):
        for operation in self.operations.filter(
            status='pending'
        ):
            operation.cancel()

    class Meta:
        verbose_name_plural = 'processes'


class ProcessTag(models.Model):
    process = models.ForeignKey(
        Process,
        related_name='tags',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'process')


class Operation(models.Model):
    process = models.ForeignKey(
        Process,
        related_name='operations',
        on_delete=models.CASCADE
    )

    ordering = models.PositiveIntegerField(default=0)
    namespace = models.SlugField(max_length=50, db_index=True)
    function = models.SlugField(max_length=50, db_index=True)
    verbose_name = models.CharField(max_length=101)
    scheduling = models.CharField(
        max_length=7,
        choices=[
            (s, s)
            for s in settings.OPERATION_SCHEDULES
        ],
        default='auto'
    )

    can_fail = models.BooleanField(default=False)
    status = models.CharField(
        max_length=10,
        choices=[
            (s, s) for s in settings.OPERATION_STATUSES
        ],
        default='pending'
    )

    progress = models.FloatField(null=True, default=None, blank=True)
    expires = models.DateTimeField(null=True, blank=True)

    objects = query.OperationQuerySet.as_manager()

    def __str__(self):
        return '%s.%s' % (self.namespace, self.function)

    def schedule(self):
        if self.restrictions.filter(
            kind='tag'
        ).exists():
            if not OperationResultTag.objects.filter(
                result__operation__process=self.process,
                name__in=self.restrictions.filter(
                    kind='tag'
                ).values_list(
                    'value',
                    flat=True
                )
            ).exists():
                conditions = ', '.join(
                    [
                        'tag="%s"' % tag
                        for tag in self.restrictions.filter(
                            kind='tag'
                        ).values_list(
                            'value',
                            flat=True
                        )
                    ]
                )

                self.process.info(
                    (
                        'Operation "%s" skipped as it does not meet '
                        'conditions (%s).'
                    ) % (
                        self,
                        conditions
                    )
                )

                self.status = 'cancelled'
                operation_status.send(
                    type(self),
                    operation=self,
                    status='cancelled'
                )

                self.save()
                return False

        for machine in Machine.objects.all():
            if machine.enabled_for_process(self.process):
                if machine.schedule_operation(self):
                    return True

        raise exceptions.OperationFailedError(
            'No machines accepted the operation.'
        )

    def retry(self):
        for machine in Machine.objects.all():
            if machine.enabled_for_process(self.process):
                if machine.retry_operation(self):
                    return True

        raise exceptions.NoMoreRetriesError(
            'No other machines accepted the operation.'
        )

    def cancel(self):
        self.status = 'cancelled'
        self.expires = None
        self.process.info(
            'Status of operation "%s" changed to "cancelled".' % self
        )

        operation_status.send(
            type(self),
            operation=self,
            status='cancelled'
        )

        self.process.set_status()

    def set_status(self, status, operator, result={}, tags=[]):
        methods = {
            'pending': 'debug',
            'scheduled': 'info',
            'running': 'info',
            'failed': 'warning',
            'cancelled': 'warning',
            'successful': 'info'
        }

        if self.status in methods:
            del methods[self.status]

        try:
            logger = methods[status]
        except KeyError:
            raise TypeError(
                (
                    '"%s" is not a valid operation status '
                    '(status is already %s).'
                ) % (
                    status,
                    self.status
                )
            )

        try:
            resultobj = OperationResult.objects.get(
                operator=operator,
                operation=self
            )
        except OperationResult.DoesNotExist:
            resultobj = OperationResult(
                operator=operator,
                operation=self,
                status=status
            )

        resultobj.data = json.dumps(result)
        resultobj.save()
        resultobj.tags.all().delete()

        for tag in tags:
            resultobj.tags.create(name=tag)

        if status == 'scheduled':
            self.expires = timezone.now() + timedelta(
                seconds=settings.START_TIMEOUT
            )
        elif status == 'running':
            self.expires = timezone.now() + timedelta(
                seconds=settings.RUNNING_TIMEOUT
            )
        else:
            self.expires = None

        if status == 'failed':
            try:
                self.retry()
            except exceptions.NoMoreRetriesError:
                self.status = 'failed'
                operation_status.send(
                    type(self),
                    operation=self,
                    status='failed'
                )

                self.save()

                if not self.can_fail:
                    self.process.cancel()
                    self.process.set_status('failed')

                    logger = getattr(self.process, logger)
                    logger(
                        'Status of operation "%s" changed to "%s".' % (
                            self,
                            status
                        )
                    )
                else:
                    self.process.set_status()

            return

        self.status = status
        self.save()
        operation_status.send(
            type(self),
            operation=self,
            status=status
        )

        logger = getattr(self.process, logger)
        logger(
            'Status of operation "%s" changed to "%s".' % (
                self,
                status
            )
        )

        if status == 'successful':
            if isinstance(result, dict):
                self.process.output_bundle.update_items(**result)

            self.process.set_status()
            self.process.next()

    def to_json(self):
        from .resources.operations import OperationResource
        from .resources.processes import ProcessResource
        from .resources.bundles import BundleResource

        operation_resource = OperationResource(object=self)
        packed = operation_resource.pack()

        included = []
        process_data = ProcessResource(object=self.process).pack()
        included.append(process_data['data'])

        input_bundle_data = BundleResource(
            object=self.process.input_bundle
        ).pack().get('data')

        output_bundle_data = BundleResource(
            object=self.process.output_bundle
        ).pack().get('data')

        for input_attr in input_bundle_data['attributes']:
            if input_attr in output_bundle_data['attributes']:
                input_bundle_data['attributes'][input_attr]['value'] = (
                    output_bundle_data['attributes'][input_attr]['value']
                )

        for output_attr in output_bundle_data['attributes']:
            if output_attr not in input_bundle_data['attributes']:
                input_bundle_data['attributes'][output_attr] = (
                    output_bundle_data['attributes'][output_attr]
                )

        if 'links' in input_bundle_data:
            del input_bundle_data['links']

        included.append(input_bundle_data)
        packed['included'] = included
        return packed

    class Meta:
        ordering = ('ordering',)


class Restriction(models.Model):
    operation = models.ForeignKey(
        Operation,
        related_name='restrictions',
        on_delete=models.CASCADE
    )

    kind = models.CharField(
        max_length=3,
        choices=(
            ('tag', 'tag'),
        ),
        db_index=True
    )

    value = models.CharField(max_length=255, db_index=True)

    class Meta:
        unique_together = ('value', 'kind')


class Message(models.Model):
    operation = models.ForeignKey(
        Operation,
        related_name='messages',
        on_delete=models.CASCADE
    )

    kind = models.CharField(
        max_length=7,
        choices=[(k, k) for k in settings.MESSAGE_KINDS],
        db_index=True
    )

    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ('kind', 'operation')


class OperationRequest(models.Model):
    operation = models.ForeignKey(
        Operation,
        related_name='requests',
        on_delete=models.CASCADE
    )

    operator = models.ForeignKey(
        Operator,
        related_name='requests',
        on_delete=models.CASCADE
    )

    created = models.DateTimeField(auto_now_add=True)
    response = models.BooleanField(null=True)
    responded = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        new = not self.pk
        super().save(*args, **kwargs)

        if new:
            self.operation.process.info(
                'Waiting for manual acceptance of "%s" operation.' % str(
                    self.operation
                )
            )

            operation_request.send(type(self), request=self)

    def decline(self):
        self.response = False
        self.responded = timezone.now()
        self.save()
        self.operation.cancel()
        self.operation.process.next()

    def accept(self):
        self.response = True
        self.responded = timezone.now()
        self.save()

        self.operator.machine.enqueue(
            self.operator.perform,
            args=[self.operation]
        )


class OperationResult(models.Model):
    operation = models.ForeignKey(
        Operation,
        related_name='results',
        on_delete=models.CASCADE
    )

    operator = models.ForeignKey(
        Operator,
        related_name='results',
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=10,
        choices=[
            (s, s) for s in settings.OPERATION_STATUSES
        ],
        default='pending'
    )

    data = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('operator', 'operation')


class OperationResultTag(models.Model):
    result = models.ForeignKey(
        OperationResult,
        related_name='tags',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'result')


class LogEntry(models.Model):
    process = models.ForeignKey(
        Process,
        related_name='log',
        on_delete=models.CASCADE
    )

    created = models.DateTimeField(auto_now_add=True)

    kind = models.CharField(
        max_length=7,
        choices=[(k, k) for k in settings.LOG_ENTRY_KINDS],
        db_index=True
    )

    text = models.TextField(null=True, blank=True)
    extra = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-created',)
        get_latest_by = 'created'
