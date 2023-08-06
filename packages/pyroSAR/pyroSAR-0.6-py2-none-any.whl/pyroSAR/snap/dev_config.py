# import re
#
# filename = '/usr/local/snap/etc/snap.auxdata.properties'
#
# pattern = r'^(?P<key>[\w\.]*)\s*=\s*(?P<value>.*)\n'

# test = 'OrbitFiles.delftERS2OrbitPath = ${AuxDataPath}/Orbits/Delft Precise Orbits/ODR.ERS-2/dgm-e04\n'
#
# print(re.search(pattern, test))

# snap_properties = {}
#
# with open(filename, 'r') as prop:
#     for line in prop:
#         print(repr(line))
#         if re.search(pattern, line):
#             print('match')
#             key, value = re.match(re.compile(pattern), line).groups()
#             snap_properties[key] = value
#
# print(snap_properties.keys())

# print(type(snap_properties['DEM.srtm1GridDEMDataPath']))

#####################################################################
import os

config = '/home/john/.pyrosar/config.ini'
if os.path.isfile(config):
    os.remove(config)

from pyroSAR.snap import ExamineSnap

env = os.environ['PATH']

os.environ['PATH'] = ''

test = ExamineSnap()

print('=========================================')

os.environ['PATH'] = env

test2 = ExamineSnap()

print('=========================================')

test3 = ExamineSnap()
# print(test.auxdata)
# print(isinstance(test.auxdata, list))
#####################################################################
# from pyroSAR import ConfigHandler
#
# print(ConfigHandler.sections)
