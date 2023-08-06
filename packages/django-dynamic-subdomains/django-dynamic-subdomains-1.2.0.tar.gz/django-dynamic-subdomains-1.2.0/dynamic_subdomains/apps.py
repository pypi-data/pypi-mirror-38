import re
import monkeypatch

from django.apps import AppConfig
from django.http import HttpRequest
from django.conf.urls import url, include
from django.test.client import RequestFactory
from django.utils.module_loading import import_string

from .utils import HttpRequest__get_host, RequestFactory__generic
from .app_settings import app_settings

class DynamicSubdomainsConfig(AppConfig):
    name = 'dynamic_subdomains'

    def ready(self):
        for x in app_settings.SUBDOMAINS:
            # We add a literal period to the end of every pattern to avoid rather
            # unwieldy escaping in every definition.
            x['_regex'] = re.compile(r'%s(\.|$)' % x['regex'])
            x['_callback'] = import_string(x['callback'])

        if not app_settings.EMULATE:
            return

        monkeypatch.patch(HttpRequest__get_host, HttpRequest, 'get_host')
        monkeypatch.patch(RequestFactory__generic, RequestFactory, 'generic')

        # Inject our URLs
        for x in app_settings.SUBDOMAINS:
            urlconf_module = import_string(x['urlconf'])
            urlconf_module.urlpatterns = list(urlconf_module.urlpatterns) + [
                url(r'^_/subdomains/', include('dynamic_subdomains.urls',
                    namespace='dynamic-subdomains')),
            ]
