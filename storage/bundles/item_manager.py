#app="all"
from ycappuccino.core.api import  IActivityLogger, IConfiguration, YCappuccino,  IProxyManager
from ycappuccino.storage.bundles.managers import AbsManager, ProxyManager
from ycappuccino.storage.api import IItemManager,  IStorage,   IManager,  IDefaultManager
import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property, Provides, Instantiate, BindField, UnbindField
from ycappuccino.core.decorator_app import App

import ycappuccino.core.framework as framework

import ycappuccino.storage.models.decorators

_logger = logging.getLogger(__name__)


class CreateManagerProxy(object):

    def __init__(self, a_name, a_map_managers, a_default_manager,  a_context):
        self._name = a_name
        self._map_managers = a_map_managers
        self._default_manager = a_default_manager
        self._context = a_context

    def run(self):
        """ main loop for the thread that call the run"""


@ComponentFactory('ItemManager-Factory')
@Provides(specifications=[IItemManager.name, YCappuccino.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_storage", IStorage.name, optional=True)
@Requires("_config", IConfiguration.name)
@Property('_is_secure', "secure", True)
@Requires("_managers", specification=IManager.name, aggregate=True, optional=True)
@Requires("_proxies", specification=IProxyManager.name, aggregate=True, optional=True)
@Requires("_default_manager", specification=IDefaultManager.name)
@Instantiate("itemManager")
@App(name="ycappuccino.storage")
class ItemManager(IItemManager, AbsManager):

    def __init__(self):
        super(ItemManager, self).__init__();
        super(AbsManager, self).__init__();
        self._log = None
        self._config = None
        self._storage = None
        self._managers = None
        self._map_managers = {}

        self._default_manager = None
        self._context = None



    def get_one(self, a_item_id,  a_id):
        w_dicts = ycappuccino.storage.models.decorators.get_map_items_emdpoint()
        if a_id in w_dicts:
            w_result = w_dicts[a_id]
        return w_result

    def get_many(self, a_item_id, a_params):
        w_result = ycappuccino.storage.models.decorators.get_map_items_emdpoint()

        return w_result

    def get_item_from_id_plural(self,a_item_plural):
        """ return list of item id"""
        return {
            "id":"item",
            "secureRead":False
        }

    @BindField("_managers")
    def bind_manager(self, field, a_manager, a_service_reference):
        self._context = a_service_reference._ServiceReference__bundle._Bundle__context
        for w_item_id in a_manager.get_item_ids():
            if w_item_id not in self._map_managers:
                self._map_managers[w_item_id] = a_manager
                if not isinstance(a_manager,ProxyManager):
                    w_item = ycappuccino.storage.models.decorators.get_item(w_item_id)
                    a_manager.add_item(w_item, self._context)

    @BindField("_default_manager")
    def bind_default_manager(self, field, a_manager, a_service_reference):
        self._context = a_service_reference._ServiceReference__bundle._Bundle__context
        self._default_manager = a_manager
        #self.load_item()

    @UnbindField("_default_manager")
    def unbind_default_manager(self, field, a_manager, a_service_reference):
        self._default_manager = None

    @UnbindField("_managers")
    def unbind_manager(self, field, a_manager, a_service_reference):

        for w_item_id in a_manager.get_item_ids():
            self._map_managers[w_item_id] = None


    def load_item(self):
        """ """
        for w_item in ycappuccino.storage.models.decorators.get_map_items():
            if "id" in w_item.keys() and  w_item["id"] not in self._map_managers and self._default_manager is not None:
                # instanciate a component regarding the manager factory to use by item and default manage can be multi item
                if not w_item["abstract"] :
                    self._log.info("add item {}".format(w_item["id"]))
                    self._default_manager.add_item(w_item, self._context)
            else:
                print("error")

    @Validate
    def validate(self, context):
        self._log.info("Manager validating")
        try:
            self._context = context
            framework.set_item_manager(self)
        except Exception as e:
            self._log.error("Manager Error {}".format(e))
            self._log.exception(e)

        self._log.info("Manager validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("Manager invalidating")

        self._log.info("Manager invalidated")
