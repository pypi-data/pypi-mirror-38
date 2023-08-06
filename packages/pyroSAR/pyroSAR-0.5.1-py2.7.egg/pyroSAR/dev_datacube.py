from pyroSAR.datacube_util import Product, Dataset
from pyroSAR.ancillary import groupby, find_datasets

# define a directory containing processed SAR scenes
dir = '/home/john/Desktop/Spain_Fuente-de-Piedra'

# define a directory for storing the ingestion YMLs; these are used to ingest dataset into the datacube
outdir = '/home/john/Desktop/test_dcube'

# define a name for the product YML; this is used for creating a new product in the datacube
product_yml = '/home/john/Desktop/product_test.yml'

# product description
name = 'S1_GRD_test'
product_type = 'gamma0'
description = 'this is just some test'

# define the units of the dataset measurements (i.e. polarizations)
units = 'backscatter'
# alternatively this could be a dictionary:
# units = {'VV': 'backscatter VV', 'VH': 'backscatter VH'}

# find pyroSAR files by metadata attributes
files = find_datasets(dir, recursive=True, sensor=('S1A', 'S1B'))

# group the found files by their file basenames
# files with the same basename are considered to belong to the same dataset
grouped = groupby(files, 'outname_base')

# create a new product and add the collected datasets to it
# alternatively, an existing product can be used by providing the corresponding product YML file
with Product(name=name,
             product_type=product_type,
             description=description) as prod:

    for dataset in grouped:
        with Dataset(dataset, units=units) as ds:

            # add the datasets to the product
            # this will generalize the metadata from those datasets to measurement descriptions,
            # which define the product definition
            prod.add(ds)

            # parse datacube ingestion YMLs from product and dataset metadata
            prod.export_indexing_yml(ds, outdir)

    # print the product metadata, which is written to the product YML
    print(prod)

    # write the product YML
    prod.write(product_yml)

with Product(name=name,
             product_type=product_type,
             description=description) as prod:
# with Product(product_yml) as prod:
    # print(prod)
    # print(prod.meta)
    print(prod.platform)
    print(prod.instrument)
    print(prod.product_type)
    print(prod.format)
    prod.format = 'ENVI'
    print(prod.format)
    prod.export_ingestion_yml(outdir='/home/john/Desktop',
                              name='S1_GRD_test_ingest2',
                              location='/home/john/Desktop/test_ingest')
with Product(name=name,
             product_type=product_type,
             description=description) as prod:
    print(prod.platform)
    print(prod.instrument)
    print(prod.format)
    print(prod.crs)
    prod.platform = 'SENTINEL-1'
    prod.instrument = 'C-SAR'
    prod.format = 'GTiff'
    prod.crs = 'EPSG:32630'
    prod.resolution = {'x': 20.0, 'y': 20.0}
    # print(prod)
    with Dataset(grouped[0]) as ds:
        prod.add(ds)
    print(prod)
    prod.write('/home/john/Desktop/product_test_new.yml')
