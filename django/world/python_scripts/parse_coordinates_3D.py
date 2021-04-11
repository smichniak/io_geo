import json

from django.http import HttpResponse

def parse_coordinates_3D(request):
    if not request.is_ajax():
        # TODO Error?
        return HttpResponse('Wrong request')

    json_data = json.loads(str(request.body)[2:-1])
    if not json_data['features']:
        return HttpResponse('No region selected')
    elif len(json_data['features']) >= 2:  # TODO Forbid this situation in the user interface
        return HttpResponse('Select only one region')

    coordinates = json_data['features'][0]['geometry']['coordinates'][0]

    # TODO 3D display needs to be done yet.

    return HttpResponse(':)')