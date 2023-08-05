from django.conf.urls import url
from ..views.processes import (
    ProcessListView,
    ProcessDetailView,
    ProcessRelationView,
    ProcessRelationshipView
)


urlpatterns = [
    url(
        r'^$',
        ProcessListView.as_view(),
        name='factory_server_process_list'
    ),
    url(
        r'^(?P<pk>\d+)/$',
        ProcessDetailView.as_view(),
        name='factory_server_process_detail'
    ),
    url(
        r'^(?P<pk>\d+)/input-bundle/$',
        ProcessRelationView.as_view(rel='input-bundle'),
        name='factory_server_process_input_bundle'
    ),
    url(
        r'^(?P<pk>\d+)/relationships/input-bundle/$',
        ProcessRelationshipView.as_view(rel='input-bundle'),
        name='factory_server_process_input_bundle_relationship'
    )
]
