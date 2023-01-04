#app="all"
from ycappuccino.core.api import IActivityLogger, IService, YCappuccino
from ycappuccino.storage.api import IManager
from ycappuccino.endpoints.api import IJwt
from ycappuccino.rest_app_base.api import ILoginService

import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, Instantiate
import hashlib


_logger = logging.getLogger(__name__)


class AbsService(IService, ILoginService):

    def __init__(self):
        super(IService, self).__init__();
        self._manager_login = None
        self._log = None
        self._jwt = None




    def change_password(self, a_login, a_password, a_new_password):
        """ return tuple of 2 element that admit a dictionnary of header and a body"""
        _logger.info("change password")

        w_login = self._manager_login.get_one("login", a_login)

        w_concat = "{}{}".format(w_login.__dict__["_salt"], a_password).encode("utf-8")
        result = hashlib.md5(w_concat).hexdigest()

        if w_login.__dict__["_password"] == result:
            w_login.password(a_new_password)
            _logger.info(" password changed")

            return self._manager_login.up_sert_model(w_login._id, w_login)

        return None


    def check_login(self, a_login, a_password):
        """ return tuple of 2 element that admit a dictionnary of header and a body"""
        w_login = self._manager_login.get_one("login",  a_login)

        w_concat = "{}{}".format(w_login._salt, a_password).encode("utf-8")
        result = hashlib.md5(w_concat).hexdigest()

        if w_login._password == result:
            w_token = self._jwt.generate(a_login)
            return w_token
        return None

@ComponentFactory('LoginService-Factory')
@Provides(specifications=[IService.name, YCappuccino.name,ILoginService.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_manager_login", IManager.name, spec_filter="'(item_id=login)'")
@Requires("_jwt", IJwt.name)
@Instantiate("LoginService")
class LoginService(AbsService):

    def __init__(self):
        super(LoginService, self).__init__();
        self._manager_login = None
        self._log = None
        self._jwt = None

    def get_name(self):
        return "auth"

    def is_sercure(self):
        return False

    def post(self, a_header, a_params, a_body):
        """ return tuple of 2 element that admit a dictionnary of header and a body"""

        w_token = self.check_login(a_body["login"], a_body["password"])
        if w_token is not None:
            return {},{
                "token": w_token
            }
        return None, None


    def get(self, a_header, a_params):
        return self.post(a_header, a_params, None)

    def delete(self, a_header, a_params):
        return self.post(a_header, a_params, None)

    @Validate
    def validate(self, context):
        _logger.info("LoginService validating")

        _logger.info("LoginService validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("LoginService invalidating")

        _logger.info("LoginService invalidated")




@ComponentFactory('ChangePasswordService-Factory')
@Provides(specifications=[IService.name, YCappuccino.name,ILoginService.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_manager_login", IManager.name, spec_filter="'(item_id=login)'")
@Requires("_jwt", IJwt.name)
@Instantiate("ChangePasswordService")
class ChangePasswordService(AbsService):

    def __init__(self):
        super(ChangePasswordService, self).__init__();
        self._manager_login = None
        self._log = None


    def is_secure(self):
        return True


    def get_name(self):
        return "change_password"

    def post(self, a_header, a_params, a_body):
        """ return tuple of 2 element that admit a dictionnary of header and a body"""
        _logger.info("post change password")

        w_new = self.change_password(a_body["login"], a_body["password"], a_body["new_password"])
        if w_new is not None:
            return {}, {
                "login": a_body
            }

        _logger.info("post change password failed")
        return None, None


    def put(self, a_header, a_params, a_body):
        return None

    def get(self, a_header, a_params):
        return None

    def delete(self, a_header, a_params):
        return None

    @Validate
    def validate(self, context):
        _logger.info("ChangePasswordService validating")

        _logger.info("ChangePasswordService validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("ChangePasswordService invalidating")

        _logger.info("ChangePasswordService invalidated")


@ComponentFactory('LoginCookieService-Factory')
@Provides(specifications=[IService.name, YCappuccino.name,ILoginService.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_manager_login", IManager.name, spec_filter="'(item_id=login)'")
@Requires("_jwt", IJwt.name)
@Instantiate("LoginCookieService")
class LoginCookieService(AbsService):

    def __init__(self):
        super(LoginCookieService, self).__init__();
        self._manager_login = None
        self._log = None
        self._jwt = None

    def is_secure(self):
        return False

    def get_name(self):
        return "login"

    def post(self, a_header, a_params, a_body):
        """ return tuple of 2 element that admit a dictionnary of header and a body"""

        w_token = self.check_login(a_body["login"], a_body["password"])
        if w_token is not None:
            return {
              "Set-Cookie": "_ycappuccino="+w_token+";Path=/;HttpOnly"
            }, {
                "token":w_token
            }
        return None, None


    def put(self, a_header, a_params, a_body):
        return None

    def get(self, a_header, a_params):
        return None

    def delete(self, a_header, a_params):
        return None

    @Validate
    def validate(self, context):
        _logger.info("LoginCookieService validating")

        _logger.info("LoginCookieService validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("LoginCookieService invalidating")

        _logger.info("LoginCookieService invalidated")
