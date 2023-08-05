from api import resources
from ..models import Process
import json


class ProcessMixin(object):
    def pack_attributes(self, obj):
        attrs = super().pack_attributes(obj)
        del attrs['meta']

        return attrs

    def pack_meta(self, obj):
        return json.loads(obj.meta or {})


class ProcessResource(ProcessMixin, resources.ModelResource):
    pass


class ProcessResourceList(ProcessMixin, resources.ModelResourceList):
    pass


resources.registry.register(
    Process, ProcessResourceList, ProcessResource
)
