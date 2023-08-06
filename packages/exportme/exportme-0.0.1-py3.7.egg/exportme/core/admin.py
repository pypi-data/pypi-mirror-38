from django.contrib import admin

from . import models


@admin.register(models.ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('owner', 'service')
    list_filter = ('owner', 'service')
