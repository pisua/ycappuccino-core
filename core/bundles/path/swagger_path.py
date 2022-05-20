from ycappuccino.core.api import IActivityLogger, IManager, IManagerBootStrapData, YCappuccino, IConfiguration
import logging, os
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate,  Provides, Instantiate, BindField, UnbindField

import inspect
import base64
from ycappuccino.core.api import IClientIndexPath

_logger = logging.getLogger(__name__)


@ComponentFactory('SwaggerPath-Factory')
@Provides(specifications=[IClientIndexPath.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_config", IConfiguration.name)
@Instantiate("SwaggerPath")
class SwaggerPath(IClientIndexPath):

    def __init__(self):
        super(IClientIndexPath, self).__init__();
        self._path =inspect.getmodule(self).__file__.replace("core{0}bundles{0}path{0}swagger_path.py".format(os.path.sep), "")
        self._log =None
        self._id = "swagger"
        self._user = None
        self._pass = None
        self._config = None

    def get_path(self):
        return self._path

    def is_auth(self):
        return True

    def check_auth(self, a_authorization):
        if a_authorization is not None and "Basic " in a_authorization:
            w_decode = base64.standard_b64decode(a_authorization.replace("Basic ","")).decode('ascii')
            if ":" in w_decode:
                w_user = w_decode.split(":")[0]
                w_pass = w_decode.split(":")[1]
                if w_user == self._user and w_pass == self._pass:
                    return True

        return False

    def get_id(self):
        return self._id


    def load_configuration(self):
        self._user = self._config.get("swagger.login", "admin")
        self._pass = self._config.get("swagger.password", "1234")


    @Validate
    def validate(self, context):
        _logger.info("SwaggerPath validating")

        self.load_configuration()
        _logger.info("SwaggerPath validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("SwaggerPath invalidating")

        _logger.info("SwaggerPath invalidated")
