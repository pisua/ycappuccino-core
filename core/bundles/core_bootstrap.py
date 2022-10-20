from ycappuccino.core.api import IActivityLogger, IManager, IBootStrap, YCappuccino
import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property, Provides, Instantiate, BindField, UnbindField
from pelix.ipopo.constants import use_ipopo

import ycappuccino.core.framework as framework

import ycappuccino.core.model.decorators
from ycappuccino.core.model.account import Account
from ycappuccino.core.model.login import Login
from ycappuccino.core.model.role import Role
from ycappuccino.core.model.ui.client_path import ClientPath


_logger = logging.getLogger(__name__)


@ComponentFactory('AccountBootStrap-Factory')
@Provides(specifications=[IBootStrap.name, YCappuccino.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_manager_account", IManager.name, spec_filter="'(item_id=account)'")
@Requires("_manager_login", IManager.name, spec_filter="'(item_id=login)'")
@Requires("_manager_role", IManager.name, spec_filter="'(item_id=role)'")
@Requires("_manager_client_path", IManager.name, spec_filter="'(item_id=clientPath)'")
@Property("_id", "id", "core")

@Instantiate("AccountBootStrap")
class AccountBootStrap(IBootStrap):

    def __init__(self):
        super(IBootStrap, self).__init__();
        self._manager_account =None
        self._manager_login =None
        self._manager_role =None
        self._manager_client_path = None
        self._log =None
        self._id = "core"

    def get_id(self):
        return self._id

    def bootstrap(self):

        w_admin_login = Login()
        w_admin_login.id("superadmin")
        w_admin_login.login("superadmin")
        w_admin_login.password("admin")

        w_admin_role = Role()
        w_admin_role.id("superadmin")
        w_admin_role.name("superadmin")

        w_admin_account = Account({})
        w_admin_account.id("superadmin")
        w_admin_account.name("superadmin")
        w_admin_account.login("superadmin")
        w_admin_account.role("superadmin")

        self._manager_role.up_sert_model("superadmin", w_admin_role)
        self._manager_account.up_sert_model("superadmin", w_admin_account)
        if self._manager_login.get_one("login","superadmin") is None:
            self._manager_login.up_sert_model("superadmin", w_admin_login)

        w_client_path_default = ClientPath()
        w_client_path_default.id("default")
        w_client_path_default.path("/")
        w_client_path_default.subpath("client")
        w_client_path_default.priority(0)
        w_client_path_default.secure(False)

        self._manager_client_path.up_sert_model("default", w_client_path_default)

        w_client_path_swagger = ClientPath()
        w_client_path_swagger.id("swagger")
        w_client_path_swagger.path("/swagger")
        w_client_path_swagger.subpath("swagger")
        w_client_path_swagger.priority(1)

        w_client_path_swagger.secure(False)

        self._manager_client_path.up_sert_model("swagger", w_client_path_swagger)

        w_client_path_swagger = ClientPath()
        w_client_path_swagger.id("simpleform")
        w_client_path_swagger.path("/simpleform")
        w_client_path_swagger.subpath("simpleform")
        w_client_path_swagger.priority(1)

        w_client_path_swagger.secure(False)

        self._manager_client_path.up_sert_model("simpleform", w_client_path_swagger)

    @Validate
    def validate(self, context):
        _logger.info("AccountBootStrap validating")
        try:
            self.bootstrap()
        except Exception as e:
            _logger.error("AccountBootStrap Error {}".format(e))
            _logger.exception(e)

        _logger.info("AccountBootStrap validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("AccountBootStrap invalidating")
        try:
            pass
        except Exception as e:
            _logger.error("AccountBootStrap Error {}".format(e))
            _logger.exception(e)
        _logger.info("AccountBootStrap invalidated")
