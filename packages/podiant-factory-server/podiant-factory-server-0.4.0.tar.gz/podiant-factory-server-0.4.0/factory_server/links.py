from api.resources.links import ResourceLink
from django.contrib.sites.models import Site
from django.urls import reverse
from json import JSONEncoder
from urllib.parse import urlencode
from . import settings


class ResourceLinkJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ResourceLink):
            domain = settings.DOMAIN or Site.objects.get_current().domain
            proto = settings.SSL and 'https' or 'http'

            resolved = reverse(
                obj.urlname,
                kwargs=obj.kwargs
            )

            return '%s://%s%s%s' % (
                proto,
                domain,
                resolved,
                '?%s' % urlencode(obj.qs, doseq=True) if obj.qs else ''
            )

        return super().default(obj)  # pragma: no cover
