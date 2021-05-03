from ..models import MapDetailsImages


def gen_details_map(longitude1, latitude1, longitude2, latitude2):
    api_key = "137c168ea32d498b9e6f8f4ece624503"
    style = "osm-bright"
    format = "jpeg"
    area = f"rect:{longitude1},{latitude1},{longitude2},{latitude2}"

    details_map = MapDetailsImages.objects.create(
        image_url=f"https://maps.geoapify.com/v1/staticmap?style={style}&format={format}&area={area}&apiKey={api_key}")

    details_map.get_remote_image()

    return details_map
