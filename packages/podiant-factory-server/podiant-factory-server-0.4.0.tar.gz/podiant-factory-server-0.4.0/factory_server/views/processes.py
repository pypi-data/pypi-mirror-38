from api.views import ListView, DetailView, RelationView, RelationshipView
from ..auth import MachineKeyAuthenticator, ProcessAuthoriser
from ..models import Process
from ..resources.processes import ProcessResource, ProcessResourceList


class ProcessMixin(object):
    model = Process
    authenticators = [MachineKeyAuthenticator]
    authorisers = [ProcessAuthoriser]


class ProcessListView(ProcessMixin, ListView):
    resource_class = ProcessResourceList


class ProcessDetailView(ProcessMixin, DetailView):
    resource_class = ProcessResource


class ProcessRelationView(ProcessMixin, RelationView):
    resource_class = ProcessResource
    rel = None


class ProcessRelationshipView(ProcessMixin, RelationshipView):
    resource_class = ProcessResource
    rel = None
