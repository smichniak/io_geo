from django.http import HttpResponse
from .parse_coordinates_hypsometric import check_valid_request


def parse_coordinates_3D(request):
    request_result, valid = check_valid_request(request)
    if not valid:
        return request_result

    coordinates = request_result['features'][0]['geometry']['coordinates'][0]

    # TODO 3D display needs to be done yet.

    return HttpResponse(':)')
