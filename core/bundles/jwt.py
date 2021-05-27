from ycappuccino.core.api import IActivityLogger, IJwt, IConfiguration

import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, Instantiate, Property

_logger = logging.getLogger(__name__)

import jwt

KEY = 'YCap'
@ComponentFactory('Jwt-Factory')
@Provides(specifications=[IJwt.name])
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_config",IConfiguration.name)
@Instantiate("jwt")
class Jwt(IJwt):

    def __init__(self):
        super(IJwt, self).__init__();
        self._log = None
        self._key = None
        self._config = None

    def load_configuration(self):
        self._key = self._config.get("jwt.token.key", KEY)

    def generate(self,login, password):
        # tody manage right / account / tenant
        return jwt.encode({'iss': 'auth0', 'login': login }, self._key , algorithm='HS256').decode("utf-8")

    def verify(self, a_token):
        w_res = jwt.decode(a_token, self._key, algorithms='HS256')
        return w_res is not None

    @Validate
    def validate(self, context):
        _logger.info("Endpoint validating")
        self.load_configuration()
        _logger.info("Endpoint validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("Endpoint invalidating")

        _logger.info("Endpoint invalidated")
