from django.http import HttpResponse
from .parse_coordinates_hypsometric import check_valid_request
from .gen_3d_surface import gen_3d_surface


def parse_coordinates_3D(request):
    request_result, valid = check_valid_request(request)
    if not valid:
        return request_result

    coordinates = request_result['features'][0]['geometry']['coordinates'][0]
    pk_of_the_image = gen_3d_surface(coordinates[0][0] - .05, coordinates[0][1] - .05,
                                     coordinates[2][0] + .05, coordinates[2][1] + .05)

    return HttpResponse(pk_of_the_image)
