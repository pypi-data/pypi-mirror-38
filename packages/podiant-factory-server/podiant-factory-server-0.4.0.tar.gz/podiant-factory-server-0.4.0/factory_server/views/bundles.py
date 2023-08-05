from api.views import ListView, DetailView, RelationView, RelationshipView
from ..auth import MachineKeyAuthenticator, BundleAuthoriser
from ..models import Bundle
from ..resources.bundles import BundleResource, BundleResourceList


class BundleMixin(object):
    model = Bundle
    authenticators = [MachineKeyAuthenticator]
    authorisers = [BundleAuthoriser]


class BundleListView(BundleMixin, ListView):
    resource_class = BundleResourceList


class BundleDetailView(BundleMixin, DetailView):
    resource_class = BundleResource


class BundleRelationView(BundleMixin, RelationView):
    resource_class = BundleResource
    rel = None


class BundleRelationshipView(BundleMixin, RelationshipView):
    resource_class = BundleResource
    rel = None
