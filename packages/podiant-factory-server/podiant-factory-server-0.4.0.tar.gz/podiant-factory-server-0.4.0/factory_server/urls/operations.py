from django.conf.urls import url
from ..views.operations import (
    OperationListView,
    OperationDetailView,
    OperationRelationView,
    OperationRelationshipView
)

urlpatterns = [
    url(
        r'^$',
        OperationListView.as_view(),
        name='factory_server_operation_list'
    ),
    url(
        r'^(?P<pk>\d+)/$',
        OperationDetailView.as_view(),
        name='factory_server_operation_detail'
    ),
    url(
        r'^(?P<pk>\d+)/process/$',
        OperationRelationView.as_view(rel='process'),
        name='factory_server_operation_process'
    ),
    url(
        r'^(?P<pk>\d+)/relationships/process/$',
        OperationRelationshipView.as_view(rel='process'),
        name='factory_server_operation_process_relationship'
    )
]
