# _*_ coding: utf-8 _*_
__author__ = 'luoli'
import abc
import AuthModule


class AcsRequest:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._query_params = {}
        self._header_params = {}
        self._add_request_params = {}
        self._uri_params = {}
        self.__uri = None

    def get_query_params(self):
        return self._query_params

    def add_header_params(self, k, v):
        if self._header_params is None:
            self._header_params = {}
        else:
            self._header_params[k] = v

    def add_request_params(self, k, v):
        if self._add_request_params is None:
            self._add_request_params = {}
        else:
            self._header_params[k] = v

    def get_header_params(self):
        return self._header_params

    def get_uri_params(self):
        return self._uri_params

    def get_uri(self):
        uid = self._uri_params['uid']
        item = self._uri_params['item']
        uri = '/json-api/v1/metricdata/%s/BCE_BCC/%s' % (uid, item)
        return uri


class IqiyiOpRequest(AcsRequest):
    def __init__(self, endpoint):
        AcsRequest.__init__(self)
        self.add_header_params('Content-Type', 'application/json')
        self.add_header_params('Expect', '100-continue')
        self.add_header_params('Host', endpoint)
        # self.add_request_params('method', 'GET')

    def add_query_params(self, k, v):
        if self._query_params is None:
            self._query_params = {}
        else:
            self._query_params[k] = v

    def add_uri_params(self, k, v):
        if self._uri_params is None:
            self._uri_params = {}
        else:
            self._uri_params[k] = v

    def set_auth_params(self, auth):
        self.add_header_params('Authorization', auth)

    def get_auth_params(self):
        self.get_header_params().get('Authorization')



