from pyroSAR import Archive, identify
from pyroSAR.snap import geocode
from spatialist.ancillary import finder
from spatialist import Vector

# find all S1 SAR scenes in a directory
scenes = finder('directory', ['S1*.zip'])

# identify a scene and get familiar with its metadata attributes
id = identify(scenes[0])
print(id)

# define a database file to be written and insert the scenes
dbfile = 'scenes.db'
with Archive(dbfile) as archive:
    archive.insert(scenes)

# define an output directory
outdir = ''

# select scenes from the database
# this will return a list of scene names which match the defined criteria
# a testsite shapefile can be passed via parameter vectorobject
# see documentation here: https://pyrosar.readthedocs.io/en/latest/pyroSAR.html#pyroSAR.drivers.Archive
with Archive(dbfile) as archive:
    with Vector('site.shp') as site:
        selection_proc = archive.select(vectorobject=site,
                                        processdir=outdir,
                                        sensor=('S1A', 'S1B'),
                                        product='GRD',
                                        acquisition_mode='IW',
                                        vv=1,
                                        orbitNumber_rel=99)

# start the geocoding in test mode first; this will only create SNAP workflow XMls.
# to do the actual processing set test to False
# if XMLs were created before, they need to be deleted first.
# Otherwise pyroSAR will assume that the scene hase been processed before
# for further info see the documentation here:
# https://pyrosar.readthedocs.io/en/latest/pyroSAR.html#pyroSAR.snap.util.geocode
for scene in selection_proc:
    geocode(scene, outdir=outdir, basename_extensions=['orbitNumber_rel'], test=True)
