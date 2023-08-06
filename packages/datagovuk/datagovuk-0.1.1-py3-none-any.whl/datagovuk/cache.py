import os
from pathlib import Path

import pandas as pd


class DataCache(object):
    def __init__(self):
        self._path = Path(os.path.join(
            os.path.expanduser('~'),
            '.cache'
        ))
        if not self._path.exists():
            self._path.mkdir(exist_ok=True)
        self._path = self._path / 'datagovuk'
        if not self._path.exists():
            self._path.mkdir(exist_ok=True)

    def __call__(self, identifier):
        cache_file = self._path / (identifier + '.parquet')

        def func_wrapper(func):
            def cache_handler(*args, **kwargs):
                return self._serialise(
                    cache_file=cache_file,
                    callback=lambda _: func(*args, **kwargs),
                )

            return cache_handler

        return func_wrapper

    def _serialise(self, cache_file, callback):
        if cache_file.exists():
            df = pd.read_parquet(cache_file)
        else:
            df = callback()
            df.to_parquet(cache_file)
        return df


class PluginCache(DataCache):
    def __call__(self):
        def func_wrapper(func):
            def cache_handler(*args, **kwargs):
                response = func(*args, **kwargs)
                return response(self._path)

            return cache_handler

        return func_wrapper


cache = DataCache()
plugin_cache = PluginCache()
