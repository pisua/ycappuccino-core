#app="all"
import json, re
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

    def __init__(self, a_method,  a_url, a_api_description):
        """ need status"""
        self._url = a_url
        w_url_no_query = a_url
        w_url_query = a_url
        self._method = a_method
        self._query_param = None
        if "?" in a_url:
            self._query_param = dict(parse_qsl(urlsplit(a_url).query))
            w_url_no_query = w_url_no_query.split("?")[0]
            w_url_query = w_url_query.split("?")[1]

        self._split_url = w_url_no_query.split("api/")[1].split("/")
        self._type = self._split_url[0][1:]
        self._is_service = "$service" in self._split_url

        if self._is_service :
            self._service_name = self._split_url[1]
        self._url_no_query = w_url_no_query.split("api/")[1]
        self._url_param = w_url_query
        if len(self.get_split_url()) > 1:
            self._item_plural_id = self.get_split_url()[1]
        # retrieve description url
        for w_path in a_api_description._body["paths"].keys():
            w_path_pattern = re.sub("\{.*\}",".*", w_path).replace("/","\/").replace("$","\$")+"$"
            if re.search(w_path_pattern,"/"+self._url_no_query):
                w_path_split = w_path[1:].split("/")
                i=0
                for w_part in w_path_split:
                    if w_part[0] == "{" and w_part[-1] == "}":
                        if self._query_param is None:
                            self._query_param = {}
                        self._query_param[w_part[1:-1]] = self.get_split_url()[i]
                    i=i+1




    def get_split_url(self):
        return self._split_url
    def get_url_no_query(self):
        return self._url_no_query

    def get_url_query(self):
        return self._url_param

    def get_method(self):
        return self._method

    def get_type(self):
        return self._type

    def is_service(self):
        return self._is_service

    def get_service_name(self):
        return self._service_name

    def get_params(self):
        return self._query_param
