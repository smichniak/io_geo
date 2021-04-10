from django.http import HttpResponse
from django.views.generic.base import TemplateView
import json


class MarkersMapView(TemplateView):
    """Markers map view."""
    template_name = "map.html"


def display_coordinates(request):
    if not request.is_ajax():
        # TODO Error?
        return HttpResponse('Wrong request')

    json_data = json.loads(str(request.body)[2:-1])
    if not json_data['features']:
        return HttpResponse('No region selected')
    elif len(json_data['features']) >= 2:  # TODO Forbid this situation in the user interface
        return HttpResponse('Select only one region')
    else:
        return HttpResponse(json_data['features'][0]['geometry']['coordinates'])


class HypsometricMapView(TemplateView):
    """Hypsometric map view."""
    template_name = "hypsometric_map.html"