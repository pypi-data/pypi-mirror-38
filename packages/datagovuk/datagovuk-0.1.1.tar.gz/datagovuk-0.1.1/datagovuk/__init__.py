from ckanapi import RemoteCKAN

from datagovuk.cache import DataCache
from datagovuk.calls.datasets import FetchAllDatasetsBaseCall, FetchAllDatasetsCall, FetchAllResourcesCall, \
    FetchResourceCall
from datagovuk.calls.organisations import FetchAllOrganisationsCall, FetchOrganisationGroupsCall, \
    FetchOrganisationStructureCall, FetchOrganisationUsersCall


class Api(RemoteCKAN):
    ENDPOINT = 'https://data.gov.uk/'

    DEFAULT = None

    def __init__(self):
        super().__init__(
            address=self.ENDPOINT
        )
        if Api.DEFAULT is None:
            Api.DEFAULT = self

    def session_wrapper(self, func):
        def default_session_handler(*args, **kwargs):
            if 'session' not in kwargs:
                kwargs['session'] = self.DEFAULT
            return func(*args, **kwargs)

        return default_session_handler


client = Api()

# Organisations
organisation_structure = client.session_wrapper(FetchOrganisationStructureCall())
organisations_users = client.session_wrapper(FetchOrganisationUsersCall())
organisations_groups = client.session_wrapper(FetchOrganisationGroupsCall())
organisations = client.session_wrapper(FetchAllOrganisationsCall())

# Datasets

resources = client.session_wrapper(FetchAllResourcesCall())
datasets = client.session_wrapper(FetchAllDatasetsCall())

# Retrieve resources
resource = client.session_wrapper(FetchResourceCall())

# try:
#     __IPYTHON__
#     IPY = True
# except NameError:
#     IPY = False
