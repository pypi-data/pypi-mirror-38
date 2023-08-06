import tempfile

import geopandas as gpd

from datagovuk.data_processors.base import PluginBase


class GeoJSONProcessor(PluginBase):
    handlers = ['geojson']
    extension = 'shp'

    def _process(self, data):
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(data)
            tmp.seek(0)

            df = gpd.read_file(tmp.name)

        return df

    def encode(self, data):
        return data

    def serialise(self, data, cache_dir, name):
        data.to_file(
            driver='ESRI Shapefile',
            filename=self._file_name(cache_dir, name)
        )

    def deserialise(self, cache_dir, name):
        file = self._file_name(cache_dir, name)
        if file.exists():
            return gpd.read_file(file)
