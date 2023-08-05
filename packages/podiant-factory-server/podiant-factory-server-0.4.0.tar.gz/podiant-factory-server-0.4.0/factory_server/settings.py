from django.conf import settings
import re
import os


BUNDLE_ITEM_KINDS = (
    'array',
    'boolean',
    'media',
    'null',
    'number',
    'object',
    'string'
)

MESSAGE_KINDS = (
    'confirm',
    'success',
    'error'
)

LOG_ENTRY_KINDS = (
    'debug',
    'info',
    'warning',
    'success',
    'error'
)

OPERATION_SCHEDULES = (
    'auto',
    'manual',
)

OPERATION_STATUSES = (
    'pending',
    'scheduling',
    'scheduled',
    'running',
    'failed',
    'cancelled',
    'successful'
)

PROCESS_STATUSES = (
    'pending',
    'running',
    'failed',
    'successful'
)

CODENAME_RE = re.compile(r'^([a-z][a-z0-9_]*)\.([a-z][a-z0-9_]*)$')

MACHINE_PROCESS_MATCHERS = getattr(
    settings,
    'MACHINE_PROCESS_MATCHERS',
    ()
)

DEFAULT_TIMEOUT = getattr(
    settings,
    'FACTORY_DEFAULT_TIMEOUT',
    300
)  # Default timeout = 5 minutes


START_TIMEOUT = getattr(
    settings,
    'FACTORY_START_TIMEOUT',
    DEFAULT_TIMEOUT
)

RUNNING_TIMEOUT = getattr(
    settings,
    'FACTORY_RUNNING_TIMEOUT',
    DEFAULT_TIMEOUT
)

DOMAIN = getattr(settings, 'FACTORY_API_DOMAIN', None)
SSL = getattr(settings, 'FACTORY_API_SSL', True)
AWS_S3_HOST = getattr(
    settings,
    'AWS_S3_HOST',
    os.getenv(
        'AWS_S3_HOST',
        's3-eu-west-1.amazonaws.com'
    )
)

AWS_S3_ENDPOINT_URL = getattr(
    settings,
    'AWS_S3_ENDPOINT_URL',
    os.getenv(
        'AWS_S3_ENDPOINT_URL',
        'https://%s/' % AWS_S3_HOST
    )
)

AWS_S3_BUCKET = getattr(
    settings,
    'AWS_S3_BUCKET',
    os.getenv(
        'AWS_S3_BUCKET',
        'factory'
    )
)
