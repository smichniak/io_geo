#!/usr/bin/env python3

from osgeo import gdal
import numpy as np
import plotly.graph_objects as go
import os


os.system("eio clip -o Shasta-30m-DEM.tif --bounds 19.5 48.5 21.5 50.5")

filename = "Shasta-30m-DEM.tif"
gdal_data = gdal.Open(filename)
gdal_band = gdal_data.GetRasterBand(1)
nodataval = gdal_band.GetNoDataValue()

data_array = gdal_data.ReadAsArray().astype(float)

# replace missing values if necessary
if np.any(data_array == nodataval):
    data_array[data_array == nodataval] = np.nan


# 3d generator
fig = go.Figure(data=[go.Surface(z=data_array)])
fig.update_layout(title='3D Surface of ...(bounds)', autosize=True)
fig.show()
print(data_array)

#os.system("rm -rf *.tif")