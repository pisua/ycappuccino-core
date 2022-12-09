from ycappuccino.core.api import  IActivityLogger, IConfiguration, YCappuccino, IServerProxy
import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property, Provides, Instantiate, BindField, UnbindField
import pelix.http

_logger = logging.getLogger(__name__)


@ComponentFactory('Proxy-Factory')
@Provides(specifications=[IServerProxy.name, YCappuccino.name, pelix.http.HTTP_SERVLET])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_config", IConfiguration.name)
@Property("_servlet_path", pelix.http.HTTP_SERVLET_PATH, "/proxy")
@Requires('_components', YCappuccino.name,optional=True,aggregate=True)
@Instantiate("serverProxy")
class Proxy(object):

    def __init__(self):
        self._components = None
        self._map_component = {}

        self._log = None

    @BindField("_components")
    def bind_components(self, field, a_service, a_service_reference):
        for interface in a_service_reference.get_properties()["objectClass"]:
            if interface not in self._map_component:
                self._map_component[interface] = []
            self._map_component[interface].append(a_service)
            self.notifySse(a_service, a_service_reference, True)

    @UnbindField("_components")
    def unbind_components(self, field, a_service, a_service_reference):
        for interface in a_service_reference.get_properties()["objectClass"]:
            self._map_component[interface].remove(a_service)
            self.notifySse(a_service, a_service_reference, False)


    def notifySse(self, a_service, a_service_reference, isBinded):
        """ notify if sse client open all bind component """
        pass

    @Validate
    def validate(self, context):
        _logger.info("serverProxy validating")

        _logger.info("serverProxy validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("serverProxy invalidating")

        _logger.info("serverProxy invalidated")
