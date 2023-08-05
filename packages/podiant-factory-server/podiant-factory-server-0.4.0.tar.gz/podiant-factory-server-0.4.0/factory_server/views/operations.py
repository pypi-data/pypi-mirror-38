from api.exceptions import ForbiddenError
from api.views import ListView, DetailView, RelationView, RelationshipView
from django.db.models import Q
from ..auth import MachineKeyAuthenticator, OperationAuthoriser
from ..models import Operation
from ..resources.operations import OperationResource, OperationResourceList


class OperationMixin(object):
    model = Operation
    authenticators = [MachineKeyAuthenticator]
    authorisers = [OperationAuthoriser]


class OperationListView(OperationMixin, ListView):
    resource_class = OperationResourceList


class OperationDetailView(OperationMixin, DetailView):
    resource_class = OperationResource

    def get_operator(self, obj):
        for operator in self.request.machine.operators.filter(
            namespace=obj.namespace,
            function=obj.function
        ):
            return operator

        q = Q(
            function__isnull=True
        ) | Q(
            function=''
        )

        for operator in self.request.machine.operators.filter(
            namespace=obj.namespace
        ).filter(q):
            return operator

    def form_valid(self, form):
        resource = self.get_resource()
        obj = resource.get_object()
        resource.operator = self.get_operator(obj)

        if resource.operator is None:
            raise ForbiddenError(
                'This machine cannot perform this operation.'
            )

        return super().form_valid(form)


class OperationRelationView(OperationMixin, RelationView):
    resource_class = OperationResource
    rel = None


class OperationRelationshipView(OperationMixin, RelationshipView):
    resource_class = OperationResource
    rel = None
