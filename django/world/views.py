from django.http import HttpResponse
from django.views.generic.base import TemplateView
import json


class MarkersMapView(TemplateView):
    """Markers map view."""
    template_name = "map.html"


def draw_data(request):
    if not request.is_ajax():
        # TODO Error?
        return HttpResponse('Wrong request')

    json_data = json.loads(str(request.body)[2:-1])
    if not json_data['features']:
        return HttpResponse('No region selected')
    elif len(json_data['features']) >= 2:  # TODO Forbid this situation in the user interface
        return HttpResponse('Select only one region')
    else:
        # TODO Call some coloring function
        return HttpResponse(json_data['features'][0]['geometry']['coordinates'])
