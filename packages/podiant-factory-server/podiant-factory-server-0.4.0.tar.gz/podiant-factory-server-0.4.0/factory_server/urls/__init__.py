from django.conf.urls import url, include
from . import bundles, operations, processes


urlpatterns = [
    url(r'^bundles/', include(bundles)),
    url(r'^operations/', include(operations)),
    url(r'^processes/', include(processes))
]

app_name = 'factory_server'
