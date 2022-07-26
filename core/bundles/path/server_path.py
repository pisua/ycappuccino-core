from ycappuccino.core.api import IActivityLogger, IManager, IBootStrap, YCappuccino, IClientIndexPathFactory, IClientIndexPath
import logging, os
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property,  Provides, Instantiate, BindField, UnbindField
from pelix.ipopo.constants import use_ipopo

import inspect
import base64


_logger = logging.getLogger(__name__)


@ComponentFactory('ClientPath-Factory')
@Provides(specifications=[IClientIndexPath.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Property('_id', "id", "default")
@Property('_subpath', "subpath", "client")
@Property('_secure', "secure", False)
@Property('_priority', "priority", 0)
class ClientPath(IClientIndexPath):

    def __init__(self):
        super(IClientIndexPath, self).__init__();
        self.path_core = inspect.getmodule(self).__file__.replace("core{0}bundles{0}path{0}server_path.py".format(os.path.sep), "")
        self.path_app = inspect.getmodule(self).__file__.replace("ycappuccino{0}core{0}bundles{0}path{0}server_path.py".format(os.path.sep), "")
        self._log =None
        self._secure =None
        self._user = None
        self._pass =None
        self._id = None
        self._priority = None
        self._subpath = None

    def get_path(self):
        w_path =[self.path_app+self._subpath,self.path_core+self._subpath]

        return w_path

    def get_priority(self):
        return self._priority

    def get_subpath(self):
        return self._subpath

    def is_auth(self):
        return self._secure

    def get_id(self):
        return self._id

    def load_configuration(self):
        if self._secure :
            self._user = self._config.get(self._id+".login", "admin")
            self._pass = self._config.get(self._id+".password", "1234")

    def check_auth(self, a_authorization):
        if a_authorization is not None and "Basic " in a_authorization:
            w_decode = base64.standard_b64decode(a_authorization.replace("Basic ", "")).decode('ascii')
            if ":" in w_decode:
                w_user = w_decode.split(":")[0]
                w_pass = w_decode.split(":")[1]
                if w_user == self._user and w_pass == self._pass:
                    return True

        return False

    @Validate
    def validate(self, context):
        _logger.info("ClientPath validating")
        self.load_configuration()

        _logger.info("ClientPath validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("ClientPath invalidating")

        _logger.info("ClientPath invalidated")


@ComponentFactory('ClientPathFactory-Factory')
@Provides(specifications=[IClientIndexPathFactory.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_manager_client_path", IManager.name, spec_filter="'(item_id=clientPath)'")
@Requires("_bootstraps", specification=IBootStrap.name, aggregate=True, optional=True)
@Instantiate("ClientPathFactory")
class ClientPathFactory(IClientIndexPathFactory):

    def __init__(self):
        super(IClientIndexPathFactory, self).__init__();
        self._bootstraps = None
        self._manager_client_path = None
        self._map_boostrap = {}
        self._map_client_path = {}
        self._context = None

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

        if a_model.id not in self._map_client_path.keys():
            with use_ipopo(a_bundle_context) as ipopo:
                # use the iPOPO core service with the "ipopo" variable
                if "subpath" in a_model.__dict__.keys():
                    ipopo.instantiate("ClientPath-Factory", "ClientPath-{}".format(a_model.id),
                                      {"id": a_model.path,"subpath":a_model.subpath,"priority":a_model.priority,  "secure": a_model.secure} )
                else:
                    ipopo.instantiate("ClientPath-Factory", "ClientPath-{}".format(a_model.id),
                                      {"id": a_model.path, "subpath": "","priority":a_model.priority, "secure": a_model.secure})
                self._map_client_path[a_model.id] = True

    def create_client_paths(self):
        if self._context is not None:
            w_models = self._manager_client_path.get_many("clientPath", None)
            for w_model in w_models:
                self.create_client_path(w_model, self._context)


    @Validate
    def validate(self, context):
        _logger.info("ClientPathFactory validating")
        self._context = context
        self.create_client_paths()
        _logger.info("ClientPathFactory validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("ClientPathFactory invalidating")

        _logger.info("ClientPathFactory invalidated")
