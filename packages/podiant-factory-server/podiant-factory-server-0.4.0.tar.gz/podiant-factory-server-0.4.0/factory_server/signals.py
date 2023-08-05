from django.dispatch import Signal


operation_request = Signal(providing_args=('request',))
operation_status = Signal(providing_args=('operation', 'status'))
process_status = Signal(providing_args=('process', 'status', 'progress'))
