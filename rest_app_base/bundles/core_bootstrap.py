#app="all"
from ycappuccino.core.api import IActivityLogger,  YCappuccino
from ycappuccino.storage.api import IManager, IBootStrap
from ycappuccino.core.decorator_app import App

import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property, Provides, Instantiate

from ycappuccino.rest_app_base.models.account import Account
from ycappuccino.rest_app_base.models.login import Login
from ycappuccino.rest_app_base.models.role import Role
from ycappuccino.rest_app_base.models.ui.client_path import ClientPath
from ycappuccino.rest_app_base.models.role_permission import RolePermission
from ycappuccino.rest_app_base.models.role_account import RoleAccount

from ycappuccino.endpoints.api import IJwt

_logger = logging.getLogger(__name__)


@ComponentFactory('AccountBootStrap-Factory')
@Provides(specifications=[IBootStrap.name, YCappuccino.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_manager_account", IManager.name, spec_filter="'(item_id=account)'")
@Requires("_manager_role_permission", IManager.name, spec_filter="'(item_id=rolePermission)'")
@Requires("_manager_role_account", IManager.name, spec_filter="'(item_id=roleAccount)'")
@Requires("_manager_login", IManager.name, spec_filter="'(item_id=login)'")
@Requires("_manager_role", IManager.name, spec_filter="'(item_id=role)'")
@Requires("_manager_client_path", IManager.name, spec_filter="'(item_id=clientPath)'")
@Requires("_jwt", IJwt.name)
@Property("_id", "id", "core")
@Instantiate("AccountBootStrap")
@App(name="ycappuccino.rest-app")

class AccountBootStrap(IBootStrap):

    def __init__(self):
        super(IBootStrap, self).__init__();
        self._manager_account =None
        self._manager_login =None
        self._manager_role =None
        self._manager_role_permission =None
        self._manager_role_account =None
        self._jwt =None

        self._manager_client_path = None
        self._log =None
        self._id = "core"

    def get_id(self):
        return self._id

    def bootstrap(self):

        w_subject = self._jwt.get_token_subject("bootstrap", "system")

        w_admin_login = Login()
        w_admin_login.id("superadmin")
        w_admin_login.login("superadmin")
        w_admin_login.password("client_pyscript_core")

        w_admin_role = Role()
        w_admin_role.id("superadmin")
        w_admin_role.name("superadmin")

        w_admin_account = Account({})
        w_admin_account.id("superadmin")
        w_admin_account.name("superadmin")
        w_admin_account.login("superadmin")
        w_admin_account.role("superadmin")


        w_admin_role_permission = RolePermission({})
        w_admin_role_permission.id("superadmin")
        w_admin_role_permission.role("superadmin")
        w_admin_role_permission.rights(["*:*:*"])

        w_admin_role_account = RoleAccount({})
        w_admin_role_account.id("superadmin")
        w_admin_role_account.role("superadmin")
        w_admin_role_account.account("superadmin")
        w_admin_role_account.organization("system")

        self._manager_role.up_sert_model("superadmin", w_admin_role, w_subject)
        self._manager_account.up_sert_model("superadmin", w_admin_account, w_subject)
        self._manager_role_permission.up_sert_model("superadmin", w_admin_role_permission, w_subject)
        self._manager_role_account.up_sert_model("superadmin", w_admin_role_account, w_subject)

        if self._manager_login.get_one("login","superadmin", w_subject) is None:
            self._manager_login.up_sert_model("superadmin", w_admin_login, w_subject)

        w_client_path_default = ClientPath()
        w_client_path_default.id("default")
        w_client_path_default.path("/")
        w_client_path_default.subpath("client")
        w_client_path_default.priority(0)
        w_client_path_default.secure(False)

        self._manager_client_path.up_sert_model("default", w_client_path_default, w_subject)


        w_client_path_pyscript_core = ClientPath()
        w_client_path_pyscript_core.id("client_pyscript_core")
        w_client_path_pyscript_core.path("/pyscriptcore")
        w_client_path_pyscript_core.subpath("endpoints_storage/client_pyscript_core")
        w_client_path_pyscript_core.priority(1)
        w_client_path_pyscript_core.type("pyscript")
        w_client_path_pyscript_core.core(True)
        w_client_path_pyscript_core.secure(False)

        self._manager_client_path.up_sert_model("client_pyscript_core", w_client_path_pyscript_core, w_subject)

    @Validate
    def validate(self, context):
        self._log.info("AccountBootStrap validating")
        try:
            self.bootstrap()
        except Exception as e:
            self._log.error("AccountBootStrap Error {}".format(e))
            self._log.exception(e)

        self._log.info("AccountBootStrap validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("AccountBootStrap invalidating")
        try:
            pass
        except Exception as e:
            self._log.error("AccountBootStrap Error {}".format(e))
            self._log.exception(e)
        self._log.info("AccountBootStrap invalidated")
