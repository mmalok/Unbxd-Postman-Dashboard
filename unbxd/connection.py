"""
Connection Module

Handles put and get operations to the Bigcommerce REST API
"""
import base64
import hashlib
import hmac

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
import json  # only used for urlencode querystr
import logging
import streql

import requests

#from bigcommerce.exception import *

#log = logging.getLogger("bigcommerce.connection")


class Connection(object):
    """
    Connection class manages the connection to the Bigcommerce REST API.
    """

    def __init__(self, host,api_path='/autosuggest/{}'):
        self.host = host
        self.api_path = api_path

        self.timeout = 7.0  # need to catch timeout?

        #log.info("API Host: %s/%s" % (self.host, self.api_path))

        # set up the session
        self._session = requests.Session()
       # self._session.auth = auth
        self._session.headers = {"Accept": "application/json"}

        self._last_response = None  # for debugging

    def full_path(self, url):
        ust="http://" + self.host + self.api_path.format(url)
        return ust
    def _run_method(self, method, url, data=None, params={}):
        # make full path if not given
        if url and url[:4] != "http":
            if url[0] == '/':  # can call with /resource if you want
                url = url[1:]
            url = self.full_path(url)
        elif not url:  # blank path
            url = self.full_path(url)
        resp = getattr(self, method)(url,params)
        # mess with content
        return resp.text
        #############
        
    # CRUD methods

    def get(self, url,params={}):
        if url:
            response=requests.post(url, data=params['data'])
            return response
        
    def update(self, resource, rid, updates):
        """
        Updates the resource with id 'rid' with the given updates dictionary.
        """
        if resource[-1] != '/': resource += '/'
        resource += str(rid)
        return self.put(resource, data=updates)

    def create(self, resource, data):
        """
        Create a resource with given data dictionary.
        """
        return self.post(resource, data)

    def delete(self, url,params={} ):  # note that rid can't be 0 - problem?
        """
        Deletes the resource with given id 'rid', or all resources of given type if rid is not supplied.
        """
        if url:
            response=requests.post(url, data=params['data'])
            return response
         

    # Raw-er stuff

    def make_request(self, method, url, data=None, params = {}):
        return self._run_method(method, url, data, params)
        
    def put(self, url, params={}):
        """
        Make a PUT request to save data.
        data should be a dictionary.
        """
        if url:
            response=requests.post(url,params['data'])
            return response

    def post(self, url, data, headers={}):
        """
        POST request for creating new objects.
        data should be a dictionary.
        """
        response = self._run_method('POST', url, data=data, headers=headers)
        return self._handle_response(url, response)

