# import re
# from pyroSAR.gamma.parser import parse_command, parse_module
# result = parse_command('adapt_filt')
# print(result)
# print(repr(result))
#
# parse_module('/cluster/GAMMA_SOFTWARE-20161207/ISP/bin', '/homes4/geoinf/ve39vem/parser_demo.py')
#
# raw = '''*** Offset tracking between MLI images using intensity cross-correlation ***
# *** Copyright 2016, Gamma Remote Sensing, v4.8 clw 22-Octf-2016 ***
#
# usage: offset_pwrm <MLI-1> <MLI-2> <DIFF_par> <offs> <ccp> [rwin] [azwin] [offsets] [n_ovr] [nr] [naz] [thres] [c_ovr] [pflag] [pltflg] [ccs]
#
# input parameters:
#   MLI-1     (input) real valued intensity image 1 (reference)
#   MLI-2     (input) real valued intensity image 2
#   DIFF_par  DIFF/GEO parameter file
#   offs      (output) offset estimates (fcomplex)
#   ccp       (output) cross-correlation of each patch (0.0->1.0) (float)
#   rwin      range patch size (range pixels, (enter - for default from offset parameter file)
#   azwin     azimuth patch size (azimuth lines, (enter - for default from offset parameter file)
#   offsets   (output) range and azimuth offsets and cross-correlation data in text format, enter - for no output
#   n_ovr     MLI oversampling factor (integer 2**N (1,2,4,8), enter - for default: 2)
#   nr        number of offset estimates in range direction (enter - for default from offset parameter file)
#   naz       number of offset estimates in azimuth direction (enter - for default from offset parameter file)
#   thres     cross-correlation threshold (enter - for default from offset parameter file)
#   c_ovr     correlation function oversampling factor (integer 2**N (1,2,4,8) default: 4)
#   pflag     print flag
#               0:print offset summary
#               1:print all offset data
#   pltflg    plotting flag:
#               0: none (default)
#               1: screen output
#               2: screen output and PNG format plots
#               3: output plots in PDF format
#   ccs       (output) cross-correlation standard deviation of each patch (float)
#
# '''

# args = ['MLI-1', 'MLI-2', 'DIFF_par', 'offs', 'ccp', 'rwin', 'azwin', 'offsets',
#         'n_ovr', 'nr', 'naz', 'thres', 'c_ovr', 'pflag', 'pltflg', 'ccs']
#
# tabspace = ' ' * 4
#
# docstring_elements = ['{0}Parameters\n{0}----------'.format(tabspace)]
#
# starts = [re.search(r'\n[ ]*{0}.*'.format(x), raw).start() for x in args] + [len(raw)]
# for i in range(0, len(starts)-1):
#     doc_raw = raw[starts[i]:starts[i+1]]
#     print(repr(doc_raw))
#     pattern = r'\n[ ]*(?P<command>{0})[ ]+(?P<doc>.*)'.format('|'.join(args))
#     match = re.match(pattern, doc_raw, flags=re.DOTALL)
#     cmd = match.group('command')
#     print(repr(cmd))
#     # print(repr(match.group('doc')))
#     doc_items = re.split('\n+\s*', match.group('doc').strip('\n'))
#     description = '\n{0}{0}{0}'.join(doc_items).format(tabspace)
#     print(doc_items)
#     doc = '{0}{1}:\n{0}{0}{2}'.format(tabspace, cmd, description)
#     docstring_elements.append(doc)
#     print(doc)
#     print('=======================================================================')
# print('\n'.join(docstring_elements))
import os
from pyroSAR.gamma.api import diff
from pyroSAR.gamma.error import GammaUnknownError

refs = ['/usr/share/gdal/2.2/pcs.csv',
        '/usr/share/gdal/2.2/gcs.csv']

outdir = 'home/john/gamma_crs_test'

if not os.path.isdir(outdir):
    os.makedirs(outdir)

print(os.path.realpath(outdir))

# counter = 0
# for ref in refs:
#     with open(ref, 'r') as crs:
#         header = crs.readline()
#         for line in crs:
#             items = line.split(',')
#             epsg = items[0]
#             counter += 1
#             print('{}: {}'.format(counter, epsg))
#             try:
#                 outname = os.path.join(outdir, 'dempar_{}.par'.format(epsg))
#                 diff.create_dem_par(outname, EPSG=epsg)
#                 print('{}: sucess'.format(epsg))
#             except GammaUnknownError:
#                 print('{}: fail'.format(epsg))
#                 continue
