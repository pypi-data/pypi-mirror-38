import xml.etree.ElementTree as ET
from spatialist.ancillary import finder


def read_dim(dimfile):
    with open(dimfile, 'r') as dim:
        tree = ET.fromstring(dim.read())
    orbitNumber_rel = int(tree.find('.//Dataset_Sources/'
                                    'MDElem[@name="metadata"]/'
                                    'MDElem[@name="Abstracted_Metadata"]/'
                                    'MDATTR[@name="REL_ORBIT"]').text)
    orbit = tree.find('.//Dataset_Sources/'
                      'MDElem[@name="metadata"]/'
                      'MDElem[@name="Abstracted_Metadata"]/'
                      'MDATTR[@name="PASS"]').text
    
    return orbit, orbitNumber_rel


def dim2csv(dimfiles, csvfile):
    items = []
    for dimfile in dimfiles:
        orbit, orbitNumber_rel = read_dim(dimfile)
        items.append('{};{};{}'.format(dimfile, orbit, orbitNumber_rel))
    with open(csvfile, 'w') as csv:
        csv.write('dimfile;orbit;orbitNumber_rel\n')
        csv.write('\n'.join(items))


dimfiles = finder('dir', ['*.dim'])

dim2csv(dimfiles, 'test.csv')
