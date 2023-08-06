import csv
import zipfile
from io import BytesIO, StringIO

import requests

from datagovuk.calls.base import BaseCall
from datagovuk.data_processors import plugins
from datagovuk.data_processors.base import PluginCallBase


class FetchAllDatasetsBaseCall(BaseCall):
    facet = None
    column_mapping = {}
    metadata_file_format = 'https://data.gov.uk/data/dumps/' \
                           'data.gov.uk-ckan-meta-data-{date}.csv.zip'

    def _fetch(self):
        return self._fetch_data(self.facet)

    def _fetch_data(self, facet):
        url = self._build_latest_metadata_url()
        r = requests.get(url)
        response = []
        with zipfile.ZipFile(
            BytesIO(r.content)
        ).open(facet + '.csv') as fp:
            csvfile = StringIO(fp.read().decode('utf-8'))
            sample = csvfile.read(1024)
            csvfile.seek(0)

            sniffer = csv.Sniffer()
            skip_first = sniffer.has_header(sample)

            reader = csv.reader(csvfile)
            for row in reader:
                if skip_first:
                    skip_first = False
                    continue
                response.append(dict(zip(self.column_mapping.values(), row)))
            return response

    def _build_latest_metadata_url(self, date=None):
        date_str = 'latest' if (date is None) else date.strftime("%Y-%m-%d")
        return self.metadata_file_format.format(
            date=date_str
        )


class FetchAllResourcesCall(FetchAllDatasetsBaseCall):
    cache_identifier = 'resources'
    facet = 'resources'
    indices = ['name', 'date']
    column_mapping = {
        'Dataset Name': 'name',
        'URL': 'url',
        'Format': 'format',
        'Description': 'description',
        'Resource ID': 'id',
        'Position': 'position',
        'Date': 'date',
        'Organization': 'organization',
        'Top level Organization': 'top-level-organization'
    }


class FetchAllDatasetsCall(FetchAllDatasetsBaseCall):
    cache_identifier = 'datasets'
    facet = 'datasets'
    indices = ['name']
    column_mapping = {
        "Name": "name",
        "Title": "title",
        "URL": "url",
        "Organization": "organization",
        "Top level organisation": "top-level-organisation",
        "License": "license",
        "Published": "published",
        "NII": "nii",
        "Location": "location",
        "Import source": "import-source",
        "Author": "author",
        "Geographic Coverage": "geographic-coverage",
        "Isopen": "isopen",
        "License Id": "license-id",
        "Maintainer": "maintainer",
        "Mandate": "mandate",
        "Metadata Created": "metadata-created",
        "Metadata Modified": "metadata-modified",
        "Notes": "notes",
        "Odi Certificate": "odi-certificate",
        "ODI Certificate URL": "odi-certificate-url",
        "Tags": "tags",
        "Temporal Coverage From": "temporal-coverage-from",
        "Temporal Coverage To": "temporal-coverage-to",
        "Primary Theme": "primary-theme",
        "Secondary Themes": "secondary-themes",
        "Update Frequency": "update-frequency",
        "Version": "version"
    }


class FetchResourceCall(PluginCallBase):
    def _fetch(self, df, **kwargs):
        processor = plugins.find_processor(
            filetype=df['format'],
            resource_name=df['name']
        )

        def handler(cache_path):
            data = processor.deserialise(cache_path, df['id'])
            if data is not None:
                return data
            data = processor.encode(
                processor.fetch(df=df)
            )
            processor.serialise(data, cache_path, df['id'])
            return data

        return handler

    def get_cache_identifier(self, df, **kwargs):
        return 'resource_' + df['id']
