from ycappuccino.core.api import IActivityLogger, IManager, IManagerBootStrapData, YCappuccino
import logging, os
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate,  Provides, Instantiate, BindField, UnbindField

import inspect

from ycappuccino.core.api import IClientIndexPath

_logger = logging.getLogger(__name__)


@ComponentFactory('ReactPath-Factory')
@Provides(specifications=[IClientIndexPath.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Instantiate("ReactPath")
class ReactPath(IClientIndexPath):

    def __init__(self):
        super(IClientIndexPath, self).__init__();
        self._path =inspect.getmodule(self).__file__.replace("core{0}bundles{0}path{0}react_path.py".format(os.path.sep), "")
        self._log =None
        self._id = "react"

    def get_path(self):
        return self._path

    def is_auth(self):
        return False

    def get_id(self):
        return self._id
    @Validate
    def validate(self, context):
        _logger.info("ReactPath validating")


        _logger.info("ReactPath validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("ReactPath invalidating")

        _logger.info("ReactPath invalidated")
