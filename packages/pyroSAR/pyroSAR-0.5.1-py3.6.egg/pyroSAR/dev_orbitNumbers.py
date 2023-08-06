import os
from datetime import datetime

from pyroSAR.ERS.auxil import passdb_create, passdb_query

# ers1 = '/home/john/Desktop/ers1passes.tab'
# ers2 = '/home/john/Desktop/ers2passes.tab'
#
#
# dbname = '/home/john/PycharmProjects/pyroSAR/pyroSAR/ERS/data/erspasses.db'
#
# # if os.path.isfile(dbname):
# #     os.remove(dbname)
# #
# # passdb_create(ers1passes=ers1, ers2passes=ers2, dbname=dbname)
#
# date = datetime.strptime('2011-03-02 23:20:00.0', '%Y-%m-%d %H:%M:%S.%f')
# print(passdb_query('ERS2', date, dbname))


# con = sqlite_setup(driver=dbname)
# cursor = con.cursor()
# print(cursor.execute('''SELECT Count(*) FROM data''').fetchone()[0])
#
# cursor.execute('PRAGMA table_info(data)')
# print(sorted([str(x[1]) for x in cursor.fetchall()]))
#
# query = '''SELECT * FROM data WHERE satellite = ? AND starttime <= ? AND endtime >= ?'''
# cursor.execute(query, (sat, '2011-03-02 23:20:00.0', '2011-03-02 23:20:00.0'))
# print(cursor.fetchall())

###########################################################
# from datetime import datetime
# from pyroSAR import identify
# from pyroSAR.ERS.auxil import passdb_query
#
# filename = '/geonfs01_vol1/ve39vem/archive/SAR/ERS/DRAGON/ERS1_0132_2529_20dec95.zip'
#
# id = identify(filename)
#
# print(id.sensor)
# print(id.start)
# dt = datetime.strptime(id.start, '%Y%m%dT%H%M%S')
# print(passdb_query(id.sensor, dt))
#
# print(passdb_query('ERS2', datetime.strptime('2011-03-02 23:20:00.0', '%Y-%m-%d %H:%M:%S.%f')))
#
#
# from spatialist import sqlite_setup
# dbname = '/homes4/geoinf/ve39vem/scripts/pythonland/pyroSAR/ERS/data/erspasses.db'
# con = sqlite_setup(driver=dbname)
# cursor = con.cursor()
# query = '''SELECT * FROM data WHERE satellite = ? AND starttime <= ? AND endtime >= ?'''
# datestring = dt.strftime('%Y-%m-%d %H:%M:%S.%f')
# cursor.execute(query, ('ERS1', datestring, datestring))
# print(cursor.fetchall())
#
# query = '''SELECT * FROM data WHERE satellite = "ERS1"'''
# cursor.execute(query)
# for item in cursor.fetchall():
#     print(item)
#
#
# '1995-12-20 02:43:20.000000'
###########################################################
from pyroSAR import identify

filename = '/geonfs01_vol3/swos/data/ers_envisat/SAR_IMP_1PXESA20110215_100902_00000017A165_00208_82727_2688.E2.zip'

id = identify(filename)

for key in sorted(id.meta.keys()):
    print(key, id.meta[key])
