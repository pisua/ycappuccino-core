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

    def get_name(self):
        return "device-sender"

    def is_sercure(self):
        return True

    def has_post(self):
        return True

    def has_put(self):
        return True

    def has_get(self):
        return True

    def has_delete(self):
        return True

    def get_extra_path(self):
        """ return the list of extra path that are manage by service """
        return {
            "post": ["{sensorId}/value"],
            "get": [],
            "put": [],
            "delete": []
        }
    def post(self, a_header, a_url_path, a_body):
        pass

    def put(self, a_header, a_url_path, a_body):
        pass

    def get(self, a_header, a_url_path):
        pass

    def delete(self, a_header, a_url_path):
        pass
