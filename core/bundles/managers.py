from ycappuccino.core.api import IManager, IActivityLogger, IItemManager, IStorage, ITrigger
from ycappuccino.core.model.model import Model
import json
import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property, Provides

_logger = logging.getLogger(__name__)


class AbsManager(IManager):

    def __init__(self):
        super(IManager, self).__init__();
        self._log = None
        self._item = None
        self._item_id = None
        self._triggers = None

        self._storage = None
        self._item_manager = None
        self._is_secureRead = False
        self._is_secureWrite = False

    def get_item_id(self):
        return self._item.id

    def get_item_id_plural(self):
        return self._item.collection

    def is_secureRead(self):
        return self._is_secureRead

    def is_secureWrite(self):
        return self._is_secureWrite

    def get_one(self, a_id):
        w_result = None
        if self._storage is not None:

            if self._item is not None:
                res = self._storage.get_one(self._item.collection, a_id)
                if res is not None:
                    for w_model in res:
                        w_result = Model(w_model)
        return w_result

    def get_many(self, a_params):
        w_result = []
        if self._storage is not None:
            if self._item is not None:
                w_filter = {}
                if a_params is not None and "filter" in a_params:
                    w_filter = json.loads(a_params["filter"])
                res = self._storage.get_many(self._item.collection, w_filter)
                if res is not None:
                    for w_model in res:
                        w_result.append(Model(w_model))
        return w_result

    def up_sert(self, a_id, a_new_field):
        """ update (insert if no exists) a collection with bson (a_new_field) for the id specify in parameter and return the model create """
        if self._storage is not None:
            if self._item is not None:
                res = self._storage.up_sert(self._item.collection, a_id, a_new_field)
                if res is not None:
                    return Model(res)
        return None


    def up_sert_many(self, a_new_fields):
        res = []
        if self._item is not None:
            for w_dict in a_new_fields:


                w_res = self.up_sert(w_dict.id,w_dict)
                if w_res is not None:
                    res.append(w_res)
        return res

    def delete(self, a_id):
        if self._storage is not None:

            if self._item is not None:
                res = self._storage.delete(self._item.collection, a_id)
                if res is not None:
                    return Model(res)
        return None

    def delete_many(self, a_filter):
        if self._storage is not None:

            if self._item is not None:
                res = self._storage.delete_many(self._item.collection, a_filter)
                if res is not None:
                    return Model(res)
        return None


@ComponentFactory('Manager-Factory')
@Provides(IManager.name)
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_item_manager",IItemManager.name)
@Requires("_storage",IStorage.name,optional=True)
@Property('_item_id', "item_id", "model")
@Property('_item', "item", None)
@Property('_is_secureRead', "secureRead", False)
@Property('_is_secureWrite', "secureWrite", False)
@Requires('_list_trigger', ITrigger.name, aggregate=True, optional=True)
class Manager(AbsManager):

    def __init__(self):
        super(AbsManager, self).__init__()
        self._list_trigger = None
        self._map_trigger = {}

    @BindField("_list_trigger")
    def bind_trigger(self, a_field, a_service, a_service_reference):
        if a_service is not None and a_service.get_item() == self._item_id:
            self._map_trigger[a_service.get_name()] = a_service

    @UnBindField("_list_trigger")
    def un_bind_trigger(self, a_field, a_service, a_service_reference):
        if a_service is not None and a_service.get_item() == self._item_id:
            if a_service.get_name() in self._map_trigger[a_service.get_name()]:
                del self._map_trigger[a_service.get_name()]

    @Validate
    def validate(self, context):
        _logger.info("Manager {} validating".format(self._item.id))
        try:
            pass
        except Exception as e:
            _logger.error("Manager Error {}".format(e))
            _logger.exception(e)

        _logger.info("Manager {} validated".format(self._item.id))

    @Invalidate
    def invalidate(self, context):
        _logger.info("Manager {} invalidating".format(self._item.id))

        _logger.info("Manager {} invalidated".format(self._item.id))
