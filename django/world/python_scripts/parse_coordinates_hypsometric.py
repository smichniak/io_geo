import json

from django.http import HttpResponse
from .gen_hypso_map import gen_hypso_map


# In second element returns if the request is valid, if not, the first element contains error in from
# of HttpResponse, otherwise it returns request data in json form
def check_valid_request(request):
    if not request.is_ajax():
        # TODO Error?
        return HttpResponse('Wrong request'), False

    json_data = json.loads(str(request.body)[2:-1])
    if not json_data['features']:
        return HttpResponse('No region selected'), False
    elif len(json_data['features']) >= 2:
        return HttpResponse('Select only one region'), False
    elif json_data['angle'] is None or json_data['azimuth'] is None:
        return HttpResponse('Wrong parameters'), False

    return json_data, True


def parse_coordinates_hypsometric(request):
    request_result, valid = check_valid_request(request)
    if not valid:
        return request_result

    coordinates = request_result['features'][0]['geometry']['coordinates'][0]
    pk_of_the_image = gen_hypso_map(coordinates[0][0] - .05, coordinates[0][1] - .05, coordinates[2][0] + .05, coordinates[2][1]  + .05,
                                    request_result['smooth_color'],
                                    request_result['angle'],
                                    request_result['azimuth'])

    return HttpResponse(pk_of_the_image)
