from os import path, write, close
from tempfile import mkstemp
from urllib.parse import urlparse
from uuid import uuid4
from .exceptions import BundleValidationError
from . import settings
import boto3
import json
import re
import requests


class BundlerBase(object):
    base_type = None
    strict = False

    def __init__(self, value, **meta):
        self.value = value
        self.meta = meta

    def check(self):
        if self.strict and not isinstance(self.value, self.base_type):
            raise BundleValidationError(
                'Value is of incorrect type.'
            )

        if self.base_type is not None:
            try:
                self.base_type(self.value)
            except Exception:
                raise BundleValidationError(
                    'Value cannot be converted to serializable type.'
                )
        else:  # pragma: no cover
            raise NotImplementedError('Method not implemented')

    def pack(self):
        return json.dumps(self.value)


class ArrayBundler(BundlerBase):
    base_type = list
    strict = True


class BooleanBundler(BundlerBase):
    base_type = bool
    strict = True


class MediaBundler(BundlerBase):
    def check(self):
        urlparts = urlparse(self.value)
        ext = path.splitext(urlparts.path)[-1]
        handle, filename = mkstemp(ext)

        try:
            response = requests.head(self.value)
        except Exception as ex:
            raise BundleValidationError(
                'Object could not be retrieved: %s' % str(ex)
            )

        mime_type = response.headers['Content-Type']
        mime_match = re.compile(
            '^' + self.meta['mime_type'].replace(
                '/', r'\/'
            ).replace(
                '*', r'.*'
            ) + '$'
        )

        self.meta['mime_type'] = mime_type

        if mime_match.match(mime_type) is None:
            raise BundleValidationError(
                'Object content type does not match bundle requirements.'
            )

        try:
            response = requests.get(
                self.value,
                headers={
                    'User-Agent': (
                        'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 '
                        'like Mac OS X) AppleWebKit/602.1.38 (KHTML, '
                        'like Gecko) Version/10.0 Mobile/14A300 Safari/602.1'
                    )
                },
                stream=True
            )

            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=1024):
                write(handle, chunk)
        finally:
            close(handle)

        self._cached = filename

    def pack(self):
        if not hasattr(self, '_cached'):
            self.check()

        ext = path.splitext(self._cached)[-1]
        key = str(uuid4()) + ext
        s3 = boto3.client(
            's3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL
        )

        s3.put_object(
            Bucket=settings.AWS_S3_BUCKET,
            Key=key,
            Body=open(self._cached, 'rb'),
            ContentType=self.meta['mime_type']
        )

        return json.dumps(
            s3.generate_presigned_url(
                'get_object',
                Params=dict(
                    Bucket=settings.AWS_S3_BUCKET,
                    Key=key
                ),
                ExpiresIn=3600
            )
        )


class NullBundler(BundlerBase):
    def check(self):
        if self.value is not None:
            raise BundleValidationError(
                'Value cannot be converted to serializable type.'
            )


class NumberBundler(BundlerBase):
    base_type = float


class ObjectBundler(BundlerBase):
    base_type = dict


class StringBundler(BundlerBase):
    base_type = str
