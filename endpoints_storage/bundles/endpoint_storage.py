#app="all"
from ycappuccino.core.api import  IActivityLogger
from ycappuccino.endpoints.api import IHandlerEndpoint
from ycappuccino.storage.api import IManager, IItemManager
from ycappuccino.core.decorator_app import App

import uuid
import os
import logging
from ycappuccino.endpoints_storage.beans import UrlPath, EndpointResponse
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, BindField, UnbindField, Instantiate
import ycappuccino.core.models.decorators

from ycappuccino.endpoints.api import IJwt

from ycappuccino.endpoints.api import IEndpoint

_logger = logging.getLogger(__name__)

from ycappuccino.endpoints.bundles import util_swagger
from ycappuccino.endpoints.bundles.utils_header import check_header, get_token_decoded, get_token_from_header


@ComponentFactory('EndpointStorage-Factory')
@Provides(specifications=[IHandlerEndpoint.name])
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@Instantiate("handlerEndpointStorage")
@Requires("_item_manager", specification=IItemManager.name)
@Requires("_managers", specification=IManager.name, aggregate=True, optional=True)
@Requires("_endpoint", specification=IEndpoint.name)
@Requires("_jwt", specification=IJwt.name)
@App(name='ycappuccino.endpoint-storage')
class HandlerEndpointStorage(IHandlerEndpoint):

    def __init__(self):
        super(IHandlerEndpoint, self).__init__();
        self._log = None
        self._managers = None
        self._endpoint = None
        self._map_managers = {}
        self._item_manager = None
        self._file_dir = None
        self._jwt = None

    def get_types(self):
        return ["crud","schema","empty"]

    def find_manager(self, a_item_plural_id):
        if a_item_plural_id in self._map_managers:
             return self._map_managers[a_item_plural_id]
        return None

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
            self._log.info("token {}".format(w_token))
            return self._jwt.verify(w_token)

    def get_token(self, a_headers):
        w_token = None
        if "authorization" in a_headers:
            w_authorization = a_headers["authorization"]
            if w_authorization is not None and "Bearer" in w_authorization:
                w_token = w_authorization[len("Bearer "):]
        elif "Cookie" in a_headers:
            w_cookies = a_headers["Cookie"]
            if ";" in w_cookies:
                w_arr = w_cookies.split(";")
                for w_cookie in w_arr:
                    if "_ycappuccino" in w_cookie:
                        w_token = w_cookie.split("=")[1]
            else:
                w_token = w_cookies.split("=")[1]

        return w_token

    def upload_media(self, a_path, a_headers,  a_content):
        w_url_path = UrlPath("put",a_path, self._endpoint.get_swagger_descriptions())
        if w_url_path.is_crud():
            w_item_plural = w_url_path.get_item_plural_id()
            w_manager = self.find_manager(w_item_plural)
            if w_manager is not None:
                w_item = w_manager.get_item_from_id_plural(w_item_plural)
                if w_item["secureWrite"]:
                    if not check_header(self._jwt, a_headers):
                        self._log.info("failed authorization service ")
                        return EndpointResponse(401)
                    w_token = get_token_from_header(a_headers)
                    if not self._jwt.is_authorized(w_token, w_url_path):
                        self._log.info("failed authorization service ")
                        return EndpointResponse(403)

                w_id = w_url_path.get_params()["id"]
                if w_url_path.is_draft():
                    # concat the draft id
                    w_id = w_id + "_" + w_url_path.get_draft()

                # create file in data
                w_filename = "test"
                w_path = self._file_dir+"/"+w_filename;
                with open(w_path,"w") as f:
                    f.write(a_content)

                w_instance = w_manager.get_aggregate_one(w_item["id"], w_id, get_token_decoded(self._jwt, a_headers))
                w_instance[w_item["multipart"]] = w_path
                w_manager.up_sert(w_item["id"], w_id, w_instance.__dict__)
                w_meta = {
                    "type": "object"
                }
                return EndpointResponse(201, None, w_meta, {"id": w_id})
            else:
                return EndpointResponse(405)

    def post(self,a_path, a_headers, a_body):
        w_url_path = UrlPath("post",a_path, self._endpoint.get_swagger_descriptions())
        if w_url_path.is_crud():
            w_item_plural = w_url_path.get_item_plural_id()
            w_manager = self.find_manager(w_item_plural)
            if w_manager is not None:
                w_item = w_manager.get_item_from_id_plural(w_item_plural)
                if not w_item["isWritable"]:
                    self._log.info("failed authorization service ")
                    return EndpointResponse(403)
                if w_item["secureWrite"]:
                    if not check_header(self._jwt, a_headers):
                        self._log.info("failed authorization service ")
                        return EndpointResponse(401)
                    w_token = get_token_from_header(a_headers)
                    if not self._jwt.is_authorized(w_token, w_url_path):
                        self._log.info("failed authorization service ")
                        return EndpointResponse(403)
                if "id" in a_body:
                    w_id = a_body["id"]
                else:
                    w_id = str(uuid.uuid4())
                if w_url_path.is_draft():
                    # concat the draft id
                    w_id = w_id + "_" + w_url_path.get_draft()
                w_manager.up_sert(w_item["id"], w_id, a_body, get_token_decoded(self._jwt, a_headers))
                w_meta = {
                    "type": "array"
                }
                return EndpointResponse(201, None, w_meta, {"id":w_id})
            else:
                return EndpointResponse(405)
        elif w_url_path.is_schema():
            return EndpointResponse(501)

        return EndpointResponse(400)

    def put(self, a_path, a_headers, a_body):
        w_url_path = UrlPath("put",a_path, self._endpoint.get_swagger_descriptions())
        if w_url_path.is_crud():
            w_item_plural = w_url_path.get_item_plural_id()
            w_manager = self.find_manager(w_item_plural)
            if w_manager is not None:
                w_item = w_manager.get_item_from_id_plural(w_item_plural)
                if not w_item["isWritable"]:
                    self._log.info("failed authorization service ")
                    return EndpointResponse(403)
                if w_item["secureWrite"]:
                    if not check_header(self._jwt, a_headers):
                        self._log.info("failed authorization service ")
                        return EndpointResponse(401)
                    w_token = get_token_from_header(a_headers)
                    if not self._jwt.is_authorized(w_token, w_url_path):
                        self._log.info("failed authorization service ")
                        return EndpointResponse(403)

                if w_url_path.get_params() is not None and w_url_path.get_params()["id"] is not None:
                    w_id = w_url_path.get_params()["id"]
                    if w_url_path.is_draft():
                        # concat the draft id
                        w_id = w_id + "_" + w_url_path.get_draft()
                    w_manager.up_sert(w_item["id"], w_id, a_body, get_token_decoded(self._jwt, a_headers))
                    w_meta = {
                        "type": "array",
                        "size": 1
                    }
                    return EndpointResponse(200, None, w_meta, {"id":w_id})
            else:
                return EndpointResponse(405)
        elif w_url_path.is_schema():
            return EndpointResponse(501)

        return EndpointResponse(400)

    def get_swagger_descriptions(self, a_tag, a_swagger, a_scheme):

        util_swagger.get_swagger_description_item(a_swagger["paths"])
        for w_item in ycappuccino.core.models.decorators.get_map_items():
            if not w_item["abstract"]:
                util_swagger.get_swagger_description(w_item, a_swagger["paths"])
                a_tag.append({"name": util_swagger.get_swagger_description_tag(w_item)})

        return EndpointResponse(200, None, None, a_swagger)

    def get(self, a_path, a_headers):
        w_url_path = UrlPath("get",a_path, self._endpoint.get_swagger_descriptions())
        if w_url_path.is_crud():
            w_item_plural = w_url_path.get_item_plural_id()
            if w_item_plural == "items":
                w_manager =  self._item_manager
            else:
                w_manager = self.find_manager(w_item_plural)
            if w_manager is not None:
                w_item = w_manager.get_item_from_id_plural(w_item_plural)

                if w_item["secureRead"]:
                    if not check_header(self._jwt, a_headers):
                        self._log.info("failed authorization service ")
                        return EndpointResponse(401)
                    w_token = get_token_from_header(a_headers)
                    if not self._jwt.is_authorized(w_token, w_url_path):
                        self._log.info("failed authorization service ")
                        return EndpointResponse(403)

                if w_url_path.get_params() is not None and "id" in w_url_path.get_params():
                    w_id = w_url_path.get_params()["id"]
                    if w_url_path.is_draft():
                        # concat the draft id
                        w_id = w_id + "_" + w_url_path.get_draft()
                    w_resp = w_manager.get_one(w_item["id"], w_id, w_url_path.get_params())
                    if w_resp is None:
                        w_resp = w_manager.get_one(w_item["id"], w_url_path.get_params()["id"], w_url_path.get_params())
                    w_meta = {
                        "type": "object",
                        "size": 1
                    }
                else:

                    w_resp_temp = w_manager.get_aggregate_many(w_item["id"],w_url_path.get_params(), get_token_decoded(self._jwt, a_headers))
                    w_resp = []
                    if w_url_path.is_draft():
                        # check if duplicate element with draft exists and only keep the draft one
                        w_draft =  w_url_path.get_draft()
                        w_to_removes = []
                        for w_elem in w_resp_temp:
                            if w_draft in w_elem["_id"]:
                                w_to_removes.append(w_elem["_id"][0:-len(w_draft)+1])
                        for w_elem in w_resp:
                            if w_elem["_id"] not in w_to_removes:
                                w_resp.append(w_elem)
                    else:
                        w_resp = w_resp_temp
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
                return EndpointResponse(200, None, w_meta, w_resp)
        elif w_url_path.is_multipart():
            w_item_plural = w_url_path.get_item_plural_id()

            w_manager = self.find_manager(w_item_plural)
            if w_manager is not None:
                w_item = w_manager.get_item_from_id_plural(w_item_plural)

                w_resp = {
                    "is_multipart" : w_item["multipart"] is not None
                }
                w_meta = {
                    "type": "object",
                    "size": 1
                }
                return EndpointResponse(200, None, w_meta, w_resp)

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
                return EndpointResponse(200, None, w_meta, w_resp)
            return EndpointResponse(501)
        return EndpointResponse(400)

    def delete(self, a_path, a_headers):
        w_url_path = UrlPath("delete",a_path, self._endpoint.get_swagger_descriptions())
        if w_url_path.is_crud():
            w_item_plural = w_url_path.get_item_plural_id()
            w_manager = self.find_manager(w_item_plural)
            if w_manager is not None:
                w_item = w_manager.get_item_from_id_plural(w_item_plural)
                if w_item["secureWrite"]:
                    if not check_header(self._jwt, a_headers):
                        self._log.info("failed authorization service ")
                        return EndpointResponse(401)
                    w_token = get_token_from_header(a_headers)
                    if not self._jwt.is_authorized(w_token, w_url_path):
                        self._log.info("failed authorization service ")
                        return EndpointResponse(403)
                w_meta = {
                    "type": "array",
                    "size": 1
                }
                if w_url_path.get_params() is not None and w_url_path.get_params().id is not None:
                    w_manager.delete(w_item["id"], w_url_path.get_params().id, get_token_decoded(self._jwt, a_headers))
                    return EndpointResponse(200, None, w_meta)
            else:
                return EndpointResponse(405)
        elif w_url_path.is_schema():
            return EndpointResponse(501)

        return EndpointResponse(400)

    @BindField("_managers")
    def bind_manager(self, field, a_manager, a_service_reference):
        w_item_id = a_manager._item_id
        w_item = ycappuccino.core.models.decorators.get_item(w_item_id)
        if w_item is not None:
            w_item_plural = w_item["plural"]
            self._map_managers[w_item_plural] = a_manager

    @UnbindField("_managers")
    def unbind_manager(self, field, a_manager, a_service_reference):
        w_item_id = a_manager._item_id
        w_item = ycappuccino.core.models.decorators.get_item(w_item_id)
        if w_item is not None:
            w_item_plural = w_item["plural"]
            self._map_managers[w_item_plural] = None

    @Validate
    def validate(self, context):
        self._log.info("HandlerEndpointStorage validating")

        w_data_path = os.getcwd() + "/data"
        if not os.path.isdir(w_data_path):
            os.mkdir(w_data_path)

        self._file_dir = os.path.join(w_data_path, "files")
        if not os.path.isdir(self._file_dir):
            os.mkdir(self._file_dir)
        self._log.info("HandlerEndpointStorage validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("HandlerEndpointStorage invalidating")

        self._log.info("HandlerEndpointStorage invalidated")
