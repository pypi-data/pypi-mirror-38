from tkbeacon.api_client import ApiClient
from tkbeacon.configuration import Configuration
from tkbeacon.api.concepts_api import ConceptsApi
from tkbeacon.api.metadata_api import MetadataApi
from tkbeacon.api.statements_api import StatementsApi

from typing import Union
from enum import Enum

class KnowledgeSource(Enum):
    RHEA = 'https://kba.ncats.io/beacon/rhea/'
    SMPDB = 'https://kba.ncats.io/beacon/smpdb/'
    SEMMED = 'https://kba.ncats.io/beacon/rkb/'
    BIOLINK = 'https://kba.ncats.io/beacon/biolink/'
    RTX = 'https://kba.ncats.io/beacon/rtx/'
    NDEX = 'https://kba.ncats.io/beacon/ndex/'

class BeaconClient(ConceptsApi, StatementsApi, MetadataApi):
    """
    Derives from ConceptsApi, StatementsApi, and MetadataApi, and has all of
    their methods.
    """
    def __init__(self, source:Union[KnowledgeSource, str]):
        """
        Constructs a new BeaconClient with the basepath
        """
        if isinstance(source, KnowledgeSource):
            self.base_url = source.value
        elif isinstance(source, str):
            for ks in KnowledgeSource:
                if source.upper() == ks.name:
                    self.base_url = ks.value
            if not hasattr(self, 'base_url'):
                self.base_url = source
        else:
            raise Exception('Unrecognized knowlege source: {}'.format(source))

        configuration = Configuration()
        configuration.host = self.base_url

        self.api_client = ApiClient(configuration=configuration)
