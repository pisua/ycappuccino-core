#app="all"
from ycappuccino.core.api import IActivityLogger,  IConfiguration
from ycappuccino.endpoints.api import IClientIndexPath

import logging, os
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property,  Provides, Instantiate
from ycappuccino.core.decorator_app import App

import inspect
import base64


_logger = logging.getLogger(__name__)


@ComponentFactory('ClientPath-Factory')
@Provides(specifications=[IClientIndexPath.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_config", IConfiguration.name)
@Property('_id', "id", "default")
@Property('_subpath', "subpath", "client")
@Property('_secure', "secure", False)
@Property('_priority', "priority", 0)
@App(name="ycappuccino.endpoint")
class ClientPath(IClientIndexPath):

    def __init__(self):
        super(IClientIndexPath, self).__init__();
        self.path_core = inspect.getmodule(self).__file__.replace("endpoints{0}bundles{0}server_path.py".format(os.path.sep), "")
        self.path_app = inspect.getmodule(self).__file__.replace("ycappuccino{0}endpoints{0}bundles{0}server_path.py".format(os.path.sep), "")
        self._log =None
        self._secure =None
        self._user = None
        self._pass =None
        self._id = None
        self._priority = None
        self._subpath = None
        self._config = None

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
        self._log.info("ClientPath validating")
        self.load_configuration()

        self._log.info("ClientPath validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("ClientPath invalidating")

        self._log.info("ClientPath invalidated")


@ComponentFactory('ClientPathSwagger-Factory')
@Provides(specifications=[IClientIndexPath.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Instantiate("ClientPathSwagger")
@App(name="ycappuccino.endpoint")
class ClientPathSwagger(IClientIndexPath):

    def __init__(self):
        super(IClientIndexPath, self).__init__();
        self.path_core = inspect.getmodule(self).__file__.replace("bundles{0}server_path.py".format(os.path.sep), "")
        self._log =None
        self._secure = False
        self._user = None
        self._pass =None
        self._id = "/swagger"
        self._priority = 0
        self._subpath = "swagger"
        self._config = None

    def get_path(self):
        w_path =[self.path_core+self._subpath]

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
        self._log.info("ClientPathSwagger validating")
        self.load_configuration()

        self._log.info("ClientPathSwagger validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("ClientPathSwagger invalidating")

        self._log.info("ClientPathSwagger invalidated")