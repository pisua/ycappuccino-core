#app="all"
import json
from urllib.parse import parse_qsl, urlsplit
from ycappuccino.storage.models.model import Model
import ycappuccino.endpoints.beans


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

class UrlPath(ycappuccino.endpoints.beans.UrlPath):

    def __init__(self, a_method , a_url, a_api_description):
        """ need status"""
        super().__init__(a_method, a_url, a_api_description)


        self._is_schema = "$schema" in self.get_split_url()
        self._is_multipart = "$multipart" in self.get_split_url()

        self._is_empty = "$empty" in self.get_split_url()





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



