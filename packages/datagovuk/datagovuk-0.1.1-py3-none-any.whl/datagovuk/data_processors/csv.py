import csv
from io import StringIO

import chardet
import pandas as pd

from datagovuk.data_processors.base import PluginBase


class CSVProcessor(PluginBase):
    handlers = ['csv']
    extension = 'parquet'

    def _process(self, data):
        response = []

        encoding = chardet.detect(data)['encoding']

        csvfile = StringIO(data.decode(encoding))
        sample = csvfile.read(1024)
        csvfile.seek(0)

        sniffer = csv.Sniffer()
        skip_first = sniffer.has_header(sample)

        reader = csv.reader(csvfile)
        for row in reader:
            if skip_first:
                header = row
                skip_first = False
                continue
            response.append(dict(zip(header, row)))
        return response

    def encode(self, data):
        return pd.DataFrame(data)

    def serialise(self, data, cache_dir, name):
        data.to_parquet(self._file_name(cache_dir, name))

    def deserialise(self, cache_dir, name):
        file = self._file_name(cache_dir, name)
        if file.exists():
            return pd.read_parquet(file)
