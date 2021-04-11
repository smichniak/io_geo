from django.http import HttpResponse
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from .models import HypsometricImages
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


class HypsometricMapView(DetailView):
    model = HypsometricImages
    queryset = HypsometricImages.objects.all()
    context_object_name = 'hypso_map'

    template_name = "hypsometric_map.html"
