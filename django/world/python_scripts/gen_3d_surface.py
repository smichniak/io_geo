#!/usr/bin/env python3

from osgeo import gdal
import numpy as np
import plotly.graph_objects as go
import os
from .gen_hypso_map import set_title


def gen_3d_surface(longitude1, latitude1, longitude2, latitude2):
    filename = "DEM_for_3d.tif"
    command = 'eio clip -o ' + filename + ' --bounds ' \
              + str(longitude1) + ' ' + str(latitude1) + ' ' \
              + str(longitude2) + ' ' + str(latitude2)

    os.system(command)
    gdal_data = gdal.Open(filename)
    gdal_band = gdal_data.GetRasterBand(1)
    nodataval = gdal_band.GetNoDataValue()

    data_array = gdal_data.ReadAsArray().astype(float)

    # replace missing values if necessary
    if np.any(data_array == nodataval):
        data_array[data_array == nodataval] = np.nan

    title_start = '3D Surface of ['
    title = set_title(title_start, longitude1, latitude1, longitude2, latitude1)
    # 3d generator
    fig = go.Figure(data=[go.Surface(z=data_array)])
    fig.update_layout(title=title, autosize=True)
    fig.show()

