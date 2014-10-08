from requests.auth import HTTPBasicAuth
import logging
import requests


class Client(object):
    ENDPOINTS = {
        'live': 'https://ws.bluesnap.com',
        'sandbox': 'https://sandbox.bluesnap.com'
    }

    def __init__(self,
                 # Environment
                 env,
                 # Authentication
                 username, password,
                 # Default store Id
                 default_store_id):
        if env not in self.ENDPOINTS:
            raise ValueError('env not in {0}'.format(self.ENDPOINTS.keys()))

        self.env = env
        self.username = username
        self.password = password
        self.default_store_id = default_store_id

    @property
    def endpoint_url(self):
        return self.ENDPOINTS[self.env]

    @property
    def http_basic_auth(self):
        return HTTPBasicAuth(self.username, self.password)

    def request(self, method, path, data=None):
        headers = {
            'content-type': 'application/xml',
        }

        url = self.endpoint_url + path

        r = requests.request(method, url,
                             headers=headers,
                             auth=self.http_basic_auth,
                             data=data)

        return r


__client__ = None


def default():
    """:rtype : Client"""
    global __client__

    if __client__ is None:
        # TODO refactor
        __client__ = Client(
            env='sandbox',
            username='test',
            password='password',
            default_store_id='100'
        )

    return __client__


def configure(**config):
    """:rtype : Client"""
    global __client__
    __client__ = Client(**config)
    return __client__
