from pelix.ipopo.constants import use_ipopo
from ycappuccino.core.api import IManager, IActivityLogger, IStorage, ITrigger, IDefaultManager
from ycappuccino.core.model.model import Model
from ycappuccino.core.model.utils import Proxy
import json
import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Property,  Invalidate, Provides, BindField, UnbindField, \
    Instantiate

_logger = logging.getLogger(__name__)


class AbsManager(IManager):

    def __init__(self):
        super(IManager, self).__init__();
        self._log = None
        self._items = {}
        self._items_class = {}
        self._items_plural = {}
        self._triggers = None
        self._loaded = False
        self._storage = None

    def add_item(self, a_item, a_bundle_context):
        """ add item in map manage by the manager"""
        self._items[a_item.id] = a_item
        self._items_class[a_item._class] = a_item
        self._items_plural[a_item.plural] = a_item
        self.create_proxy_manager(a_item.id,a_bundle_context)

    def create_proxy_manager(self, a_item_id, a_bundle_context):

        with use_ipopo(a_bundle_context) as ipopo:
            # use the iPOPO core service with the "ipopo" variable
            ipopo.instantiate("Manager-Proxy-Factory", "Manager-Proxy-{}".format(a_item_id),
                              {"item_id": a_item_id })


    def get_item_ids(self):
        """ return list of item id"""

        ids = []
        for w_item in self._items.values():
            ids.append(w_item.id)
        return ids

    def get_map_item_ids_plural(self):
        """ return dict of plural name regarding item_id"""
        ids = {}
        for w_item in self._items.values():
            ids[w_item.id]=w_item.plural
        return ids

    def get_item_ids_plural(self):
        """ return dict of plural name regarding item_id"""
        ids = []
        for w_item in self._items.values():
            ids.append(w_item.plural)
        return ids

    def is_secureRead(self):
        """ return dict of secureRead name regarding item_id"""
        ids = {}
        for w_item in self._items.values():
            ids[w_item.id] = w_item.secureRead
        return ids

    def is_secureWrite(self):
        """ return dict of secureRead name regarding item_id"""
        ids = {}
        for w_item in self._items.values():
            ids[w_item.id] = w_item.secureWrite
        return ids

    def get_one(self, a_item_plural_id,  a_id):
        w_result = None
        if self._storage is not None:
            w_item = self._items_plural[a_item_plural_id]
            if w_item is not None:
                res = self._storage.get_one(w_item.collection, a_id)
                if res is not None:
                    for w_model in res:
                        w_result = Model(w_model)
        return w_result

    def get_many(self, a_item_plural_id, a_params):
        w_result = []
        if self._storage is not None:
            w_item = self._items_plural[a_item_plural_id]
            if w_item is not None:
                w_filter = {}
                if a_params is not None and "filter" in a_params:
                    w_filter = json.loads(a_params["filter"])
                res = self._storage.get_many(w_item.collection, w_filter)
                if res is not None:
                    for w_model in res:
                        w_result.append(Model(w_model))
        return w_result

    def up_sert(self, a_item_plural_id, a_id, a_new_field):
        """ update (insert if no exists) a collection with bson (a_new_field) for the id specify in parameter and return the model create """

        if self._storage is not None:
            w_item = self._items_plural[a_item_plural_id]

            if w_item is not None:
                res = self._storage.up_sert(w_item.collection, a_id, a_new_field)
                if res is not None:
                    return Model(res)
        return None

    def up_sert_model(self, a_id, a_model):
        """ update (insert if no exists) a collection with bson (a_new_field) for the id specify in parameter and return the model create """

        if self._storage is not None:
            w_item = self._items_class[a_model.__class__.__name__]

            if w_item is not None:
                res = self._storage.up_sert(w_item.collection, a_id, a_new_field)
                if res is not None:
                    return Model(res)
        return None

    def up_sert_many(self, a_item_id,a_new_fields):
        res = []

        for w_dict in a_new_fields:
            w_res = self.up_sert(a_item_id, w_dict.id,w_dict)

            if w_res is not None:
                res.append(w_res)
        return res

    def up_sert_many_model(self,  a_new_models):
        res = []

        for w_dict in a_new_models:
            w_res = self.up_sert_model( w_dict.id, w_dict)

            if w_res is not None:
                res.append(w_res)
        return res

    def delete(self, a_item_plural_id, a_id):
        if self._storage is not None:
            w_item = self._items_plural[a_item_plural_id]

            if w_item is not None:
                res = self._storage.delete(w_item.collection, a_id)
                if res is not None:
                    return Model(res)
        return None



    def delete_many(self, a_item_plural_id, a_filter):
        if self._storage is not None:
            w_item = self._items_plural[a_item_plural_id]

            if w_item is not None:
                res = self._storage.delete_many(w_item.collection, a_filter)
                if res is not None:
                    return Model(res)
        return None

@ComponentFactory('Manager-Proxy-Factory')
@Provides(IManager.name)
@Property('_item_id', "item_id", "model")
@Requires('_default_manager', IDefaultManager.name)
class ProxyManager(IManager, Proxy):

    def __init__(self):
        super(ProxyManager, self).__init__()
        self._item_id = None
        self._obj = None

    @Validate
    def validate(self, context):
        _logger.info("Manager default validating")
        try:
            self._obj = self._default_manager
            self._obj._objname = "proxy-{}".format(self._item_id)
        except Exception as e:
            _logger.error("Manager Error default".format(e))
            _logger.exception(e)

        _logger.info("Manager default validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("Manager default invalidating")

        _logger.info("Manager default invalidated")


@ComponentFactory('DefaultManager-Factory')
@Provides(IDefaultManager.name)
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_storage",IStorage.name,optional=True)
@Requires('_list_trigger', ITrigger.name, aggregate=True, optional=True)
@Instantiate("Manager-default")
class DefaultManager(AbsManager):

    def __init__(self):
        super(DefaultManager, self).__init__()
        self._list_trigger = None
        self._map_trigger = {}



    @BindField("_list_trigger")
    def bind_trigger(self, a_field, a_service, a_service_reference):
        if a_service is not None and a_service.get_item() == self._item_id:
            self._map_trigger[a_service.get_name()] = a_service

    @UnbindField("_list_trigger")
    def un_bind_trigger(self, a_field, a_service, a_service_reference):
        if a_service is not None and a_service.get_item() == self._item_id:
            if a_service.get_name() in self._map_trigger[a_service.get_name()]:
                del self._map_trigger[a_service.get_name()]

    @Validate
    def validate(self, context):
        _logger.info("Manager default validating")
        try:
            pass
        except Exception as e:
            _logger.error("Manager Error default".format(e))
            _logger.exception(e)

        _logger.info("Manager default validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("Manager default invalidating")

        _logger.info("Manager default invalidated")
