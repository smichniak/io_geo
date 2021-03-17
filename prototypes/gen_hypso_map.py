#!/usr/bin/env python3

from osgeo import gdal
import numpy as np
import os
import matplotlib.pyplot as plt

os.system('eio clip -o Shasta-30m-DEM.tif --bounds 49.180417 20.085446 50.2 21.1')

filename = "Shasta-30m-DEM.tif"
gdal_data = gdal.Open(filename)
gdal_band = gdal_data.GetRasterBand(1)
nodataval = gdal_band.GetNoDataValue()

# convert to a numpy array
data_array = gdal_data.ReadAsArray().astype(float)

# replace missing values if necessary
if np.any(data_array == nodataval):
    data_array[data_array == nodataval] = np.nan

# Plot our data with Matplotlib's 'contourf'
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot()
plt.contourf(data_array, cmap="terrain",
             levels=list(range(0, 5000, 250)))
plt.title("Hypsometric map of ...(bounds)")
cbar = plt.colorbar()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

print(data_array)

#os.system("rm -rf *.tif")
