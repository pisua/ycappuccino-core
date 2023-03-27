#app="all"
from ycappuccino.core.api import IActivityLogger
from ycappuccino.storage.api import IManager, IBootStrap
from ycappuccino.rest_app_base.api import IClientIndexPathFactory

import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, Instantiate, BindField, UnbindField
from pelix.ipopo.constants import use_ipopo
from ycappuccino.core.decorator_app import App

_logger = logging.getLogger(__name__)


@ComponentFactory('ClientPathFactory-Factory')
@Provides(specifications=[IClientIndexPathFactory.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_manager_client_path", IManager.name, spec_filter="'(item_id=clientPath)'")
@Requires("_bootstraps", specification=IBootStrap.name, aggregate=True, optional=True)
@Instantiate("ClientPathFactory")
@App(name="ycappuccino.rest-app")
class ClientPathFactory(IClientIndexPathFactory):

    def __init__(self):
        super(IClientIndexPathFactory, self).__init__();
        self._bootstraps = None
        self._manager_client_path = None
        self._map_boostrap = {}
        self._map_client_path = {}
        self._context = None
        self._log = None

    @BindField("_bootstraps")
    def bind_bootstrap(self, a_field, a_service, a_service_reference):
        if a_service is not None:
            self._map_boostrap[a_service.get_id()] = a_service
        self.create_client_paths()

    @UnbindField("_bootstraps")
    def un_bind_bootstrap(self, a_field, a_service, a_service_reference):
        if a_service.get_id() in self._map_boostrap:
            del self._map_boostrap[a_service.get_id()]

    def create_client_path(self, a_model,   a_bundle_context):

        if a_model._id not in self._map_client_path.keys():
            with use_ipopo(a_bundle_context) as ipopo:
                # use the iPOPO core service with the "ipopo" variable
                if "_subpath" in a_model.__dict__.keys():
                    ipopo.instantiate("ClientPath-Factory", "ClientPath-{}".format(a_model._id),
                                      {"id": a_model._path,"subpath":a_model._subpath,"priority":a_model._priority, "type":a_model.get_type(), "core":a_model.is_core(),  "secure": a_model._secure} )
                else:
                    ipopo.instantiate("ClientPath-Factory", "ClientPath-{}".format(a_model._id),
                                      {"id": a_model._path, "subpath": "","priority":a_model._priority, "type":a_model.get_type(), "core":a_model.is_core(), "secure": a_model._secure})
                self._map_client_path[a_model._id] = True

    def create_client_paths(self):
        if self._context is not None:
            w_models = self._manager_client_path.get_many("clientPath", None)
            for w_model in w_models:
                self.create_client_path(w_model, self._context)


    @Validate
    def validate(self, context):
        self._log.info("ClientPathFactory validating")
        self._context = context
        self.create_client_paths()
        self._log.info("ClientPathFactory validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("ClientPathFactory invalidating")

        self._log.info("ClientPathFactory invalidated")

