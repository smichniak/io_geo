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


def hillshade(array, azimuth, angle_altitude):
    x, y = np.gradient(array)
    slope = np.pi / 2. - np.arctan(np.sqrt(x * x + y * y))
    aspect = np.arctan2(-x, y)
    azimuthrad = azimuth * np.pi / 180.
    altituderad = angle_altitude * np.pi / 180.

    shaded = np.sin(altituderad) * np.sin(slope) + np.cos(altituderad) * np.cos(slope) * np.cos(azimuthrad - aspect)

    return 255 * (shaded + 1) / 2


# E1/W1, N1/S1, E2/W2, N2/S2, 0/1 - steps/smooth
def gen_hypso_map(longitude1, latitude1, longitude2, latitude2, smooth_colouring, angle, azimuth):
    topocmap = 'Spectral_r'
    details_map = gen_details_map(longitude1, latitude1, longitude2, latitude2)
    data_array, hypso_map, hypso_map_database_url = get_dem_data(longitude1, latitude1,
                                                                 longitude2, latitude2)

    hypso_map += '.png'
    hypso_map_database_url += '.png'
    # Plot our data with Matplotlib's 'contourf'
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    ax.matshow(hillshade(data_array, azimuth, angle), cmap='Greys', alpha=.5, zorder=10)
    cax = ax.contourf(data_array, cmap=topocmap, origin='image',
                      levels=get_levels(data_array, smooth_colouring), zorder=0)
    ax.axis('off')
    fig.colorbar(cax, ax=ax)
    title_start = 'Hypsometric map of ['
    fig.suptitle(set_title(title_start, longitude1, latitude1, longitude2, latitude2))
    fig.gca().set_aspect('equal', adjustable='box')
    fig.savefig(hypso_map)

    saved_image = HypsometricImages.objects.create(image=hypso_map_database_url, details_map=details_map)

    return saved_image.id
