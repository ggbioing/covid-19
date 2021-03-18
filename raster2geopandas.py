"""
https://kodu.ut.ee/~kmoch/geopython2019/L4/raster.html
"""
import numpy as np
import matplotlib.pyplot as plt
from geo import COM, PROV
import rasterio
from rasterio.crs import CRS
from rasterio.transform import Affine, from_bounds
from rasterio.windows import Window
from rasterio.plot import show


def bbox(img):
    a = np.where(img != 0)
    box = np.min(a[0]), np.max(a[0]), np.min(a[1]), np.max(a[1])
    return box


rcode = 16  # Puglia

reg = COM[COM['cod_reg'] == rcode]
reg.plot()

R = PROV.dissolve(by='reg_name', aggfunc='sum').loc[['puglia']]
R.plot()
R1 = R.to_crs(epsg=3395)
R1.plot()

crs = CRS({"init": "epsg:4326"})

r = rasterio.open('fig/puglia.png', 'r+')
dir(r)


fig, ax = plt.subplots(1, 4)
for i, _ in enumerate(d):
	ax[i].imshow(_)


fig, ax = plt.subplots(1, 2)
ax[0].imshow(mask)
R.plot(ax=ax[1], facecolor='none', edgecolor='red')



####
box = bbox(mask)
newmask = mask[box[0]:box[1], box[2]:box[3]]
#window = Window(col_off, row_off, width, height)
wind = box[0], box[2], box[1]-box[0], box[3]-box[2]
# wind = box[2], box[0], box[3]-box[2], box[1]-box[0]
window = Window(*wind)
w = newmask.shape[1]
h = newmask.shape[0]
b = R.bounds.to_numpy().ravel()
transform = from_bounds(*b, w, h) # def from_bounds(west, south, east, north, width, height):

sdict = {
	'driver': 'GTiff',
	'height': h,
	'width': w,
	'count': 1,
	'dtype': newmask.dtype,
	'crs': '+proj=latlong',
	# 'crs': CRS({"init": "epsg:4326"}),
	# 'crs': CRS({"init": "epsg:32618"}),
	'transform': transform,
}

with rasterio.open('fig/puglia.tif', 'w', **sdict) as dst:
	dst.write(newmask, indexes=1)#, window=window)

with rasterio.open('fig/puglia.tif', 'r') as src:
	fig, ax = plt.subplots()
	show(src, ax=ax)
reg.plot(ax=ax, facecolor='none', edgecolor='red')
print("See you")