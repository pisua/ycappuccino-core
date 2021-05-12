import json
from urllib.parse import parse_qsl, urlsplit

class EndpointResponse(object):

    def __init__(self, status, a_meta=None, a_body=None):
        """ need status"""
        self._status = status
        self._meta = a_meta
        self._body = a_body

    def get_json(self):
        return json.dumps(self.__dict__)

    def get_status(self):
        return self._status

class UrlPath(object):

    def __init__(self, a_url):
        """ need status"""
        self._url = a_url
        w_url_no_query = a_url
        self._query_param = None
        if "?" in a_url:
            self._query_param = dict(parse_qsl(urlsplit(a_url).query))
            w_url_no_query = w_url_no_query.split("?")[0]
        w_split_url = w_url_no_query.split("api/")[1].split("/")
        self._is_service = "$service" in w_split_url
        if not self._is_service :
            self._item_id = w_split_url[0]
        else :
            self._service_name = w_split_url[1]

    def is_service(self):
        return self._is_service

    def is_crud(self):
        return not self._is_service

    def get_item_id(self):
        return self._item_id

    def get_service_name(self):
        return self._service_name

    def get_params(self):
        return self._query_param
