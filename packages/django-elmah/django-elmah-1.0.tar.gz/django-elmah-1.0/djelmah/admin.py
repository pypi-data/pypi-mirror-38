from django.contrib import admin
from djelmah import models

@admin.register(models.DjelmahHost)
class DjelmahHostAdmin(admin.ModelAdmin):
    list_display = (
        'hostname',
        'username',
        'api_key',
        'active'
    )

@admin.register(models.DjelmahLog)
class DjelmahLogAdmin(admin.ModelAdmin):
    list_display = (
        'host',
        'path',
        'username',
        'datetime',
        'error_type',
        'status_code'
    )
