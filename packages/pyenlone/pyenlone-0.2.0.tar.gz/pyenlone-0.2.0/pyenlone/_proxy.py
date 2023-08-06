""" Proxies do the actual API requests. """
from abc import ABC, abstractmethod

import requests
from requests_cache import CachedSession

from .enloneexception import EnlOneException


class EnlOneApiErrorException(EnlOneException):
    pass


class EnlOneConnectionException(EnlOneException):
    pass


def api_result(response):
    # from pprint import pprint; pprint(response)
    if not response:
        raise EnlOneConnectionException(response.text)
    if "status" in response.json() and response.json()["status"] == "error":
        raise EnlOneApiErrorException(response.json()["message"])
    # from pprint import pprint; pprint(response.json())
    if "data" in response.json():
        return response.json()["data"]
    else:
        return response.json()


class Proxy(ABC):
    """
    Proxy interface.
    """
    @abstractmethod
    def get(self, endpoint, params): pass

    @abstractmethod
    def post(self, endpoint, json): pass

    @abstractmethod
    def delete(self, endpoint, json): pass

    @abstractmethod
    def put(self, endpoint, json): pass


class KeyProxy(Proxy):
    """
    Proxy implementation for authentication using API keys.
    """
    def __init__(self, base_url, apikey, cache=0):
        self._apikey = apikey
        self._base_url = base_url
        self._session = CachedSession(expire_after=cache)

    def get(self, endpoint, params={}):
        """
        Do a get request adding the apikey as a parameter.
        """
        url = self._base_url + endpoint
        params["apikey"] = self._apikey
        try:
            response = self._session.get(url, params=params)
        except requests.exceptions.RequestException:
            raise EnlOneException("Error contacting enl.one servers.")
        return api_result(response)

    def post(self, endpoint, json):
        """
        Do a post request adding the apikey as a parameter.
        """
        url = self._base_url + endpoint
        try:
            response = self._session.post(url,
                                          params={"apikey": self._apikey},
                                          json=json)
        except requests.exceptions.RequestException:
            raise EnlOneException("Error contacting enl.one servers.")
        return api_result(response)

    def put(self, endpoint, json):
        """
        Do a put request adding the apikey as a parameter.
        """
        url = self._base_url + endpoint
        try:
            response = self._session.put(url,
                                         params={"apikey": self._apikey},
                                         json=json)
        except requests.exceptions.RequestException:
            raise EnlOneException("Error contacting enl.one servers.")
        return api_result(response)

    def delete(self, endpoint, json={}):
        """
        Do a delete request adding the apikey as a parameter.
        """
        url = self._base_url + endpoint
        try:
            response = self._session.delete(url,
                                            params={"apikey": self._apikey},
                                            json=json)
        except requests.exceptions.RequestException:
            raise EnlOneException("Error contacting enl.one servers.")
        return api_result(response)


class TokenProxy(Proxy):
    """
    Proxy implementation for authentication using OAuth tokens.
    """
    def __init__(self, base_url, token, cache=0):
        self._token = token
        self._base_url = base_url
        self._session = CachedSession(expire_after=cache)

    def get(self, endpoint, params={}):
        """
        Do a get request adding the Authorization header.
        """
        url = self._base_url + endpoint
        headers = {'Authorization': self._token}
        try:
            response = self._session.get(url, headers=headers, params=params)
        except requests.exceptions.RequestException:
            raise EnlOneException("Error contacting enl.one servers.")
        return api_result(response)

    def post(self, endpoint, json):
        """
        Do a get request adding the Authorization header.
        """
        url = self._base_url + endpoint
        headers = {'Authorization': self._token}
        try:
            response = self._session.post(url, headers=headers, json=json)
        except requests.exceptions.RequestException:
            raise EnlOneException("Error contacting enl.one servers.")
        return api_result(response)

    def put(self, endpoint, json):
        """
        Do a get request adding the Authorization header.
        """
        url = self._base_url + endpoint
        headers = {'Authorization': self._token}
        try:
            response = self._session.put(url, headers=headers, json=json)
        except requests.exceptions.RequestException:
            raise EnlOneException("Error contacting enl.one servers.")
        return api_result(response)

    def delete(self, endpoint, json={}):
        """
        Do a get request adding the Authorization header.
        """
        url = self._base_url + endpoint
        headers = {'Authorization': self._token}
        try:
            response = self._session.delete(url, headers=headers, json=json)
        except requests.exceptions.RequestException:
            raise EnlOneException("Error contacting enl.one servers.")
        return api_result(response)


class OpenProxy:
    """
    Proxy implementation for the open API.
    """
    def __init__(self, cache=0):
        self._session = CachedSession(expire_after=cache)

    def get(self, endpoint):
        """
        Do a get request with no auth.
        """
        url = "https://v.enl.one/OpenApi" + endpoint
        try:
            response = self._session.get(url)
        except requests.exceptions.RequestException:
            raise EnlOneException("Error contacting enl.one servers.")
        return api_result(response)
