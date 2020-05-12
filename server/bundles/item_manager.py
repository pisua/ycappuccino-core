from server.api import IItemManager, IActivityLogger, IStorage, IConfiguration
from server.bundles.managers import AbsManager
import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property, Provides, Instantiate
from pelix.ipopo.constants import use_ipopo

_logger = logging.getLogger(__name__)
import jsoncomment, glob

@ComponentFactory('ItemManager-Factory')
@Provides(IItemManager.name)
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_storage", IStorage.name)
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

    def load_item(self, a_module):
        """ """
        w_base_dir = self._config.get_base()
        w_module_dir = w_base_dir+"/models/"+a_module
        w_files = glob.iglob(w_module_dir+"/*.js")
        for w_file in w_files:
            if w_id not in self._map_managers:
                try:
                    w_json = jsoncomment.load(w_file)
                    w_item = w_json

                except Exception as e:
                    _logger.error("Manager load_item file {} Error {} ".format(w_file, e))
                    _logger.exception(e)
                else:
                    w_id = w_json["_id"]
                    w_version = w_json["version"]
                    w_stored = self._storage.get_one("items", w_id)
                    w_item = w_stored
                    if w_stored is None or w_stored is not None and w_stored["version"] < w_version:
                        # need to store the new version
                        self._storage.up_sert("items", w_id, w_json)

                with use_ipopo(self._context) as ipopo:
                    # use the iPOPO core service with the "ipopo" variable
                    ipopo.instantiate("Manager-Factory", "Manager-{}".format(w_item["_id"]),
                                      {"item": w_item["_id"], "secure": w_item["secure"]})

            # create a manager component and create it if it's doesn't already exists
        # TODO load data from file and database
        # load item from data base if exists
        # load item from files

    @Validate
    def validate(self, context):
        _logger.info("Manager validating")
        try:
            self._context = context
            self.load_item()
            self._item = self.get_one(self._item_id)
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
