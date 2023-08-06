"""
connect all TanDEM-X 90m DEM tiles to a GDAL VRT metadata file
John Truckenbrodt 2018

this enables using the whole dataset as one file for subsetting, resampling, etc.
without having to think about the tiles needed for the subset
"""

# this is a dirty little hackaround to circumvent problems with different GDAL versions on Terrasense
# just ignore this part ;-)
evil = '/usr/local/lib/python2.7/site-packages/GDAL-2.0.0-py2.7-linux-x86_64.egg'
import sys
if evil in sys.path:
    del sys.path[sys.path.index(evil)]

# import some file search functionality
from pyroSAR.drivers import findfiles
from spatialist.ancillary import finder

# import a function to create the VRT file
# see here for docs: https://spatialist.readthedocs.io/en/latest/spatialist.html#spatialist.auxil.gdalbuildvrt
from spatialist import gdalbuildvrt

# define a regex search pattern
pattern = 'TDM1_DEM__30_[0-9NSEW]{7}'

# search for all zipped archives containing DEM tiles
zips = finder(folder='/geonfs02_vol1/TDX_90mdem/DEM',
              matchlist=[pattern + '\.zip'],
              regex=True,
              recursive=True)

# search the archives for the actual DEM tiles
tiles = []
for zip in zips:
    tile = findfiles(zip, pattern + '_DEM\.tif')
    if len(tile) == 0:
        print(zip)
    else:
        tiles.append(tile[0])

# prepend the vsizip directive to the zipped files so that they can be read by GDAL
tiles = ['/vsizip/' + tile for tile in tiles]

# example name:
# '/vsizip//geonfs02_vol1/TDX_90mdem/DEM/N00/E000/TDM1_DEM__30_N00E006.zip/TDM1_DEM__30_N00E006_V01_C/DEM/TDM1_DEM__30_N00E006_DEM.tif'

# connect all tiles in a VRT dataset, which can be used by GDAL like a regular raster file
gdalbuildvrt(src=tiles,
             dst='/geonfs02_vol1/TDX_90mdem/TDX_90mdem.vrt',
             options={'srcNodata': -32767,
                      'VRTNodata': -32767})
