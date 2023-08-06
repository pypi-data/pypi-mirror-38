import hashlib

import pandas as pd

from datagovuk.cache import cache


class BaseCall(object):
    indices = []
    column_types = {}
    cache_identifier = None
    columns = []

    def __init__(self):
        self.session = None

    def __call__(self, **kwargs):
        session = kwargs['session']
        del kwargs['session']

        @cache(self.get_cache_identifier())
        def call_hander():
            self.session = session
            response = self._fetch(**kwargs)

            df_args = {}

            if len(self.indices):
                def indexer(i):
                    return [(o[i] if i in o.keys() else '') for o in response]

                df_args['index'] = list(map(
                    indexer,
                    self.indices
                ))

            df = pd.DataFrame(
                response,
                **df_args
            )

            for col, dtype in self.column_types.items():
                df[col] = df[col].astype(dtype)

            return df

        return call_hander()

    def _fetch(self, **kwargs):
        raise NotImplemented()

    def get_cache_identifier(self):
        return hashlib.md5(self.cache_identifier.encode()).hexdigest()
