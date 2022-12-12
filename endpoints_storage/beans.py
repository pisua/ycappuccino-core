import json
from urllib.parse import parse_qsl, urlsplit
from ycappuccino.storage.models.model import Model


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
                if isinstance(self._body, Model):
                    w_resp["data"]  = self._body._mongo_model
                elif isinstance(self._body, list) :
                    w_body = []
                    if len(self._body) > 0 :
                        if isinstance(self._body[0], Model):
                            for w_model in self._body:
                                w_body.append(w_model._mongo_model)
                        else:
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
        self._type = w_split_url[0][1:]

        self._is_schema = "$schema" in w_split_url
        self._is_multipart = "$multipart" in w_split_url

        self._is_empty = "$empty" in w_split_url

        if len(w_split_url)>1:
            self._item_plural_id = w_split_url[1]
            if len(w_split_url)>2:
                # an id is specified
                if self._query_param is None:
                    self._query_param = {}
                self._query_param["id"] = w_split_url[2]

    def get_type(self):
        return self._type

    def is_crud(self):
        return  not self._is_schema and not self._is_empty and not self._is_multipart

    def is_draft(self):
        return  self._query_param is not None and "draft" in self._query_param

    def get_draft(self):
        return self._query_param["draft"] if self.is_draft() else None

    def is_schema(self):
        return self._is_schema

    def is_multipart(self):
        return self._is_multipart

    def is_empty(self):
        return self._is_empty

    def get_item_plural_id(self):
        return self._item_plural_id

    def get_service_name(self):
        return self._service_name

    def get_params(self):
        return self._query_param
