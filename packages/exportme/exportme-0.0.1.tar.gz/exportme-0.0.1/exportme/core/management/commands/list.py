from prometheus_client import CollectorRegistry, generate_latest

from exportme.core.models import EXPORTERS, ApiKey

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("collector", nargs="?")
        parser.add_argument("username", nargs="?")

    @property
    def apikey(self):
        return get_object_or_404(
            ApiKey, owner__username=self.username, service=self.entry.module_name
        ).key

    def get(self, entry):
        try:
            self.entry = entry
            self.module = entry.load()
        except ImportError as e:
            print("Error loading")
        else:
            registry = CollectorRegistry()
            registry.register(self.module(self))
            print(generate_latest(registry).decode("utf8"))

    def handle(self, collector, username, **options):
        if collector is None:
            for entry in EXPORTERS:
                print(entry)
        else:
            for entry in EXPORTERS:
                if collector == entry.name:
                    self.username = username
                    return self.get(entry)
