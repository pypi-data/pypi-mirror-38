import requests
import urlparse
from requests.auth import HTTPBasicAuth

class SpinnakerClient(object):

    def __init__(self, server, username=None, password=None):
        self.init = True
        self.server = server
        self.username = username
        self.password = password

    def _do_request(self, method, path, params=None, data=None):
        if method in ('GET','Get','get'):
            r = requests.get(urlparse.urljoin(self.server, path), auth=HTTPBasicAuth(self.username, self.password))
        r.raise_for_status()
        return r.json()

    def get_application(self, application):
        return self._do_request('GET', '/applications/%s' % application)

    def get_applications(self):
        return self._do_request('GET', '/applications')

