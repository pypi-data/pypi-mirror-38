# _*_ coding: utf-8 _*_
__author__ = 'luoli'
import AuthModule
import QueryBccMetric
import requests


class AcsClient:

    def __init__(self,
                 ak=None,
                 sk=None,
                 uid=None,
                 endpoint=None,
                 request=None,
                 real_header=None
                 ):

        self.__ak = ak
        self.__sk = sk
        self.__uid = uid
        self.__endpoint = endpoint
        self._singer = AuthModule.BceSigner(ak, sk)
        self.__uri = QueryBccMetric.IqiyiOpRequest.get_uri(request)
        self.__params = QueryBccMetric.IqiyiOpRequest.get_query_params(request)
        self.__header = QueryBccMetric.IqiyiOpRequest.get_header_params(request)
        self.__request = request
        self.__real_header = real_header

    def get_ak(self):
        return self.__ak

    def get_sk(self):
        return self.__sk

    def get_uid(self):
        return self.__uid

    def get_endpoint(self):
        return self.__endpoint

    def get_singer(self):
        return self._singer

    def get_params(self):
        return self.__params

    def get_headers(self):
        return self.__header

    def get_uri(self):
        return self.__uri

    def get_auth(self):
        auth_request = {'method': 'GET',
                        'uri': self.__uri,
                        'params': self.__params,
                        'headers': self.__header}
        auth_params = self._singer.gen_authorization(auth_request)
        self.__request.set_auth_params(auth_params)
        return self.__header

    def get_url(self):
        return 'http://' + str(self.__endpoint) + str(self.__uri)

    def do_action(self):
        url = self.get_url()
        headers = self.get_auth()
        params = self.get_params()
        resp = requests.get(url, headers=headers, params=params)
        return resp.json()




