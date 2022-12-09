from ycappuccino.core.api import IActivityLogger, YCappuccino, IService
from ycappuccino.rest_app_base.api import IClobReplaceService

import pelix.remote
import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, BindField, UnbindField, Instantiate, Property
from ycappuccino.storage.models.decorators import get_map_items


_logger = logging.getLogger(__name__)


@ComponentFactory('JSReplaceService-Factory')
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_services", specification=IService.name, aggregate=True, optional=True)
@Provides(specifications=[IClobReplaceService.name, YCappuccino.name])
@Instantiate("JSReplaceService")
class JSReplaceService(IClobReplaceService):

    def __init__(self):
        self._services = None
        self._map_services = {}

    def extension(self):
        return ".js.mdl"

    def replace_content(self, a_in):
        """ return out string with applyance of replacement """
        # replace angularjs rest api
        w_replace_angularjs = "{}s: $resource(current_url+'/{}s'),\n".format("item", "item")
        w_replace_angularjs = w_replace_angularjs + "{}: $resource(current_url+'/{}s/:id'".format("item", "item")+", null, {'update':{method:'PUT'}})"

        for w_item in get_map_items():
            w_item_id = w_item["id"]
            if len(w_replace_angularjs) != 0:
                w_add=",\n"
            w_add = w_add+"{}s: $resource(current_url+'/{}s'),\n".format(w_item_id, w_item_id)
            w_add = w_add+"{}: $resource(current_url+'/{}s/:id'".format(w_item_id, w_item_id)+", null, {'update':{method:'PUT'}}),\n"
            w_add = w_add+"{}sSchema: $resource(current_url+'/{}s/$schema'),\n".format(w_item_id, w_item_id)
            w_add = w_add+"{}sMultipart: $resource(current_url+'/{}s/$multipart')".format(w_item_id, w_item_id)

            w_replace_angularjs=w_replace_angularjs+w_add

        for service in self._services:
            if len(w_replace_angularjs) != 0:
                w_add = ",\n"
            else:
                w_add = ""
            w_add = w_add + "{}: $resource(current_url+'/{}')".format("service_"+service.get_name(), "$service/"+service.get_name())
            w_replace_angularjs = w_replace_angularjs + w_add

        return a_in.replace("${rest_api_resource}",w_replace_angularjs)


    @BindField("_services")
    def bind_services(self, field, a_service, a_service_reference):
        w_service = a_service.get_name()
        self._map_services[w_service] = a_service

    @UnbindField("_services")
    def unbind_services(self, field, a_service, a_service_reference):
        w_service = a_service.get_name()
        self._map_services[w_service] = None
