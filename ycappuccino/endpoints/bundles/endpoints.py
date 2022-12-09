from ycappuccino.core.api import  IActivityLogger,   IService, IProxyManager
from ycappuccino.endpoints.api import IEndpoint, IHandlerEndpoint,  IJwt

import pelix.http
import os
import pelix.remote
import logging
import json
from ycappuccino.endpoints.beans import UrlPath, EndpointResponse
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, BindField, UnbindField, Instantiate, Property
from ycappuccino.endpoints.bundles import util_swagger

_logger = logging.getLogger(__name__)




@ComponentFactory('Endpoint-Factory')
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_jwt",IJwt.name)
@Provides(specifications=[pelix.http.HTTP_SERVLET])
@Instantiate("endpoints")
@Requires("_handler_endpoints", specification=IHandlerEndpoint.name, aggregate=True, optional=True)
@Requires("_services", specification=IService.name, aggregate=True, optional=True)
@Property("_servlet_path", pelix.http.HTTP_SERVLET_PATH, "/api")
@Property("_reject", pelix.remote.PROP_EXPORT_REJECT, pelix.http.HTTP_SERVLET)
class Endpoint(IEndpoint):

    def __init__(self):
        super(IEndpoint, self).__init__();
        self._log = None
        self._handler_endpoints = None
        self._map_handler_endpoints = {}
        self._services = None
        self._map_services = {}
        self._file_dir = None

    def do_GET(self, request, response):
        """  """
        w_path = request.get_path()
        w_header = request.get_headers()
        _logger.info("get path={}".format( w_path))

        if "swagger.json" in w_path:
            w_resp = self.get_swagger_descriptions(["https","http"])
        else:
            w_resp = self.get(w_path, w_header)
        response.send_content(w_resp.get_status(), w_resp.get_json(), "application/json")

    def do_POST(self, request, response):
        """ """
        w_header = request.get_headers()
        w_resp = None
        w_data = request.read_data()
        w_path = request.get_path()

        if w_header["Content-Type"] == "multipart/form-data":
            # need to parse multipart

            self.upload_media(w_path, w_header, w_data)
            print(w_data)
        else:
            w_str = w_data.decode()
            w_json = json.loads(w_str)
            _logger.info("post path={}, data={}".format(w_path, w_str))

            w_resp = self.post(w_path, w_header, w_json)

        if w_resp.get_header() is not None:
            for key, value in w_resp.get_header().items():
                response.set_header(key, value)

        response.send_content(w_resp.get_status(), w_resp.get_json(), "application/json")

    def do_PUT(self, request, response):
        """ """
        w_str = request.read_data().decode()
        w_path = request.get_path()
        w_header = request.get_headers()
        w_json = json.loads(w_str)
        _logger.info("put path={}, data={}".format(w_path, w_str))

        w_resp = self.put(w_path, w_header, w_json)
        response.send_content(w_resp.get_status(), w_resp.get_json(), "application/json")

    def do_DELETE(self, request, response):
        """ """
        w_path = request.get_path()
        w_header = request.get_headers()
        _logger.info("delete path={}".format( w_path))

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
            w_token = ""
            if ";" in w_cookies:
                w_arr = w_cookies.split(";")
                for w_cookie in w_arr:
                    if "_ycappuccino" in w_cookie:
                        w_token = w_cookie.split("=")[1]
            else:
                w_token = w_cookies.split("=")[1]
            _logger.info("token {}".format(w_token))
            return self._jwt.verify(w_token)


    def find_service(self, a_service_name):
        if a_service_name not in self._map_services:
            # reset map of manager (TODO check why bind doesn't work)
            return None
        return self._map_services[a_service_name]

    def post(self,a_path, a_headers, a_body):
        w_url_path = UrlPath(a_path)
        if w_url_path.is_service():
            w_service_name = w_url_path.get_service_name()
            w_service = self.find_service(w_service_name)
            if w_service is not None:
                if w_service.is_secure() and not self.check_header(a_headers):
                    _logger.info("failed authorization service ")
                    return EndpointResponse(401)
                else:
                    w_header, w_body = w_service.post(a_headers, w_url_path.get_params(), a_body)
                    w_meta = {
                        "type": "array"
                    }
                    if w_body is None:
                        return EndpointResponse(401)
                    else:
                        return EndpointResponse(200, w_header, w_meta, w_body)
            if w_url_path.get_Type() in self._map_handler_endpoints.keys():
                w_handler_endpoint = self._map_handler_endpoints[w_url_path.get_Type()]
                w_handler_endpoint.post(a_path, a_headers, a_body)
        return EndpointResponse(400)

    def put(self, a_path, a_headers, a_body):
        w_url_path = UrlPath(a_path)

        if w_url_path.is_service():
            w_service_name = w_url_path.get_service_name()
            w_service = self.find_services(w_service_name)
            if w_service is not None:
                if w_service.is_secure() and not self.check_header(a_headers):
                    _logger.info("failed authorization service ")

                    return EndpointResponse(401)
                else:
                    w_header, w_body = w_service.put(a_headers, w_url_path.get_params(), a_body)
                    w_meta = {
                        "type": "array"
                    }
                    return EndpointResponse(200, w_header, w_meta, w_body)
            return EndpointResponse(501)
        if w_url_path.get_Type() in self._map_handler_endpoints.keys():
            w_handler_endpoint = self._map_handler_endpoints[w_url_path.get_Type()]
            w_handler_endpoint.put(a_path, a_headers, a_body)
        return EndpointResponse(400)


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
        for w_handle_endpoints in self._map_handler_endpoints.values():
            w_handle_endpoints.get_swagger_descriptions(w_tag, w_swagger, a_scheme)

        for w_service in self._map_services.values():
            util_swagger.get_swagger_description_service(w_service, w_swagger["paths"])
            w_tag.append({"name": util_swagger.get_swagger_description_service_tag(w_service)})

        return EndpointResponse(200, None, None, w_swagger)

    def get(self, a_path, a_headers):
        w_url_path = UrlPath(a_path)

        if w_url_path.is_service():
            w_service_name = w_url_path.get_service_name()
            w_service = self.find_services(w_service_name)
            if w_service is not None:
                if w_service.is_secure() and not self.check_header(a_headers):
                    _logger.info("failed authorization service ")

                    return EndpointResponse(401)
                else:
                    w_header, w_body = w_service.get(a_headers, w_url_path.get_params())
                    w_meta = {
                        "type": "array"
                    }
                    return EndpointResponse(200, w_header,  w_meta, w_body)
            return EndpointResponse(501)
        if w_url_path.get_Type() in self._map_handler_endpoints.keys():
            w_handler_endpoint = self._map_handler_endpoints[w_url_path.get_Type()]
            w_handler_endpoint.put(a_path, a_headers, a_body)
        return EndpointResponse(400)

    def delete(self, a_path, a_headers):
        w_url_path = UrlPath(a_path)
        if w_url_path.is_service():
            w_service_name = w_url_path.get_service_name()
            w_service = self.find_services(w_service_name)
            if w_service is not None:
                if w_service.is_secure() and not self.check_header(a_headers):
                    return EndpointResponse(401)
                else:
                    w_header, w_body =  w_service.delete(a_headers, w_url_path.get_params())
                    w_meta = {
                        "type": "array"
                    }
                    return EndpointResponse(200,w_header, w_meta, w_body)
        if w_url_path.get_Type() in self._map_handler_endpoints.keys():
            w_handler_endpoint = self._map_handler_endpoints[w_url_path.get_Type()]
            w_handler_endpoint.put(a_path, a_headers, a_body)
        return EndpointResponse(400)

    @BindField("_handler_endpoints")
    def bind_manager(self, field, a_handler_endpoint, a_service_reference):
        w_item_plurals = a_handler_endpoint.get_types()
        for w_item_plural in w_item_plurals:
            self._map_handler_endpoints[w_item_plural] = a_handler_endpoint

    @UnbindField("_handler_endpoints")
    def unbind_manager(self, field, a_handler_endpoint, a_service_reference):
        w_item_plurals = a_handler_endpoint.get_types()
        for w_item_plural in w_item_plurals:
            self._map_handler_endpoints[w_item_plural] = None


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

        w_data_path = os.getcwd() + "/data"
        if not os.path.isdir(w_data_path):
            os.mkdir(w_data_path)

        self._file_dir = os.path.join(w_data_path, "files")
        if not os.path.isdir(self._file_dir):
            os.mkdir(self._file_dir)
        _logger.info("Endpoint validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("Endpoint invalidating")

        _logger.info("Endpoint invalidated")
