#app="all"
from ycappuccino.core.api import IActivityLogger, IService, YCappuccino
from ycappuccino.storage.api import IManager
from ycappuccino.endpoints.api import IJwt
from ycappuccino.core.decorator_app import App

import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, Instantiate, BindField, UnbindField
import hashlib

from ycappuccino.rest_app_base.api import ITenantTrigger
from ycappuccino.storage.api import ITrigger

from ycappuccino.component_creator.api import IComponentServiceFactoryFactory, IComponentServiceList
from pelix.ipopo.constants import use_ipopo

_logger = logging.getLogger(__name__)


@ComponentFactory('ExternalServiceFactory-Factory')
@Provides(specifications=[YCappuccino.name, IComponentServiceList.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_jwt", IJwt.name)
@Requires('_list_factory', IComponentServiceFactoryFactory.name, aggregate=True, optional=True)
@Requires("_manager_component_factory", IManager.name, spec_filter="'(item_id=component_factory)'")
@Instantiate("ComponentServiceList")
@App(name="ycappuccino.component_creator")
class ComponentServiceList(IComponentServiceList):
    def __init__(self):
        super(IComponentServiceList, self).__init__();
        self._context = None
        self._manager_component_factory = None
        self._compoonent_list = {}

    def create_component(self, a_component_model):
        with use_ipopo(self._context) as ipopo:
            # use the iPOPO core service with the "ipopo" variable
            w_factory_model = self._manager_component_factory.get(a_component_model.get_factory_id())
            w_factory_id= w_factory_model.get_factory_id()
            self._log.info("begin create component {}".format(a_component_model["id"]))
            w_instance = ipopo.instantiate(w_factory_id, "Manager-Proxy-{}".format(a_component_model["name"]),
                              {"model": a_component_model})
            self._compoonent_list[a_component_model["name"]] = w_instance
            self._log.info("end create component {}".format(a_component_model["id"]))

    def delete_component(self, a_component_model):
        with use_ipopo(self._context) as ipopo:
            # use the iPOPO core service with the "ipopo" variable
            # use the iPOPO core service with the "ipopo" variable
            w_name = a_component_model["name"]
            self._log.info("begin delete component {}".format(w_name))
            ipopo.kill(w_name)
            del self._compoonent_list[w_name]
            self._log.info("end delete component {}".format(w_name))

    @Validate
    def validate(self, context):
        self._log.info("ComponentServiceFactory validating")
        self._context = context
        self._log.info("ComponentServiceFactory validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("ComponentServiceFactory invalidating")
        self._context = None

        self._log.info("ComponentServiceFactory invalidated")