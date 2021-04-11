#!/usr/bin/env python3
import uuid

from matplotlib.colors import ListedColormap
from osgeo import gdal
import numpy as np
import os
import matplotlib.pyplot as plt
import tempfile
from ..models import HypsometricImages


def set_title(longitude1, latitude1, longitude2, latitude2):
    title = 'Hypsometric map of ['
    title += str(abs(latitude1))
    if latitude1 >= 0.:
        title += 'N '
    else:
        title += 'S '

    title += str(abs(longitude1))

    if longitude1 >= 0.:
        title += 'E, '
    else:
        title += 'W, '

    title += str(abs(latitude2))

    if latitude2 >= 0.:
        title += 'N '
    else:
        title += 'S '

    title += str(abs(longitude2))

    if longitude2 >= 0.:
        title += 'E]'
    else:
        title += 'W]'

    return title


def get_cmap():
    # set color map
    # combine 'terrain' matplotlib color map with 'Greens' and 'hot'
    terrain = plt.get_cmap('terrain')
    greens = plt.get_cmap('PiYG')
    hot = plt.get_cmap('hot')

    terrain = terrain(np.linspace(0, 1, 256))
    greens = greens(np.linspace(0, 1, 256))
    hot = hot(np.linspace(0, 1, 256))

    # terrain[:64, :] = greens[128:][::2]
    terrain[208:] = hot[58:154][::2][::-1]

    newcmap = ListedColormap(terrain)

    return newcmap


def get_levels(data_array, smooth_colouring):
    top = int(data_array.max())
    step = 250
    if smooth_colouring:
        step = 50
    return list(range(0, top + 500, step))


# E1/W1, N1/S1, E2/W2, N2/S2, 0/1 - steps/smooth
def gen_hypso_map(longitude1, latitude1, longitude2, latitude2, smooth_colouring):
    filename = tempfile.NamedTemporaryFile(suffix='.tif')
    unique_name = str(uuid.uuid4())
    hypso_map = 'media/uploaded_images/' + unique_name + '.png'
    hypso_map_database_url = 'uploaded_images/' + unique_name + '.png'

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

    # Plot our data with Matplotlib's 'contourf'
    plt.figure(figsize=(12, 8))
    plt.axis('off')
    plt.contourf(data_array, cmap=get_cmap(), levels=get_levels(data_array, smooth_colouring))

    plt.title(set_title(longitude1, latitude1, longitude2, latitude2))
    plt.colorbar()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig(hypso_map)

    saved_image = HypsometricImages.objects.create(image=hypso_map_database_url)

    filename.close()

    return saved_image.id
