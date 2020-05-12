from server.api import IEndpoint, IActivityLogger

import pelix.http
import pelix.remote
import logging
import json
from server.beans import UrlPath, EndpointResponse
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, BindField, UnbindField, Instantiate, Property

_logger = logging.getLogger(__name__)


@ComponentFactory('Endpoint-Factory')
@Provides(specifications=[pelix.http.HTTP_SERVLET, IEndpoint.name])
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@Instantiate("endpoints")
@Property("_servlet_path", pelix.http.HTTP_SERVLET_PATH, "/api")
@Property("_reject", pelix.remote.PROP_EXPORT_REJECT, pelix.http.HTTP_SERVLET)
class Endpoint(IEndpoint):

    def __init__(self):
        super(IEndpoint, self).__init__();
        self._log = None
        self._managers = None
        self._map_managers = {}
        self._services = None
        self._map_services = None

    def do_GET(self, request, response):
        """  """
        w_path = request.get_path()
        w_header = request.get_headers()

        w_resp = self.get(w_path, w_header)
        response.send_content(w_resp.get_status(), w_resp.get_json(), "application/json")

    def do_POST(self, request, response):
        """ """
        w_str = request.read_data().decode()
        w_path = request.get_path()
        w_header = request.get_headers()
        w_json = json.loads(w_str)

        w_resp = self.post(w_path, w_header, w_json)
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

    @classmethod
    def check_header(cls, a_headers):
        if a_headers.authorization is not None:
            return True
        else:
            return False



    def post(self,a_path, a_headers, a_body):
        w_url_path = UrlPath(a_path)
        if w_url_path.is_crud():
            w_manager = self._map_managers[w_url_path.get_item_id()]
            if w_manager is not None:
                if w_manager.is_secure() and not self.check_header(a_headers):
                    return EndpointResponse(401)
                w_manager.up_sert(w_url_path.get_params().id if w_url_path.get_params().id is not None else w_url_path.get_params(), a_body)
                w_meta = {
                    type: "object"
                }
                return EndpointResponse(201,w_meta)
            else:
                return EndpointResponse(405)
        return EndpointResponse(400)

    def put(self, a_path, a_headers, a_body):
        w_url_path = UrlPath(a_path)
        if w_url_path.is_crud():
            w_manager = self._map_managers[w_url_path.get_item_id()]
            if w_manager is not None:
                if w_manager.is_secure() and not self.check_header(a_headers):
                    return EndpointResponse(401)
                if w_url_path.get_params() is not None and w_url_path.get_params().id is not None:
                    w_manager.up_sert(w_url_path.get_params().id, a_body)
                    w_meta = {
                        "type": "object",
                        "size": 1
                    }
                    return EndpointResponse(200, w_meta)
            else:
                return EndpointResponse(405)

        return EndpointResponse(400)

    def get(self, a_path, a_headers):
        w_url_path = UrlPath(a_path)
        if w_url_path.is_crud() and w_url_path.get_item_id() in self._map_managers:
            w_manager = self._map_managers[w_url_path.get_item_id()]
            if w_manager is not None:
                if w_manager.is_secure() and not self.check_header(a_headers):
                    return EndpointResponse(401)
                if w_url_path.get_params() is not None and w_url_path.get_params().id is not None:
                    w_resp = w_manager.get_one(w_url_path.get_params().id)
                    w_meta = {
                        "type": "object",
                        "size": 1
                    }
                else:

                    w_resp = w_manager.get_many(w_url_path.get_params())
                    w_meta = {
                        "type": "array",
                        "size": len(w_resp)
                    }
                return EndpointResponse(200, w_meta, w_resp)
            else:
                return EndpointResponse(405)
        return EndpointResponse(400)

    def delete(self, a_path, a_headers):
        w_url_path = UrlPath(a_path)
        if w_url_path.is_crud():
            w_manager = self._map_managers[w_url_path.get_item_id()]
            if w_manager is not None:
                if w_manager.is_secure() and not self.check_header(a_headers):
                    return EndpointResponse(401)
                w_meta = {
                    "type": "object",
                    "size": 1
                }
                if w_url_path.get_params() is not None and w_url_path.get_params().id is not None:
                    w_manager.delete(w_url_path.get_params().id)
                    return EndpointResponse(200, w_meta)
            else:
                return EndpointResponse(405)
        return EndpointResponse(400)

    @BindField("_managers")
    def bind_manager(self,field, a_manager, a_service_reference):
        w_item_id = a_manager.getItem().id
        self._map_managers[w_item_id] = a_manager

    @UnbindField("_managers")
    def unbind_manager(self, field, a_manager, a_service_reference):
        w_item_id = a_manager.getItem().id
        self._map_managers[w_item_id] = None

    @BindField("_services")
    def bind_manager(self, field, a_manager, a_service_reference):
        w_item_id = a_manager.getItem().id
        self._map_managers[w_item_id] = a_manager

    @UnbindField("_services")
    def unbind_manager(self, field, a_manager, a_service_reference):
        w_item_id = a_manager.getItem().id
        self._map_managers[w_item_id] = None


    @Validate
    def validate(self, context):
        _logger.info("Endpoint validating")

        _logger.info("Endpoint validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("Endpoint invalidating")

        _logger.info("Endpoint invalidated")
