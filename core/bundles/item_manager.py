from ycappuccino.core.api import IItemManager, IActivityLogger, IStorage, IConfiguration, YCappuccino
from ycappuccino.core.bundles.managers import AbsManager
import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property, Provides, Instantiate, BindField, UnbindField
from pelix.ipopo.constants import use_ipopo

import ycappuccino.core.framework as framework

import ycappuccino.core.model.decorators

_logger = logging.getLogger(__name__)


@ComponentFactory('ItemManager-Factory')
@Provides(specifications=[IItemManager.name, YCappuccino.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_storage", IStorage.name, optional=True)
@Requires("_config", IConfiguration.name)
@Property('_item_id', "item", "item")
@Property('_is_secure', "secure", True)
@Instantiate("itemManager")
class ItemManager(IItemManager, AbsManager):

    def __init__(self):
        super(ItemManager, self).__init__();
        super(AbsManager, self).__init__();
        self._log = None
        self._item_id = "item"
        self._item = None
        self._config = None
        self._storage = None
        self._item_manager = None
        self._is_secure = False
        self._managers = None
        self._map_managers = {}
        self._context = None

    @BindField("_managers")
    def bind_manager(self, field, a_manager, a_service_reference):
        w_item_id = a_manager.getItem().id
        self._map_managers[w_item_id] = a_manager

    @UnbindField("_managers")
    def unbind_manager(self, field, a_manager, a_service_reference):
        w_item_id = a_manager.getItem().id
        self._map_managers[w_item_id] = None

    def load_item(self):
        """ """
        for w_item in ycappuccino.core.model.decorators.get_map_items():
            if w_item.id not in self._map_managers:

                # instanciate a component regarding the manager factory to use by item and default manage can be multi item
                with use_ipopo(self._context) as ipopo:
                    # use the iPOPO core service with the "ipopo" variable
                    ipopo.instantiate("Manager-Factory", "Manager-{}".format(w_item.id),
                                      {"item_id": w_item.id, "item": w_item, "secureRead": w_item.secureRead,"secureWrite": w_item.secureWrite })

            # create a manager component and create it if it's doesn't already exists
        # TODO load data from file and database
        # load item from data base if exists
        # load item from files

    @Validate
    def validate(self, context):
        _logger.info("Manager validating")
        try:
            self._context = context
            self._item = self.get_one(self._item_id)
            framework.set_item_manager(self)

        except Exception as e:
            _logger.error("Manager Error {}".format(e))
            _logger.exception(e)

        _logger.info("Manager validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("Manager invalidating")
        try:
            self._item = None
        except Exception as e:
            _logger.error("Manager Error {}".format(e))
            _logger.exception(e)
        _logger.info("Manager invalidated")
