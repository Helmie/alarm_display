__author__ = 'Christopher'

from django.contrib import admin
from model import models


class EngineAdmin(admin.ModelAdmin):
    list_display = ('station', 'engine_type', 'seq_number')
    list_filter = ['station', 'engine_type']

class StationAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(models.Station, StationAdmin)
admin.site.register(models.EngineType)
admin.site.register(models.Engine, EngineAdmin)
admin.site.register(models.Mission)