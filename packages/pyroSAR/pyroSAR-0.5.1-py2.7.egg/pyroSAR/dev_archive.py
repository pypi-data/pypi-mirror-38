import os
from pyroSAR import identify, Archive
from pyroSAR.snap import geocode

filename = '/home/john/PycharmProjects/pyroSAR/pyroSAR/tests/data/' \
           'S1A_IW_GRDH_1SDV_20150222T170750_20150222T170815_004739_005DD8_3768.zip'

id = identify(filename)


geocode(id, outdir='/home/john/Desktop', basename_extensions=['orbitNumber_rel'], test=True)

# print(id.meta.keys())
#
# print(id.meta['orbitNumber_abs'])
#
# dbfile = '/home/john/Desktop/test.db'
#
# if os.path.isfile(dbfile):
#     os.remove(dbfile)
#
# # extra = {'orbitNumber_abs_start': 'INTEGER',
# #          'orbitNumber_abs_stop': 'INTEGER'}
# #
# # with Archive(dbfile=dbfile, custom_fields=extra) as db:
# #     db.insert(id)
# #     print(db.size)
# #     print(db.get_colnames())
# #
# # with Archive(dbfile=dbfile) as db:
# #     print(db.select(orbitNumber_abs_start=4739))
#
# with Archive(dbfile=dbfile) as db:
#     db.insert(id)
#     print(db.size)
#     print(db.get_colnames())
