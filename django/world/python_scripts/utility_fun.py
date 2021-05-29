from osgeo import gdal
import numpy as np
import plotly.graph_objects as go
import os
import tempfile
import uuid


def get_dem_data(longitude1: float, latitude1: float, longitude2: float, latitude2: float) -> (any, str, str):
    filename = tempfile.NamedTemporaryFile(suffix='.tif')
    unique_name = str(uuid.uuid4())
    map_file = 'media/uploaded_images/' + unique_name
    map_database_url = 'uploaded_images/' + unique_name
    os.system('eio clip -o ' + filename.name + ' --bounds '
              + str(longitude1) + ' ' + str(latitude1) + ' '
              + str(longitude2) + ' ' + str(latitude2))

    gdal_data = gdal.Open(filename.name)
    gdal_band = gdal_data.GetRasterBand(1)
    nodataval = gdal_band.GetNoDataValue()

    # convert to a numpy array
    data_array = gdal_data.ReadAsArray().astype(float)

    # replace missing values if necessary
    if np.any(data_array == nodataval):
        data_array[data_array == nodataval] = np.nan

    filename.close()

    return np.flip(data_array, 0), map_file, map_database_url


# Decimal coordinates up to 5 decimal places have accuracy of ~ 1 meter, that's enough
def round_coordinates(coordinate: float) -> float:
    rounding_digits = 5
    return round(coordinate, rounding_digits)


def get_lat_symbol(latitude: float) -> str:
    if latitude >= 0:
        return 'N'
    else:
        return 'S'


def get_long_symbol(longitude1: float) -> str:
    if longitude1 >= 0:
        return 'E'
    else:
        return 'W'


def set_title(title: str, longitude1: float, latitude1: float, longitude2: float, latitude2: float) -> str:
    longitude1, latitude1, longitude2, latitude2 = map(round_coordinates,
                                                       [longitude1, latitude1, longitude2, latitude2])

    title += str(abs(latitude1))
    title += get_lat_symbol(latitude1) + ' '

    title += str(abs(longitude1))
    title += get_long_symbol(longitude1) + ', '

    title += str(abs(latitude2))
    title += get_lat_symbol(latitude2) + ' '

    title += str(abs(longitude2))
    title += get_long_symbol(longitude2) + ']'

    return title
