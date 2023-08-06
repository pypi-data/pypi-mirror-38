
from pyroSAR.gamma import geocode

scene = '/home/john/Desktop/S1_proc_test/S1A_IW_GRDH_1SDV_20150426T190111_20150426T190136_005659_00741C_FFB7.zip'
outdir = '/home/john/Desktop/S1_proc_test'

# scene = '/geonfs01_vol3/swos/data/sentinel1/GRD/S1A_IW_GRDH_1SDV_20150426T190111_20150426T190136_005659_00741C_FFB7.zip'
# outdir = '/geonfs01_vol1/ve39vem/test/snap_proc'
#
geocode(scene=scene,
        outdir=outdir,
        polarizations='VV',
        test=True)

# from pyroSAR.gamma.api import ipta, diff
#
# print(help(diff.create_dem_par))
#
# diff.create_dem_par('/home/john/Desktop/test_3857.par', EPSG=3857)
