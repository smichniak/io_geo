from django.contrib.gis import admin

from .models import Marker, HypsometricImages, MapDetailsImages


# Register your models here.

@admin.register(Marker)
class MarkerAdmin(admin.OSMGeoAdmin):
    """Marker admin."""

    list_display = ("name", "location")


@admin.register(HypsometricImages)
class HypsometricImagesAdmin(admin.ModelAdmin):
    list_display = ('image', 'details_map')
    fields = ('image', 'details_map')


@admin.register(MapDetailsImages)
class MapDetailsImagesAdmin(admin.ModelAdmin):
    list_display = ('image_file', 'image_url',)
    fields = ('image', 'image_url',)
