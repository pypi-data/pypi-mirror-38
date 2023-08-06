from django.shortcuts import get_object_or_404
from exportme.core.models import ApiKey


class Collector(object):
    def __init__(self, view):
        self.view = view
