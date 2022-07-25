from ycappuccino.core.api import IActivityLogger, IJwt, IConfiguration

import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, Instantiate, Property
import time

_logger = logging.getLogger(__name__)

import jwt

TIMEOUT = 15*60*1000

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
        self._timeout = None

    def load_configuration(self):
        self._key = self._config.get("jwt.token.key", KEY)
        self._timeout = self._config.get("jwt.token.timeout", TIMEOUT)

    def generate(self,login):
        # tody manage right / account / tenant
        milliseconds = int(round(time.time() * 1000))+self._timeout
        return jwt.encode({'iss': 'auth0', 'login': login, "iat": milliseconds }, self._key , algorithm='HS256')

    def verify(self, a_token):
        w_res = jwt.decode(a_token, self._key, algorithms='HS256')
        milliseconds = int(round(time.time() * 1000))
        if w_res is not None and "iat" in w_res and w_res["iat"] > milliseconds:
            return True
        return False

    @Validate
    def validate(self, context):
        _logger.info("Endpoint validating")
        self.load_configuration()
        _logger.info("Endpoint validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("Endpoint invalidating")

        _logger.info("Endpoint invalidated")
