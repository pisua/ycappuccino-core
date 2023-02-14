# component that decribe fetcher by kind of channel (protocol supported)

#app="all"
from ycappuccino.core.api import IActivityLogger,  YCappuccino, IService

import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property, Provides, Instantiate


_logger = logging.getLogger(__name__)


@ComponentFactory('DeviceSender-Factory')
@Provides(specifications=[IService.name, YCappuccino.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Instantiate("deviceSender")
class DeviceSender(IService):

    def __init__(self):
        pass

