from django.conf.urls import url
from ..views.bundles import (
    BundleListView,
    BundleDetailView,
    BundleRelationView,
    BundleRelationshipView
)

urlpatterns = [
    url(
        r'^$',
        BundleListView.as_view(),
        name='factory_server_bundle_list'
    ),
    url(
        r'^(?P<pk>\d+)/$',
        BundleDetailView.as_view(),
        name='factory_server_bundle_detail'
    ),
    url(
        r'^(?P<pk>\d+)/process/$',
        BundleRelationView.as_view(rel='process'),
        name='factory_server_bundle_process'
    ),
    url(
        r'^(?P<pk>\d+)/relationships/process/$',
        BundleRelationshipView.as_view(rel='process'),
        name='factory_server_bundle_process_relationship'
    )
]
