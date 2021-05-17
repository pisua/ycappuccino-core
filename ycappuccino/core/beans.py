import json
from urllib.parse import parse_qsl, urlsplit
from ycappuccino.core.model.model import Model
from ycappuccino.core.model.utils import YDict
class EndpointResponse(object):

    def __init__(self, status, a_meta=None, a_body=None):
        """ need status"""
        self._status = status
        self._meta = a_meta
        self._body = a_body

    def get_json(self):
        w_resp = YDict({
            "data": self._body,
            "status": self._status,
            "meta": self._meta
        })
        if isinstance(w_resp.data, Model):
            w_resp.data = w_resp.data.__dict__
        elif isinstance(w_resp.data, list) and len(w_resp.data) > 0 and isinstance(w_resp.data[0], Model):
            w_body = []
            for w_model in w_resp.data:
                w_body.append(w_model.__dict__)
            w_resp.data = w_body
        return json.dumps(w_resp.__dict__)

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
            if len(w_split_url)>1:
                # an id is specified
                if self._query_param is None:
                    self._query_param = {}
                self._query_param["id"] = w_split_url[1]
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
