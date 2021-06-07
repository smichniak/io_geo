from django.http import HttpResponse
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from .models import HypsometricImages
from .models import SurfaceImages

from .python_scripts.parse_coordinates_hypsometric import check_valid_request
from .python_scripts.gen_hypso_map import set_title


class MarkersMapView(TemplateView):
    """Markers map view."""
    template_name = "map.html"


def display_coordinates(request):
    request_result, valid = check_valid_request(request)
    if not valid:
        return request_result

    coordinates = request_result['features'][0]['geometry']['coordinates'][0]
    long1, lat1, long2, lat2 = coordinates[0][0], coordinates[0][1], coordinates[2][0], coordinates[2][1]
    return HttpResponse(set_title('', long1, lat1, long2, lat2)[:-1])  # [:-1] to remove the last char ']'


class HypsometricMapView(DetailView):
    model = HypsometricImages
    queryset = HypsometricImages.objects.all()
    context_object_name = 'hypso_map'

    template_name = "hypsometric_map.html"


class MapView3D(DetailView):
    model = SurfaceImages
    queryset = SurfaceImages.objects.all()
    context_object_name = 'map3d'

    template_name = "map_3d.html"
