from setuptools import find_packages, setup

setup(
    name='datagovuk',
    version='0.1.1',
    packages=find_packages(),
    url='https://github.com/drewsonne/datagovuk',
    license='LGPLv3',
    author='Drew J. Sonne',
    author_email='drew.sonne@gmail.com',
    description='Tool to allow easy importing to data from data.gov.uk',
    install_requires=['ckanapi', 'pandas', 'pyarrow'],
    entry_points={
        'datagovuk.plugins.processors': [
            'geojson = datagovuk.data_processors.geojson:GeoJSONProcessor [gis]',
            'csv = datagovuk.data_processors.csv:CSVProcessor'
        ]
    },
    extras_require={
        'gis': ['geopandas', 'matplotlib']
    }
)
