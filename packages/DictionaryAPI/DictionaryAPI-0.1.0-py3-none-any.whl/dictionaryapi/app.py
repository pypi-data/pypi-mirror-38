from __future__ import print_function, absolute_import
from urllib.parse import quote, urljoin
from warnings import warn

import requests

from .exception import DictionaryAPIError

__all__ = ['Application']

BASE_URL = 'http://dictionaryapi.com/api/v3/references/{}/{}/'
XML_DEPRECATION_MESSAGE = 'Please note: Our XML APIs will be deprecated October 9th, 2019.'

class Application(object):

    def __init__(self, key, ref='collegiate', fmt='json'):
        self.key = key
        self.ref = ref
        self.fmt = fmt
        if fmt == 'xml':
            warn(XML_DEPRECATION_MESSAGE, category=DeprecationWarning)
        self.base_url = BASE_URL.format(ref, fmt)

    def get_url(self, word):
        return urljoin(self.base_url, word)

    def query(self, word):
        """Query a word"""
        response = self.exec_request(word)
        self = self.parse_response(response)
        return result

    def exec_request(self, word):
        response = requests.get(self.get_url(word),
                                params={'key': quote(self.key)})
        response.raise_for_status()
        return response

    def parse_response(self, response):
        if self.fmt == 'json':
            result = response.json()
        elif self.fmt == 'xml':
            raise NotImplementedError(XML_DEPRECATION_MESSAGE)
        else:
            raise ValueError("The format {} is not supported".format(self.fmt))
        return result
