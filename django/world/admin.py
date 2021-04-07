from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Marker


# Register your models here.

# @admin.register(Marker)
class MarkerAdmin(admin.OSMGeoAdmin):
    """Marker admin."""

    list_display = ("name", "location")


admin.site.register(Marker, LeafletGeoAdmin)
