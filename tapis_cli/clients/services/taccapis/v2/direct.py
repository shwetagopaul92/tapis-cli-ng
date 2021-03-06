# from tapis_cli.main import PKG_NAME, About, VersionInfo
import requests
import curlify
from requests.auth import HTTPBasicAuth
from agavepy.agave import Agave
from tapis_cli.utils import print_stderr
from tapis_cli.settings import TAPIS_CLI_SHOW_CURL, TAPIS_CLI_VERBOSE_ERRORS
from tapis_cli.user_agent import user_agent

__all__ = ['TaccApiDirectClient']


class TaccApiDirectClient(object):
    """Requests client bootstrapped from a Tapis API client

    The intended use is to implement methods not expressed by the
    current Swagger spec and which are thus not accessible in
    AgavePy. Examples include the 'search' function, which relies
    on encoding a POST form of search terms into a GET request. The
    web request is made directly using the ``requests`` library.
    """
    def __init__(self, agave_client):
        # TODO - Catch when client is missing properties
        # token = agave_client.token.token_info['access_token']
        # Always refresh when using a requests call
        # agave_client.token.refresh()
        token = agave_client._token
        self.user_agent = user_agent()
        self.api_server = agave_client.api_server
        self.api_key = agave_client.api_key
        self.api_secret = agave_client.api_secret
        self.service_name = None
        self.service_version = None
        self.api_path = None
        self.headers = {
            'authorization': 'Bearer {}'.format(token),
            'user-agent': self.user_agent
        }

    def setup(self, service_name, service_version, api_path=None):
        setattr(self, 'service_version', service_version)
        setattr(self, 'service_name', service_name)
        setattr(self, 'api_path', api_path)

    def build_url(self, *args):
        arg_els = args
        path_els = [self.service_name, self.service_version, self.api_path]
        path_els.extend(arg_els)
        # TODO - Filter for leading slashes in path_els
        # TODO - Strip trailing slash from api_server
        url_path_els = [self.api_server]
        url_path_els.extend(path_els)
        url_path_els = [u for u in url_path_els if u is not None]
        return '/'.join(url_path_els)

    def get(self, path=None):
        url = self.build_url(path)
        resp = requests.get(url, headers=self.headers)
        show_curl(resp)
        resp = self._raise_for_status(resp)
        #        resp.raise_for_status()
        return resp.json().get('result', {})

    def delete(self, path=None):
        url = self.build_url(path)
        resp = requests.delete(url, headers=self.headers)
        show_curl(resp)
        resp = self._raise_for_status(resp)
        #        resp.raise_for_status()
        return resp.json().get('result', {})

    def get_bytes(self, path=None):
        url = self.build_url(path)
        resp = requests.get(url, headers=self.headers)
        show_curl(resp)
        resp = self._raise_for_status(resp)
        #        resp.raise_for_status()
        return resp

    def get_data(self, path=None, params={}):
        url = self.build_url(path)
        resp = requests.get(url, headers=self.headers, params=params)
        show_curl(resp)
        resp = self._raise_for_status(resp)
        #        resp.raise_for_status()
        return resp.json().get('result', {})

    def post(self, path=None, content_type=None):
        url = self.build_url(path)
        post_headers = self.headers
        if content_type is not None:
            post_headers['Content-type'] = content_type
        resp = requests.post(url, headers=post_headers)
        show_curl(resp)
        resp = self._raise_for_status(resp)
        #        resp.raise_for_status()
        return resp.json().get('result', {})

    def post_data_basic(self,
                        data=None,
                        auth=None,
                        path=None,
                        content_type=None):
        url = self.build_url(path)
        post_headers = {'user-agent': self.user_agent}
        if content_type is not None:
            post_headers['Content-type'] = content_type
        if auth is None:
            auth = (self.api_key, self.api_secret)

        resp = requests.post(url, headers=post_headers, auth=auth, data=data)
        show_curl(resp)

        resp = self._raise_for_status(resp)
        #        resp.raise_for_status()
        return resp.json()

    def _raise_for_status(self, resp):
        """Handler for requests raise_for_status to capture message from API server responses
        """
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as h:
            if TAPIS_CLI_VERBOSE_ERRORS:
                # Extract the API JSON message and attach it
                # to the HTTPError object before raising it
                code = h.response.status_code
                reason = h.response.reason + ' for ' + h.response.url
                try:
                    message = h.response.json().get('message')
                except Exception:
                    message = h.response.text
                raise requests.exceptions.HTTPError(code,
                                                    reason,
                                                    message,
                                                    response=h.response,
                                                    request=h.request)
            else:
                raise h
        return resp


def show_curl(response_object):
    if TAPIS_CLI_SHOW_CURL:
        try:
            curl_text = curlify.to_curl(response_object.request)
        except Exception as err:
            curl_text = 'Failed to render curl command: {0}'.format(err)
        print_stderr(curl_text)
