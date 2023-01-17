#app="all"
from ycappuccino.core.api import IActivityLogger,  IConfiguration
from ycappuccino.core.executor_service import ThreadPoolExecutorCallable, RunnableProcess
from ycappuccino.endpoints.api import IJwt

import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, Instantiate
import time

_logger = logging.getLogger(__name__)

import jwt

TIMEOUT = 15*60*1000

KEY = 'YCap'


class PurgeToken(RunnableProcess):
    def __init__(self, a_service):
        super(PurgeToken, self).__init__("PurgeToken")
        self._jwt = a_service
    def process(self):
        """ abstract run class"""
        w_to_delete = []
        for w_token_decoded_key in self._jwt.get_get_token_decoded().keys():
            w_token_decoded = self._jwt.get_token_decoded()[w_token_decoded_key]
            seconds = int(round(time.time() ))
            if w_token_decoded is not None and "exp" in w_token_decoded and w_token_decoded["exp"] > seconds:
                pass
            else:
                w_to_delete.append(w_token_decoded_key)

        for w_token_decoded_key in  w_to_delete:
            self._jwt.delete_token_decoded(w_token_decoded_key)


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
        # list of token decode. keep the token until expiration time
        self._token_decoded = {}
        self._executor_service = ThreadPoolExecutorCallable()
        self._runnable = PurgeToken(self)
    def load_configuration(self):
        self._key = self._config.get("jwt.token.key", KEY)
        self._timeout = self._config.get("jwt.token.timeout", TIMEOUT)


    def get_token_decoded(self):
        return self._token_decoded

    def delete_token_decoded(self, a_token):
        del self._token_decoded[a_token]
    def generate(self, a_login, a_tenant):
        # tody manage right / account / tenant
        seconds = int(round(time.time()))
        exp = int(round(time.time()))+self._timeout

        return jwt.encode({'sub': a_login, "tid": a_tenant, "iat": seconds, "exp" : exp }, self._key , algorithm='HS256')

    def decode(self, a_token):
        return self._token_decoded[a_token]

    def verify(self, a_token):
        w_res = jwt.decode(a_token, self._key, algorithms='HS256')
        seconds = int(round(time.time() ))
        if w_res is not None and "exp" in w_res and w_res["exp"] > seconds:
            self._token_decoded[a_token] = w_res
            return True
        if a_token in self._token_decoded.keus():
            del self._token_decoded[a_token]
        return False

    @Validate
    def validate(self, context):
        _logger.info("Endpoint validating")
        self.load_configuration()
        self._runnable.set_activate(True)
        self._executor_service.submit(self._runnable)
        _logger.info("Endpoint validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("Endpoint invalidating")
        self._runnable.set_activate(False)
        _logger.info("Endpoint invalidated")
