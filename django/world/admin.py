from django.contrib.gis import admin

from .models import Marker, HypsometricImages


# Register your models here.

@admin.register(Marker)
class MarkerAdmin(admin.OSMGeoAdmin):
    """Marker admin."""

    list_display = ("name", "location")


@admin.register(HypsometricImages)
class HypsometricImagesAdmin(admin.ModelAdmin):
    list_display = ('image',)
    fields = ('image',)
