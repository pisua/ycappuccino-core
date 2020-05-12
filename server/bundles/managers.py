from server.api import IManager, IActivityLogger, IItemManager, IStorage
from server.model.model import Model

import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property, Provides

_logger = logging.getLogger(__name__)


class AbsManager(IManager):

    def __init__(self):
        super(IManager, self).__init__();
        self._log = None
        self._item_id = None
        self._item = None
        self._storage = None
        self._item_manager = None
        self._is_secure = False

    def get_item(self):
        return self._item

    def is_secure(self):
        return self._is_secure

    def get_one(self, a_id):
        if self._item is not None:
            res = self._storage.get_one(self._item.get_collection_name(), a_id)
            if res is not None:
                return Model(res)
        return None

    def get_many(self, a_params):
        pass

    def up_sert(self, a_id, a_new_field):
        pass

    def up_sert_many(self, a_params, a_new_field):
        pass

    def delete(self, a_id):
        pass

    def delete_many(self, a_params):
        pass


@ComponentFactory('Manager-Factory')
@Provides(IManager.name)
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_item_manager",IItemManager.name)
@Requires("_storage",IStorage.name)
@Property('_item_id', "item", "model")
@Property('_is_secure', "secure", False)
class Manager(AbsManager):

    def __init__(self):
        super(AbsManager, self).__init__()


    @Validate
    def validate(self, context):
        _logger.info("Manager validating")
        try:
            self._item = self._item_manager.get_one(self._item_id)
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
