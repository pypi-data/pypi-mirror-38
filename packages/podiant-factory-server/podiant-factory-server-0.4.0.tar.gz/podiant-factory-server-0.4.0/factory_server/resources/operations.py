from api.exceptions import UnprocessableEntityError
from api import resources
from ..models import Operation
import json


class OperationMixin(object):
    model = Operation
    fields = (
        'process',
        'namespace',
        'function',
        'expires',
        'progress',
        'status'
    )

    readonly_fields = (
        'process',
        'namespace',
        'function',
        'expires'
    )

    relationships = ('process',)

    def pack_attributes(self, obj):
        packed = {
            'function': str(obj),
            'expires': obj.expires and obj.expires.isoformat() or None,
            'progress': obj.progress,
            'status': obj.status,
            'result': None
        }

        for result in obj.results.order_by('-pk')[:1]:
            result_data = json.loads(result.data) if result.data else {}
            result_tags = sorted(
                set(
                    result.tags.values_list('name', flat=True)
                )
            )

            if any(result_data) or any(result_tags):
                packed['result'] = result_data
                packed['result']['tags'] = result_tags

        return packed

    def unpack_attributes(self, packed):
        status = packed.pop('status', '')
        result = packed.pop('result', {})
        unpacked, extra = super().unpack_attributes(packed)

        extra['result'] = result
        extra['status'] = status

        return unpacked, extra

    def save_extra(self, extra):
        obj = self.get_object()
        status = extra.get('status')
        result = extra.get('result', {})

        if not isinstance(result, dict):
            raise UnprocessableEntityError(
                'Expected result to be an object.'
            )

        tags = result.pop('tags', [])
        if not isinstance(tags, list):
            raise UnprocessableEntityError(
                'Expected tags to be an array.'
            )

        if status and status != obj.status:
            obj.set_status(
                status,
                self.operator,
                result,
                tags
            )

        return obj


class OperationResource(OperationMixin, resources.ModelResource):
    pass


class OperationResourceList(OperationMixin, resources.ModelResourceList):
    pass


resources.registry.register(
    Operation, OperationResourceList, OperationResource
)
