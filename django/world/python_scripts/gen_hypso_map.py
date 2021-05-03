#!/usr/bin/env python3
import uuid

from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
from .utility_fun import get_dem_data
from .utility_fun import set_title
from matplotlib import use
import numpy as np
from ..models import HypsometricImages
from .gen_details_map import gen_details_map

use('Agg')  # Fixes crashes on macOS


def get_cmap():
    # set color map
    # combine 'terrain' matplotlib color map with 'Greens' and 'hot'
    terrain = plt.get_cmap('terrain')
    # greens = plt.get_cmap('PiYG')
    hot = plt.get_cmap('hot')

    terrain = terrain(np.linspace(0, 1, 256))
    # greens = greens(np.linspace(0, 1, 256))
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
    details_map = gen_details_map(longitude1, latitude1, longitude2, latitude2)

    data_array, hypso_map, hypso_map_database_url = get_dem_data(longitude1, latitude1,
                                                                 longitude2, latitude2)
    hypso_map += '.png'
    hypso_map_database_url += '.png'
    # Plot our data with Matplotlib's 'contourf'
    plt.figure(figsize=(12, 8))
    plt.axis('off')
    plt.contourf(data_array, cmap=get_cmap(), levels=get_levels(data_array, smooth_colouring))

    title_start = 'Hypsometric map of ['
    plt.title(set_title(title_start, longitude1, latitude1, longitude2, latitude2))
    plt.colorbar()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig(hypso_map)

    saved_image = HypsometricImages.objects.create(image=hypso_map_database_url, details_map=details_map)

    return saved_image.id
