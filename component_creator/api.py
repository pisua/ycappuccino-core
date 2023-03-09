#app="all"
from ycappuccino.core.api import CFQCN

from pelix.ipopo.decorators import Validate, Invalidate, Requires, Property
from pelix.ipopo.constants import use_ipopo
from ycappuccino.storage.api import IManager

from ycappuccino.component_creator.models.component_factory import ComponentFactory
from ycappuccino.endpoints.api import IJwt


class IComponentServiceList(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("IComponentServiceList")

    def __init__(self):
        """ abstract constructor """
        pass

@Requires("_manager_component", IManager.name, spec_filter="'(item_id=component_factory)'")
@Requires("_jwt", IJwt.name)
class IComponentServiceFactoryFactory(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("IComponentServiceFactoryFactory")

    def __init__(self):
        """ abstract constructor """
        self._context = None
        self._name = None
        self._manager_component = None
        self._factory_id = None # factory of the component to create
    def create_component(self, a_component_model):
        with use_ipopo(self._context) as ipopo:

            # use the iPOPO core service with the "ipopo" variable
            w_name = a_component_model["name"]
            self._log.info("begin create component {}".format(w_name))
            ipopo.instantiate(self._factory_id, "Component-{}".format(w_name),
                              {"model": a_component_model})

            self._log.info("end create component {}".format(w_name))

    def delete_component(self, a_component_model):
        with use_ipopo(self._context) as ipopo:
            # use the iPOPO core service with the "ipopo" variable
            w_name = a_component_model["name"]
            self._log.info("begin delete component {}".format(w_name))
            ipopo.kill(w_name)
            self._log.info("end delete component {}".format(w_name))

    def get_factory_id(self):
        """ return the factory ipopo name"""
        return self._factory_id


    @Validate
    def validate(self, a_context):
        self._context = a_context
        w_subject = self._jwt.get_token_subject("component_create", "system")

        w_component_factory = ComponentFactory()
        w_component_factory.name(self._name)
        w_component_factory.factory_id(self._factory_id)
        w_component_factory.configuration_schema(self._configuration_schema)

        self._manager_component.up_sert_model(self._name,  w_component_factory, w_subject)

    @Invalidate
    def invalidate(self, a_context):
        self._context = a_context

@Property('_model', "model", None)
class IComponentServiceFactory(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("IComponentServiceFactory")

    def __init__(self):
        """ abstract constructor """
        self._model = None

