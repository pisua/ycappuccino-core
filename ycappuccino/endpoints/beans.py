import json
from urllib.parse import parse_qsl, urlsplit


class EndpointResponse(object):

    def __init__(self, status,a_header=None, a_meta=None, a_body=None):
        """ need status"""
        self._status = status
        self._meta = a_meta
        self._header = a_header
        self._body = a_body

    def get_header(self):
        return self._header

    def get_json(self):
        if self._meta is None:
            return json.dumps(self._body)
        else:
            w_resp = {
                "status": self._status,
                "meta": self._meta,
                "data": None
            }
            if self._body is not None:
                if isinstance(self._body, dict):
                    w_resp["data"] = self._body
                elif isinstance(self._body, list) :
                    w_body = []
                    if len(self._body) > 0 :
                        for w_json in self._body:
                            w_body.append(w_json)
                    w_resp["data"] = w_body
            else:
                if w_resp["meta"]["type"] == "array":
                    w_resp["data"] = []
                else:
                    w_resp["data"] = {}

            return json.dumps(w_resp)

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
        self._type = w_split_url[0]
        self._is_service = "$service" in w_split_url

        if self._is_service :
            self._service_name = w_split_url[1]

    def get_type(self):
        return self._type

    def is_service(self):
        return self._is_service

    def get_service_name(self):
        return self._service_name

    def get_params(self):
        return self._query_param
