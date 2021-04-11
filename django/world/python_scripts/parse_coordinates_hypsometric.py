import json

from django.http import HttpResponse
from .gen_hypso_map import gen_hypso_map


def parse_coordinates_hypsometric(request):
    if not request.is_ajax():
        # TODO Error?
        return HttpResponse('Wrong request')

    json_data = json.loads(str(request.body)[2:-1])
    if not json_data['features']:
        return HttpResponse('No region selected')
    elif len(json_data['features']) >= 2:  # TODO Forbid this situation in the user interface
        return HttpResponse('Select only one region')

    coordinates = json_data['features'][0]['geometry']['coordinates'][0]
    pk_of_the_image = gen_hypso_map(coordinates[0][0], coordinates[0][1], coordinates[2][0], coordinates[2][1], 0)

    return HttpResponse(pk_of_the_image)
