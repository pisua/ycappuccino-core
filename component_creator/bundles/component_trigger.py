#app="all"
from ycappuccino.core.api import IActivityLogger, IService, YCappuccino
from ycappuccino.storage.api import IManager
from ycappuccino.endpoints.api import IJwt
from ycappuccino.core.decorator_app import App

import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, Instantiate
import hashlib

from ycappuccino.storage.api import ITrigger

from ycappuccino.component_creator.api import IComponentServiceList

_logger = logging.getLogger(__name__)


@ComponentFactory('ComponentServiceTrigger-Factory')
@Provides(specifications=[YCappuccino.name, ITrigger.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_component_services_list", IComponentServiceList.name)
@Requires("_jwt", IJwt.name)
@Instantiate("ComponentServiceTrigger")
@App(name="ycappuccino.component_creator")
class ComponentServiceTrigger(ITrigger):
    def __init__(self):
        super(ComponentServiceTrigger, self).__init__("ComponentServiceTrigger", "component", ["upsert", "delete"], a_synchronous=True,a_post=True);
        self._component_services = {}
        self._component_services_list = None


    def execute(self, a_action, a_component_service):
        w_factory_id = a_component_service.get_factory_id();
        w_name = a_component_service.get_name();

        w_active = False

        if a_action == "post" or a_action == "put":
            w_active = a_component_service.get_active();
        elif a_action == "get":
            return a_component_service
        if w_factory_id is not None:
            if w_name in self._component_services.keys():
                # TDOO detroy
                w_component = self._component_services_list.delete_component(a_component_service)
                del self._component_services[w_name]
            if w_active :
                w_component = self._component_services_list.create_component(a_component_service)
                self._component_services[w_name] = w_component
            return a_component_service
    @Validate
    def validate(self, context):
        self._log.info("ComponentServiceTrigger validating")

        self._log.info("ComponentServiceTrigger validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("ComponentServiceTrigger invalidating")

        self._log.info("ComponentServiceTrigger invalidated")