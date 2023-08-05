from tkbeacon.api_client import ApiClient
from tkbeacon.configuration import Configuration
from tkbeacon.api.beacon_api import BeaconApi

from typing import Union
from enum import Enum

class KnowledgeSource(Enum):
    RHEA = 'https://kba.ncats.io/beacon/rhea/'
    SMPDB = 'https://kba.ncats.io/beacon/smpdb/'
    SEMMED = 'https://kba.ncats.io/beacon/rkb/'
    BIOLINK = 'https://kba.ncats.io/beacon/biolink/'
    RTX = 'https://kba.ncats.io/beacon/rtx/'
    NDEX = 'https://kba.ncats.io/beacon/ndex/'
    HMDB = 'https://translator.ncats.io/hmdb-knowledge-beacon/'
    BIOTHINGS = 'https://kba.ncats.io/beacon/biothings-explorer'

def build(source:Union[KnowledgeSource, str]) -> ApiClient:
    """
    Constructs a new BeaconApi pointing at the source
    """
    host = None

    if isinstance(source, KnowledgeSource):
        host = source.value

    elif isinstance(source, str):
        for ks in KnowledgeSource:
            if source.upper() == ks.name:
                host = ks.value
        if host is None:
            host = source
    else:
        raise Exception('Unrecognized knowlege source: {}'.format(source))

    host = host.strip('/')

    configuration = Configuration()
    configuration.host = host

    api_client = ApiClient(configuration=configuration)

    return BeaconApi(api_client)

list_args = [
    'keywords',
    'categories',
    's',
    't',
    's_keywords',
    't_keywords',
    's_categories',
    't_categories'
]

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

BeaconApi = fix_methods(BeaconApi)
