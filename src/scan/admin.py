from django.contrib import admin

from scan.models import RawData


@admin.register(RawData)
class RawDataAdmin(admin.ModelAdmin):
    pass
