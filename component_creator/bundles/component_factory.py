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

_logger = logging.getLogger(__name__)


@ComponentFactory('ExternalServiceFactory-Factory')
@Provides(specifications=[YCappuccino.name, IComponentServiceList.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_jwt", IJwt.name)
@Requires('_list_factory', IComponentServiceFactoryFactory.name, aggregate=True, optional=True)
@Requires('_manager_component_factory', IManager.name,  spec_filter="'(name=main)'")
@Instantiate("ComponentServiceList")
@App(name="ycappuccino.component_creator")
class ComponentServiceList(IComponentServiceList):
    def __init__(self):
        super(IComponentServiceList, self).__init__();
        self._list_factory = []
        self._map_factory = {}
        self._external_services_factory = {}

    def create_component(self, a_component_model):
        pass

    def get_factory(self, a_id):
        if a_id in self._map_factory:
            return self._map_factory[a_id]
        return None



    @BindField("_list_factory")
    def bind_external_services_factory(self, a_action, a_component_factory_factory, a_reference):
        w_factory_id = a_component_factory_factory.get_factory_id()
        self._map_factory[w_factory_id] = a_component_factory_factory

    @UnbindField("_list_factory")
    def unbind_external_services_factory(self, a_action, a_component_factory_factory, a_reference):
        w_factory_id = a_component_factory_factory.get_factory_id()
        del self._map_factory[w_factory_id]
    @Validate
    def validate(self, context):
        self._log.info("ComponentServiceFactory validating")

        self._log.info("ComponentServiceFactory validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("ComponentServiceFactory invalidating")

        self._log.info("ComponentServiceFactory invalidated")