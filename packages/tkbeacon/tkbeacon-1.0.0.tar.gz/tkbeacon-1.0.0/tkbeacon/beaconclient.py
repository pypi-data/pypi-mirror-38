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

list_args = ['keywords', 'categories', 's', 't', 's_keywords', 't_keywords', 's_categories', 't_categories']

def signature_fix_decorator(method):
    def wrapper(*vargs, **kwargs):
        for arg in list_args:
            if arg in kwargs:
                if isinstance(kwargs[arg], str):
                    kwargs[arg] = [kwargs[arg]]
                elif not isinstance(kwargs[arg], list):
                    raise Exception('{} argument {} must be a list'.format(method.__name__, arg))

        return method(*vargs, **kwargs)
    return wrapper

def fix_methods(cls):
    for method_name in dir(cls):
        if method_name.startswith('get_') and not method_name.endswith('_with_http_info'):
            method = getattr(cls, method_name)
            setattr(cls, method_name, signature_fix_decorator(method))
    return cls

BeaconClient = fix_methods(BeaconClient)
