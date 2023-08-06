import requests

from datagovuk.cache import plugin_cache


class PluginBase(object):
    handlers = []
    extension = 'none'

    def __init__(self):
        self.encoder = None
        self.serialiser = None

    def fetch(self, df):
        return self._process(
            self.get_raw_data(df['url'])
        )

    def get_raw_data(self, url):
        return requests.get(url).content

    def _process(self, data):
        raise NotImplemented()

    def _file_name(self, cache_dir, name):
        return cache_dir / ('resource_' + name + '.' + self.extension)


class PluginCallBase(object):
    @plugin_cache()
    def __call__(self, df, *args, **kwargs):
        return self._fetch(df, **kwargs)

    def _fetch(self, df, **kwargs):
        raise NotImplemented
