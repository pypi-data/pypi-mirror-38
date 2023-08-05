from api import resources
from ..models import Bundle


class BundleMixin(object):
    model = Bundle

    def pack_attributes(self, obj):
        return dict(
            [
                (
                    item.key.replace('-', '_'),
                    item.as_dict()
                )
                for item in obj.items.order_by('key')
                if item.value
            ]
        )


class BundleResource(BundleMixin, resources.ModelResource):
    pass


class BundleResourceList(BundleMixin, resources.ModelResourceList):
    pass


resources.registry.register(
    Bundle, BundleResourceList, BundleResource
)
