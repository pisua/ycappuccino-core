from ycappuccino.core.api import IEndpoint, IActivityLogger, IJwt, IManager, IService, IProxyManager
import uuid
import pelix.http
import pelix.remote
import logging
import json
from ycappuccino.core.beans import UrlPath, EndpointResponse
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, BindField, UnbindField, Instantiate, Property
import ycappuccino.core.model.decorators

_logger = logging.getLogger(__name__)


@ComponentFactory('Endpoint-Factory')
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_jwt",IJwt.name)
@Provides(specifications=[pelix.http.HTTP_SERVLET])
@Instantiate("endpoints")
@Requires("_managers", specification=IManager.name, aggregate=True, optional=True)
@Requires("_services", specification=IService.name, aggregate=True, optional=True)
@Property("_servlet_path", pelix.http.HTTP_SERVLET_PATH, "/api")
@Property("_reject", pelix.remote.PROP_EXPORT_REJECT, pelix.http.HTTP_SERVLET)
class Endpoint(IEndpoint):

    def __init__(self):
        super(IEndpoint, self).__init__();
        self._log = None
        self._managers = None
        self._map_managers = {}

        self._services = None
        self._map_services = {}

    def do_GET(self, request, response):
        """  """
        w_path = request.get_path()
        w_header = request.get_headers()

        if "swagger.json" in w_path:
            w_resp = self.get_swagger_descriptions(["https","http"])
        else:
            w_resp = self.get(w_path, w_header)
        response.send_content(w_resp.get_status(), w_resp.get_json(), "application/json")

    def do_POST(self, request, response):
        """ """
        w_str = request.read_data().decode()
        w_path = request.get_path()
        w_header = request.get_headers()
        w_json = json.loads(w_str)

        w_resp = self.post(w_path, w_header, w_json)
        for key, value in w_resp.get_header().items():
            response.set_header(key, value)

        response.send_content(w_resp.get_status(), w_resp.get_json(), "application/json")

    def do_PUT(self, request, response):
        """ """
        w_str = request.read_data().decode()
        w_path = request.get_path()
        w_header = request.get_headers()
        w_json = json.loads(w_str)

        w_resp = self.put(w_path, w_header, w_json)
        response.send_content(w_resp.get_status(), w_resp.get_json(), "application/json")

    def do_DELETE(self, request, response):
        """ """
        w_path = request.get_path()
        w_header = request.get_headers()

        w_resp = self.delete(w_path, w_header)
        response.send_content(w_resp.get_status(), w_resp.get_json(), "application/json")

    def check_header(self, a_headers):
        if "authorization" in a_headers:
            w_authorization = a_headers["authorization"]
            if w_authorization is not None and "Bearer" in w_authorization:
                w_token = w_authorization[len("Bearer "):]
                return self._jwt.verify(w_token)
            else:
                return False
        elif "Cookie" in a_headers:
            w_cookies = a_headers["Cookie"]
            if ";" in w_cookies:
                w_arr = w_cookies.split(";")
                for w_cookie in w_arr:
                    if "_ycappuccino" in w_cookie:
                        w_token = w_cookie.split("=")[1]
                        return self._jwt.verify(w_token)
                return False

    def find_service(self, a_service_name):
        if a_service_name not in self._map_services:
            # reset map of manager (TODO check why bind doesn't work)
            return None
        return self._map_services[a_service_name]

    def find_manager(self, a_item_plural_id):
        if a_item_plural_id in self._map_managers:
             return self._map_managers[a_item_plural_id]

        return None

    def post(self,a_path, a_headers, a_body):
        w_url_path = UrlPath(a_path)
        if w_url_path.is_crud():
            w_item_plural = w_url_path.get_item_plural_id()
            w_manager = self.find_manager(w_item_plural)
            if w_manager is not None:
                w_item = w_manager.get_item_from_id_plural(w_item_plural)
                if w_item["secureWrite"] and not self.check_header(a_headers):
                    return EndpointResponse(401)
                w_id = str(uuid.uuid4())
                w_manager.up_sert(w_item.id, w_id, a_body)
                w_meta = {
                    "type": "array"
                }
                return EndpointResponse(201, None, w_meta, {"id":w_id})
            else:
                return EndpointResponse(405)
        elif w_url_path.is_schema():
            return EndpointResponse(501)
        elif w_url_path.is_service():
            w_service_name = w_url_path.get_service_name()
            w_service = self.find_service(w_service_name)
            if w_service is not None:
                w_header, w_body = w_service.post(a_headers, w_url_path.get_params(), a_body)
                w_meta = {
                    "type": "array"
                }
                if w_body is None:
                    return EndpointResponse(401)
                else:
                    return EndpointResponse(200, w_header, w_meta, w_body)
            return EndpointResponse(501)
        return EndpointResponse(400)

    def put(self, a_path, a_headers, a_body):
        w_url_path = UrlPath(a_path)
        if w_url_path.is_crud():
            w_item_plural = w_url_path.get_item_plural_id()
            w_manager = self.find_manager(w_item_plural)
            if w_manager is not None:
                w_item = w_manager.get_item_from_id_plural(w_item_plural)

                if w_item["secureWrite"] and not self.check_header(a_headers):
                    return EndpointResponse(401)
                if w_url_path.get_params() is not None and w_url_path.get_params()["id"] is not None:
                    w_id = w_url_path.get_params()["id"]
                    w_manager.up_sert(w_item.id, w_id, a_body)
                    w_meta = {
                        "type": "array",
                        "size": 1
                    }
                    return EndpointResponse(200, None, w_meta, {"id":w_id})
            else:
                return EndpointResponse(405)
        elif w_url_path.is_schema():
            return EndpointResponse(501)
        elif w_url_path.is_service():
            w_service_name = w_url_path.get_service_name()
            w_service = self.find_services(w_service_name)
            if w_service is not None:
                w_header, w_body = w_service.put(a_headers, w_url_path.get_params(), a_body)
                w_meta = {
                    "type": "array"
                }
                return EndpointResponse(200, w_header, w_meta, w_body)
            return EndpointResponse(501)

        return EndpointResponse(400)

    def get_swagger_description_tag(self, a_item):
        return a_item["app"]+" "+a_item["plural"]

    def get_swagger_description_service_tag(self,a_service):
        return "$service "+a_service.get_name()

    def get_swagger_description_path(self, a_item, a_with_id):
        """ query can be get, getAll, put, post and delete """
        w_path = "/"+a_item["plural"]
        if a_with_id:
            w_path =  w_path+"/{id}"
        return w_path

    def get_swagger_description_empty(self, a_item,a_path):
        """ return the path description for the item"""
        a_path["/"+a_item["plural"]+"/$empty"] = {
            "get": {
                "tags": [self.get_swagger_description_tag(a_item)],
                "operationId": "empty_" + a_item["plural"],
                "consumes": ["application/json"],
                "produces": ["application/json"],
                "parameters": [],
                "responses": {
                    "default": {
                        "description": "successful operation"
                    }
                }
            }
        }

    def get_swagger_description_schema(self, a_item,a_path):
        """ return the path description for the item"""
        a_path["/"+a_item["plural"]+"/$schema"] = {
            "get": {
                "tags": [self.get_swagger_description_tag(a_item)],
                "operationId": "schema_" + a_item["plural"],
                "consumes": ["application/json"],
                "produces": ["application/json"],
                "parameters": [],
                "responses": {
                    "default": {
                        "description": "successful operation"
                    }
                }
            }
        }


    def get_swagger_description_service(self, a_service, a_path):
        """ return the path description for the item"""
        a_path["/$service/"+a_service.get_name()]={
            "post": {
                "tags": [self.get_swagger_description_service_tag(a_service)],
                "operationId": "service_"+a_service.get_name(),
                "consumes": ["application/json"],
                "produces": ["application/json"],
                "parameters": [{
                    "in": "body",
                    "name": "body",
                    "required": True,
                    "schema": {
                        "type": "string"
                    }
                }],
                "responses": {
                    "default": {
                        "description": "successful operation"
                    }
                }
            }
        }

        return a_path


    def get_swagger_description(self, a_item, a_path):
        """ return the path description for the item"""
        a_path[self.get_swagger_description_path(a_item, False)]={
            "get": {
                "tags": [self.get_swagger_description_tag(a_item)],
                "operationId": "getAll_"+a_item["id"],
                "produces": ["application/json"],
                "parameters": [{
                    "name": "filter",
                    "in": "query",
                    "required": False,
                    "type": "string"
                },{
                    "name": "offset",
                    "in": "query",
                    "required": False,
                    "type": "integer",
                    "default": 0,
                    "format": "int32"
                }, {
                    "name": "limit",
                    "in": "query",
                    "required": False,
                    "type": "integer",
                    "default": 50,
                    "format": "int32"
                },{
                    "name": "sort",
                    "in": "query",
                    "required": False,
                    "type": "string"
                }],
                "responses": {
                    "default": {
                        "description": "successful operation"
                    }
                }
            },
            "post": {
                "tags": [self.get_swagger_description_tag(a_item)],
                "operationId": "create_"+a_item["id"],
                "consumes": ["application/json"],
                "produces": ["application/json"],
                "parameters": [{
                    "in": "body",
                    "name": "body",
                    "required": True,
                    "schema": {
                        "type": "string"
                    }
                }, {
                    "name": "filter",
                    "in": "query",
                    "required": True,
                    "type": "string"
                }],
                "responses": {
                    "default": {
                        "description": "successful operation"
                    }
                }
            }
        }
        a_path[self.get_swagger_description_path(a_item, True)] = {
            "get": {
                "tags": [self.get_swagger_description_tag(a_item)],
                "operationId": "getItem_"+a_item["id"],
                "produces": ["application/json"],
                "parameters": [{
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "type": "string"
                }],
                "responses": {
                    "default": {
                        "description": "successful operation"
                    }
                }
            },
            "put": {
                "tags": [self.get_swagger_description_tag(a_item)],
                "operationId": "update_"+a_item["id"],
                "consumes": ["application/json"],
                "produces": ["application/json"],
                "parameters": [{
                    "in": "body",
                    "name": "body",
                    "required": True,
                    "schema": {
                        "type": "string"
                    }
                }, {
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "type": "string"
                }],
                "responses": {
                    "default": {
                        "description": "successful operation"
                    }
                }
            }
        }
        self.get_swagger_description_empty(a_item,a_path)
        self.get_swagger_description_schema(a_item,a_path)

        return a_path

    def get_swagger_descriptions(self, a_scheme):
        w_path = {}
        w_tag = []
        w_swagger = {
            "swagger":"2.0",
            "info":{},
            "basePath":"/api/",
            "tags":w_tag,
            "schemes": a_scheme,
            "paths":w_path
        }
        for w_item in ycappuccino.core.model.decorators.get_map_items():
            if not w_item["abstract"]:
                self.get_swagger_description(w_item, w_swagger["paths"])
                w_tag.append({"name":self.get_swagger_description_tag(w_item)})

        for w_service in self._map_services.values():
            self.get_swagger_description_service(w_service, w_swagger["paths"])
            w_tag.append({"name": self.get_swagger_description_service_tag(w_service)})
        return EndpointResponse(200, None, None, w_swagger)

    def get(self, a_path, a_headers):
        w_url_path = UrlPath(a_path)
        if w_url_path.is_crud():
            w_item_plural = w_url_path.get_item_plural_id()
            w_manager = self.find_manager(w_item_plural)
            if w_manager is not None:
                w_item = w_manager.get_item_from_id_plural(w_item_plural)

                if w_item["secureRead"] and not self.check_header(a_headers):
                    return EndpointResponse(401)
                if w_url_path.get_params() is not None and "id" in w_url_path.get_params():
                    w_resp = w_manager.get_one(w_item["id"], w_url_path.get_params()["id"])
                    w_meta = {
                        "type": "object",
                        "size": 1
                    }
                else:

                    w_resp = w_manager.get_many(w_item["id"],w_url_path.get_params())
                    w_meta = {
                        "type": "array",
                        "size": len(w_resp)
                    }
                return EndpointResponse(200, None, w_meta, w_resp)
            else:
                return EndpointResponse(405)
        elif w_url_path.is_schema():
            w_item_plural = w_url_path.get_item_plural_id()

            w_manager = self.find_manager(w_item_plural)
            if w_manager is not None:
                w_item = w_manager.get_item_from_id_plural(w_item_plural)

                w_resp = w_manager.get_schema(w_item["id"])
                w_meta = {
                    "type": "object",
                    "size": 1
                }
                return EndpointResponse(200, w_meta, w_resp)
        elif w_url_path.is_service():
            w_service_name = w_url_path.get_service_name()
            w_service = self.find_services(w_service_name)
            if w_service is not None:
                w_header, w_body = w_service.get(a_headers, w_url_path.get_params(), a_body)
                w_meta = {
                    "type": "array"
                }
                return EndpointResponse(200, w_header,  w_meta, w_body)
            return EndpointResponse(501)
        elif w_url_path.is_empty():
            w_item_plural = w_url_path.get_item_plural_id()
            w_manager = self.find_manager(w_item_plural)
            if w_manager is not None:
                w_item = w_manager.get_item_from_id_plural(w_item_plural)

                w_resp = w_manager.get_empty(w_item["id"])
                w_meta = {
                    "type": "object",
                    "size": 1
                }
                return EndpointResponse(200, w_meta, w_resp)
            return EndpointResponse(501)
        return EndpointResponse(400)

    def delete(self, a_path, a_headers):
        w_url_path = UrlPath(a_path)
        if w_url_path.is_crud():
            w_item_plural = w_url_path.get_item_plural_id()
            w_manager = self.find_manager(w_item_plural)
            if w_manager is not None:
                w_item = w_manager.get_item_from_id_plural(w_item_plural)
                if w_item.secureWrite and not self.check_header(a_headers):
                    return EndpointResponse(401)
                w_meta = {
                    "type": "array",
                    "size": 1
                }
                if w_url_path.get_params() is not None and w_url_path.get_params().id is not None:
                    w_manager.delete(w_item["id"], w_url_path.get_params().id)
                    return EndpointResponse(200, None, w_meta)
            else:
                return EndpointResponse(405)
        elif w_url_path.is_schema():
            return EndpointResponse(501)
        elif w_url_path.is_service():
            w_service_name = w_url_path.get_service_name()
            w_service = self.find_services(w_service_name)
            if w_service is not None:
                w_header, w_body =  w_service.delete(a_headers, w_url_path.get_params())
                w_meta = {
                    "type": "array"
                }
                return EndpointResponse(200,w_header, w_meta, w_body)
            return EndpointResponse(501)
        return EndpointResponse(400)

    @BindField("_managers")
    def bind_manager(self, field, a_manager, a_service_reference):
        w_item_plurals = a_manager.get_item_ids_plural()
        for w_item_plural in w_item_plurals:
            self._map_managers[w_item_plural] = a_manager

    @UnbindField("_managers")
    def unbind_manager(self, field, a_manager, a_service_reference):
        w_item_plurals = a_manager.get_item_ids_plural()
        for w_item_plural in w_item_plurals:
            self._map_managers[w_item_plural] = None


    @BindField("_services")
    def bind_services(self, field, a_service, a_service_reference):
        w_service = a_service.get_name()
        self._map_services[w_service] = a_service

    @UnbindField("_services")
    def unbind_services(self, field, a_service, a_service_reference):
        w_service = a_service.get_name()
        self._map_services[w_service] = None


    @Validate
    def validate(self, context):
        _logger.info("Endpoint validating")

        _logger.info("Endpoint validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("Endpoint invalidating")

        _logger.info("Endpoint invalidated")
