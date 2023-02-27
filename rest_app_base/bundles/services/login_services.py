#app="all"
import json

from ycappuccino.core.api import IActivityLogger, IService, YCappuccino
from ycappuccino.storage.api import IManager
from ycappuccino.endpoints.api import IJwt
from ycappuccino.rest_app_base.api import ILoginService
from ycappuccino.core.decorator_app import App

import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, Instantiate
import hashlib


_logger = logging.getLogger(__name__)


class AbsService(IService, ILoginService):

    def __init__(self):
        super(IService, self).__init__();
        self._manager_login = None
        self._manager_account = None
        self._manager_role_account = None
        self._log = None
        self._jwt = None




    def change_password(self, a_login, a_password, a_new_password):
        """ return tuple of 2 element that admit a dictionnary of header and a body"""
        self._log.info("change password")

        w_login = self._manager_login.get_one("login", a_login)

        w_concat = "{}{}".format(w_login.__dict__["_salt"], a_password).encode("utf-8")
        result = hashlib.md5(w_concat).hexdigest()

        if w_login.__dict__["_password"] == result:
            w_login.password(a_new_password)
            self._log.info(" password changed")

            return self._manager_login.up_sert_model(w_login._id, w_login)

        return None


    def check_login(self, a_login, a_password):
        """ return tuple of 2 element that admit a dictionnary of header and a body"""
        w_login = self._manager_login.get_one("login",  a_login)

        w_filter = json.dumps({"login.ref":w_login._id})
        w_account = self._manager_account.get_many( "account", a_params={"filter":w_filter})
        if w_account is not None and len(w_account)>0:
            w_filter = json.dumps({"account.ref":w_account[0]._id})

            w_role_account = self._manager_role_account.get_many( "roleAccount", a_params={"filter":w_filter})
            w_filter = json.dumps({"role.ref":w_role_account[0]._id})

            w_role_permissions = self._manager_role_account.get_many( "rolePermission", a_params={"filter":w_filter})

            w_concat = "{}{}".format(w_login._salt, a_password).encode("utf-8")
            result = hashlib.md5(w_concat).hexdigest()

            if w_login._password == result:
                w_token = self._jwt.generate(w_account[0], w_role_account[0], w_role_permissions)
                return w_token
        return None

@ComponentFactory('LoginService-Factory')
@Provides(specifications=[IService.name, YCappuccino.name,ILoginService.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_manager_login", IManager.name, spec_filter="'(item_id=login)'")
@Requires("_manager_account", IManager.name, spec_filter="'(item_id=account)'")
@Requires("_manager_role_account", IManager.name, spec_filter="'(item_id=roleAccount)'")
@Requires("_jwt", IJwt.name)
@Instantiate("LoginService")
@App(name="ycappuccino.rest-app")

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

    def post(self, a_header, a_url_path, a_body):
        """ return tuple of 2 element that admit a dictionnary of header and a body"""

        w_token = self.check_login(a_body["login"], a_body["password"])
        if w_token is not None:
            return {},{
                "token": w_token
            }
        return None, None


    def get(self, a_header, a_url_path):
        return self.post(a_header, a_url_path, None)

    def delete(self, a_header, a_url_path):
        return self.post(a_header, a_url_path, None)

    @Validate
    def validate(self, context):
        self._log.info("LoginService validating")

        self._log.info("LoginService validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("LoginService invalidating")

        self._log.info("LoginService invalidated")




@ComponentFactory('ChangePasswordService-Factory')
@Provides(specifications=[IService.name, YCappuccino.name,ILoginService.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_manager_login", IManager.name, spec_filter="'(item_id=login)'")
@Requires("_jwt", IJwt.name)
@Instantiate("ChangePasswordService")
@App(name="ycappuccino.rest-app")

class ChangePasswordService(AbsService):

    def __init__(self):
        super(ChangePasswordService, self).__init__();
        self._manager_login = None
        self._log = None


    def is_secure(self):
        return True


    def get_name(self):
        return "change_password"

    def post(self, a_header, a_url_path, a_body):
        """ return tuple of 2 element that admit a dictionnary of header and a body"""
        self._log.info("post change password")

        w_new = self.change_password(a_body["login"], a_body["password"], a_body["new_password"])
        if w_new is not None:
            return {}, {
                "login": a_body
            }

        self._log.info("post change password failed")
        return None, None


    def put(self, a_header, a_url_path, a_body):
        return None

    def get(self, a_header, a_url_path):
        return None

    def delete(self, a_header, a_url_path):
        return None

    @Validate
    def validate(self, context):
        self._log.info("ChangePasswordService validating")

        self._log.info("ChangePasswordService validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("ChangePasswordService invalidating")

        self._log.info("ChangePasswordService invalidated")


@ComponentFactory('LoginCookieService-Factory')
@Provides(specifications=[IService.name, YCappuccino.name,ILoginService.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_manager_login", IManager.name, spec_filter="'(item_id=login)'")
@Requires("_manager_account", IManager.name, spec_filter="'(item_id=account)'")
@Requires("_manager_role_account", IManager.name, spec_filter="'(item_id=roleAccount)'")
@Requires("_jwt", IJwt.name)
@Instantiate("LoginCookieService")
@App(name="ycappuccino.rest-app")

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

    def post(self, a_header, a_url_path, a_body):
        """ return tuple of 2 element that admit a dictionnary of header and a body"""

        w_token = self.check_login(a_body["login"], a_body["password"])
        if w_token is not None:
            return {
              "Set-Cookie": "_ycappuccino="+w_token+";Path=/;HttpOnly"
            }, {
                "token":w_token
            }
        return None, None


    def put(self, a_header, a_url_path, a_body):
        return None

    def get(self, a_header, a_url_path):
        return None

    def delete(self, a_header, a_url_path):
        return None

    @Validate
    def validate(self, context):
        self._log.info("LoginCookieService validating")

        self._log.info("LoginCookieService validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("LoginCookieService invalidating")

        self._log.info("LoginCookieService invalidated")
