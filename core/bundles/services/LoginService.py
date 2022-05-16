from ycappuccino.core.api import IActivityLogger, IManager, IService, YCappuccino, IJwt,ILoginService
import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property, Provides, Instantiate, BindField, UnbindField
import hashlib


_logger = logging.getLogger(__name__)


@ComponentFactory('LoginService-Factory')
@Provides(specifications=[IService.name, YCappuccino.name,ILoginService.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_manager_login", IManager.name, spec_filter="'(item_id=login)'")
@Requires("_jwt", IJwt.name)
@Instantiate("LoginService")
class LoginService(IService, ILoginService):

    def __init__(self):
        super(IService, self).__init__();
        self._manager_login = None
        self._log = None
        self._jwt = None

    def get_name(self):
        return "login"


    def post(self, a_header, a_params, a_body):
        if "login" in a_body and "password" in a_body:
            w_login = self._manager_login.get_one("login",  a_body["login"])

            w_concat = "{}{}".format(w_login.__dict__["salt"], a_body["password"]).encode("utf-8")
            result = hashlib.md5(w_concat).hexdigest()

            if w_login.__dict__["password"] == result:
                w_token = self._jwt.generate(a_body["login"])
                return {
                    "token": w_token
                }
        return None

    def put(self, a_header, a_params, a_body):
        return None

    def get(self, a_header, a_params):
        return None

    def delete(self, a_header, a_params):
        return None

    @Validate
    def validate(self, context):
        _logger.info("AccountBootStrap validating")

        _logger.info("AccountBootStrap validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("AccountBootStrap invalidating")

        _logger.info("AccountBootStrap invalidated")
