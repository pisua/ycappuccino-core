#app="all"
from ycappuccino.core.api import IActivityLogger, IService, YCappuccino
from ycappuccino.storage.api import IManager
from ycappuccino.endpoints.api import IJwt
from ycappuccino.core.decorator_app import App
from ycappuccino.core.framework import listener_factory
import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, Instantiate, BindField, UnbindField
import hashlib
import ycappuccino.component_creator.models.component_factory
from ycappuccino.rest_app_base.api import ITenantTrigger
from ycappuccino.storage.api import ITrigger

from ycappuccino.component_creator.api import  IComponentServiceList
from pelix.ipopo.constants import use_ipopo

_logger = logging.getLogger(__name__)


@ComponentFactory('ExternalServiceFactory-Factory')
@Provides(specifications=[YCappuccino.name, IComponentServiceList.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_jwt", IJwt.name)
@Requires("_manager_component_factory", IManager.name, spec_filter="'(item_id=component_factory)'")
@Instantiate("ComponentServiceList")
@App(name="ycappuccino.component_creator")
class ComponentServiceList(IComponentServiceList):
    def __init__(self):
        super(IComponentServiceList, self).__init__();
        self._context = None
        self._manager_component_factory = None
        self._compoonent_list = {}
        self._jwt = None


    def notify(self, a_factory_name):
        wComponentFactory = ycappuccino.component_creator.models.component_factory.ComponentFactory()
        wComponentFactory.id(a_factory_name)
        wComponentFactory.name(a_factory_name)
        wComponentFactory.factory_id(a_factory_name)
        self._manager_component_factory.up_sert_model(a_factory_name, wComponentFactory, self._subject)


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
        self._subject = self._jwt.get_token_subject("bootstrap", "yblues")
        w_service_spec = "ycappuccino.api.IComponentServiceFactory"
        w_list = listener_factory.get_factories_by_service_specification(w_service_spec)
        for w_factory in w_list:
            self.notify(w_factory)
        listener_factory.subscribe_notifier(w_service_spec, self)

        self._log.info("ComponentServiceFactory validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("ComponentServiceFactory invalidating")
        self._context = None

        self._log.info("ComponentServiceFactory invalidated")