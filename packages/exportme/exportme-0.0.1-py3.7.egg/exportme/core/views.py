from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, generate_latest

from exportme.core.models import EXPORTERS, ApiKey

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View


class CollectorList(View):
    def get(self, request):
        return render(request, 'core/collector-list.html', {
            'collector_list': self.collectors
        })

    @property
    def collectors(self):
        for entry in EXPORTERS:
            yield entry


class Collector(View):
    @property
    def apikey(self):
        return get_object_or_404(ApiKey, owner=self.request.user, service=self.entry.module_name).key

    def get(self, request, collector):
        for entry in EXPORTERS:
            if collector == entry.name:
                try:
                    self.entry = entry
                    self.module = entry.load()
                except ImportError as e:
                    return HttpResponse('Render Error')
                else:
                    registry = CollectorRegistry()
                    registry.register(self.module(self))
                    return HttpResponse(generate_latest(registry), content_type="text/plain")
        return HttpResponse('Render Error')
