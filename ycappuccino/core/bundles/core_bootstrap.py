from ycappuccino.core.api import IActivityLogger, IManager, IManagerBootStrapData, YCappuccino
import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property, Provides, Instantiate, BindField, UnbindField
from pelix.ipopo.constants import use_ipopo

import ycappuccino.core.framework as framework

import ycappuccino.core.model.decorators
from ycappuccino.core.model.account import Account
from ycappuccino.core.model.login import Login

_logger = logging.getLogger(__name__)


@ComponentFactory('AccountBootStrap-Factory')
@Provides(specifications=[IManagerBootStrapData.name, YCappuccino.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_manager_account", IManager.name, spec_filter="'(item_id=account)'")
@Requires("_manager_login", IManager.name, spec_filter="'(item_id=login)'")
@Requires("_manager_role", IManager.name, spec_filter="'(item_id=role)'")
@Instantiate("AccountBootStrap")
class AccountBootStrap(IManagerBootStrapData):

    def __init__(self):
        super(IManagerBootStrapData, self).__init__();
        self._manager_account =None
        self._manager_login =None
        self._manager_role =None
        self._log =None

    def bootstrap(self):

        w_admin_account = Account({})
        w_admin_account.name("admin")
        w_admin_login = Login()
        w_admin_login.login("admin")
        w_admin_login.password("Danst0ncu1")
        w_admin_account.login("admin")
        self._manager_account.up_sert("admin", w_admin_account)
        if self._manager_login.get_one("admin") is None:
            self._manager_login.up_sert("admin", w_admin_login)

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
