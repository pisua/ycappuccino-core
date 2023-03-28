#app="all"
from pelix.ipopo.constants import use_ipopo
from ycappuccino.core.api import  IActivityLogger
from ycappuccino.storage.api import IManager, IStorage, ITrigger, IDefaultManager, IOrganizationManager
from ycappuccino.storage.models.model import Model
from ycappuccino.core.models.decorators import get_sons_item, get_sons_item_id
from ycappuccino.core.models.utils import Proxy
import json
import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Property,  Invalidate, Provides, BindField, UnbindField, \
    Instantiate
from ycappuccino.core.decorator_app import App

from ycappuccino.storage.api import IFilter

from ycappuccino.storage.api import IUploadManager

_logger = logging.getLogger(__name__)


class AbsManager(IManager):

    def __init__(self):
        super(IManager, self).__init__();
        self._log = None
        self._items = {}
        self._items_class = {}
        self._items_plural = {}
        self._triggers = None
        self._map_triggers = {}

        self._loaded = False
        self._storage = None
        self._list_component = {}
        self._filters = None

    def add_item(self, a_item, a_bundle_context):
        """ add item in map manage by the manager"""
        self._items[a_item["id"]] = a_item
        self._items_class[a_item["_class"]] = a_item
        self._items_plural[a_item["plural"]] = a_item



    def get_item_from_id_plural(self,a_item_plural):
        """ return list of item id"""
        return self._items_plural[a_item_plural]

    def get_item_ids(self):
        """ return list of item id"""

        ids = []
        for w_item in self._items.values():
            ids.append(w_item["id"])
        return ids

    def get_map_item_ids_plural(self):
        """ return dict of plural name regarding item_id"""
        ids = {}
        for w_item in self._items.values():
            ids[w_item["id"]]=w_item["plural"]
        return ids

    def get_item_ids_plural(self):
        """ return dict of plural name regarding item_id"""
        ids = []
        for w_item in self._items.values():
            ids.append(w_item["plural"])
        return ids

    def is_secureRead(self):
        """ return dict of secureRead name regarding item_id"""
        ids = {}
        for w_item in self._items.values():
            ids[w_item["id"]] = w_item["secureRead"]
        return ids

    def is_secureWrite(self):
        """ return dict of secureRead name regarding item_id"""
        ids = {}
        for w_item in self._items.values():
            ids[w_item["id"]] = w_item["secureWrite"]
        return ids


    def _get_lookup_param(self, a_exp):
        w_result = {}
        if "." in a_exp:
            w_target_split = a_exp.split(".")
        else:
            w_target_split = [a_exp]

        w_item_target_id_father = None
        for w_exp in w_target_split:
            w_lookup_params = {}

            w_item_target_id = w_exp
            if "(" in w_exp:
                w_item_target_id = w_exp[0:w_exp.index("(")]
                w_item_target_constraint = w_exp[w_exp.index("(") + 1:w_exp.index(")")]
                w_lookup_params_str = None
                if "|" in w_item_target_constraint:
                    w_lookup_params_str = w_item_target_constraint.split("|")
                else:
                    w_lookup_params_str = [w_item_target_constraint]
                if w_lookup_params_str is not None:
                    for w_elem in w_lookup_params_str:
                        if "=" in w_elem:
                            w_lookup_params[w_elem.split("=")[0]] = w_elem.split("=")[1]
            w_key = w_item_target_id
            w_result_current = w_result
            if w_item_target_id_father is not None:
                w_prefix = None
                for w_father in w_item_target_id_father.split("."):
                    w_result_current = w_result_current[w_father]
                    w_lookup_as = w_result_current["params"]["as"] if "as" in w_result_current["params"].keys() else w_result_current["target"]+ "_doc"
                    w_prefix = w_prefix+"."+w_lookup_as if w_prefix is not None else w_lookup_as
                w_result_current[w_key] = {
                    "target": w_item_target_id,
                    "params": w_lookup_params,
                    "prefix": w_prefix
                }
            else:
                w_result_current[w_key] = {
                    "target": w_item_target_id,
                    "params": w_lookup_params
                }
            w_item_target_id_father = w_item_target_id_father+"."+w_key if w_item_target_id_father is not None else w_key

        return w_result

    def _add_lookup_pipeline(self, a_pipeline, a_item, a_result_elem, a_subject=None):
        w_lookup_params = a_result_elem["params"]
        w_item_target_id = a_result_elem["target"]
        w_prefix = a_result_elem["prefix"]+"." if "prefix" in a_result_elem else ""

        if "refs" in a_item.keys() and w_item_target_id in a_item["refs"]:
            w_doc = "_doc"
            if a_item["refs"][w_item_target_id]["reverse"]:
                w_doc = "_docs"
            w_lookup_as = w_prefix + w_item_target_id + w_doc
            w_lookup_as = w_prefix + w_lookup_params["as"] if "as" in w_lookup_params.keys() else w_lookup_as

            w_prop_lookup = a_item["refs"][w_item_target_id]
            w_item_target = self._items[w_item_target_id]
            # add lookup
            a_pipeline["lookup"].append({
                "$lookup": {
                    "from": w_item_target["collection"],
                    "let": {
                        "localid": "$" + w_prefix + w_prop_lookup["local_field"]
                    },
                    "pipeline": [
                        {
                            "$match": {
                                "$and": [
                                    {
                                        "$expr": {
                                            "$eq": ["$" + w_prop_lookup["foreign_field"], "$$localid"]
                                        }
                                    },
                                    json.loads(w_lookup_params["filter"]) if "filter" in w_lookup_params.keys() else {}
                                ]
                            }
                        }, {
                            "$skip": w_lookup_params["skip"] if "skip" in w_lookup_params.keys() else 0
                        },
                        {
                            "$limit": w_lookup_params["limit"] if "limit" in w_lookup_params.keys() else 50
                        }
                    ],
                    "as": w_lookup_as
                }
            })
            # add undind
            if not a_item["refs"][w_item_target_id]["reverse"]:
                a_pipeline["lookup"].append({
                    "$unwind": {
                        "path": "$" + w_lookup_as,
                        "preserveNullAndEmptyArrays": True
                    }
                })
            for w_elem_key_son in a_result_elem.keys():
                if w_elem_key_son != "params" and w_elem_key_son != "target" and w_elem_key_son != "prefix":
                    # get item
                    self._add_lookup_pipeline(a_pipeline, w_item_target, a_result_elem[w_elem_key_son])

    def _generate_pipeline(self, a_item ,a_filter, a_expand, a_select=None, a_subject=None):
        w_pipeline = None
        w_expand_split = a_expand.split(",")
        w_pipeline = {
            "filter": {},
            "lookup": [],
            "group": [],
            "project": []
        }
        for w_exp in w_expand_split:
            w_result = self._get_lookup_param(w_exp)
            for w_result_elem in w_result.keys():
                self._add_lookup_pipeline(w_pipeline, a_item, w_result[w_result_elem])

        w_pipeline_arr = []
        if w_pipeline is not None:
            if len(w_pipeline["filter"].keys()) > 0:
                w_pipeline_arr.append(w_pipeline["filter"])
            for w_elem in w_pipeline["lookup"]:
                w_pipeline_arr.append(w_elem)

            for w_elem in reversed(w_pipeline["group"]):
                w_pipeline_arr.append(w_elem)

        return w_pipeline_arr

    def _manage_filter(self, a_filter_res, a_tenant):
        if self._filters is not None and len(self._filters):
            for a_filter in self._filters:
                w_filter = a_filter.get_filter(a_tenant)
                a_filter_res[w_filter.key] = w_filter.value

    def get_one(self, a_item_id, a_id, a_params=None, a_subject=None):
        w_result = None
        if self._storage is not None:
            w_item = self._items[a_item_id]
            if w_item is not None:
                w_items = self.get_sons_item_id(w_item)
                w_filter = {
                    "_id": a_id,
                    "_item_id":{
                        "$in":w_items
                    }
                }
                if a_subject is not None:
                    self._manage_filter(w_filter, a_subject["tid"] )

                res = self._storage.get_one(w_item["collection"], w_filter)
                w_result = self._manage_return_result_from_one_instance(w_item, res, a_params)
                self._call_trigger_post("read", w_result)

        return w_result

    def get_aggregate_one(self, a_item_id, a_id, a_params=None, a_subject=None):
        w_result = None
        if self._storage is not None:
            w_item = self._items[a_item_id]
            if w_item is not None:
                w_items = self.get_sons_item_id(w_item)


                if a_params is not None and "expand" in a_params:
                    w_expand = a_params["expand"]
                    w_filter = a_params["filter"] if  a_params.keys() else {}
                    w_filter["_id"] = a_id,
                    w_filter["_item_id"] = {
                        "$in": w_items
                    }

                    self._manage_filter(w_filter, a_subject["tid"])
                    w_pipeline = self._generate_pipeline(w_item, w_filter, w_expand)
                    if w_pipeline is not None:
                        res = self._storage.aggregate(w_item["collection"], w_pipeline)
                        return self._manage_return_result_from_one_instance(w_item, res,a_params)

                w_result = self.get_one(a_item_id, a_id, a_params)
                self._call_trigger_post("read", w_result)

        return w_result


    def _manage_return_result_from_one_instance(self, a_item,  res, a_params, a_aggregate=False):
        w_result = None
        if res is not None:
            w_private_field = False
            if a_params is not None and "content" in a_params:
                if "privateField" in a_params["content"]:
                    w_private_field = True

            for w_model in res:
                if not w_private_field and "private_property" in a_item:
                    # remove private field if not asked
                    for w_priv_prop in a_item["private_property"]:
                        if w_priv_prop in w_model:
                            del w_model[w_priv_prop]
                w_instance = a_item["_class_obj"](w_model)
                w_instance.on_read(a_aggregate)
                w_result = w_instance
        return w_result

    def _manage_return_result_from_many_instance(self, a_item, res, a_params, a_aggregate=False):
        w_result = []
        if res is not None:
            w_private_field = False
            if a_params is not None and "content" in a_params:
                if "privateField" in a_params["content"]:
                    w_private_field = True

            for w_model in res:

                if not w_private_field and "private_property" in a_item:
                    # remove private field if not asked
                    w_model["id"] = w_model["_id"]
                    del w_model["_id"]
                    for w_priv_prop in a_item["private_property"]:
                        if w_priv_prop in w_model:
                            del w_model[w_priv_prop]
                w_instance = a_item["_class_obj"](w_model)
                w_instance.on_read(a_aggregate)
                w_result.append(w_instance)
        return w_result

    def get_schema(self, a_item_id):
        w_schema = self._items[a_item_id]["schema"]
        return w_schema

    def get_empty(self, a_item_id):
        w_empty = self._items[a_item_id]["empty"]
        return w_empty

    def get_sons_item(self, a_item):
        return get_sons_item(a_item["id"])

    def get_sons_item_id(self, a_item):
        return get_sons_item_id(a_item["id"])

    def get_many(self, a_item_id, a_params=None, a_subject=None):
        w_result = []
        if self._storage is not None:
            w_item = self._items[a_item_id]
            if w_item is not None:
                w_filter = {}
                w_sort = None
                w_offset = None
                w_limit = None
                w_sort = None

                if a_params is not None and "filter" in a_params:
                    w_filter = json.loads(a_params["filter"])
                if a_params is not None and "limit" in a_params:
                    w_limit = int(a_params["limit"])
                if a_params is not None and "offset" in a_params:
                    w_offset = int(a_params["offset"])
                if a_params is not None and "sort" in a_params:
                    w_sort = a_params["sort"]

                w_items = self.get_sons_item_id(w_item)

                w_filter["_item_id"] = {
                    "$in":w_items
                }
                if a_subject is not None:
                    self._manage_filter(w_filter, a_subject["tid"] )

                res = self._storage.get_many(w_item["collection"], w_filter, w_offset, w_limit, w_sort)
                w_result = self._manage_return_result_from_many_instance(w_item, res,a_params)
                self._call_trigger_post("read", w_result)

        return w_result

    def get_aggregate_many(self, a_item_id, a_params=None, a_subject=None):
        w_result = []
        if self._storage is not None:
            w_item = self._items[a_item_id]
            if w_item is not None:
                w_filter = {}
                w_sort = None
                w_offset = None
                w_limit = None
                w_sort = None

                if a_params is not None and "filter" in a_params:
                    w_filter = json.loads(a_params["filter"])
                if a_params is not None and "limit" in a_params:
                    w_limit = int(a_params["limit"])
                if a_params is not None and "offset" in a_params:
                    w_offset = int(a_params["offset"])
                if a_params is not None and "sort" in a_params:
                    w_sort = a_params["sort"]

                w_items = self.get_sons_item_id(w_item)


                if a_params is not None and "expand" in a_params:
                    w_expand = a_params["expand"]
                    w_filter = a_params["filter"] if "filter" in a_params.keys() else {}
                    w_filter["_item_id"] = {
                        "$in": w_items
                    }
                    self._manage_filter(w_filter, a_subject["tid"])

                    w_pipeline = self._generate_pipeline(w_item, w_filter, w_expand)
                    if w_pipeline is not None:
                        res = self._storage.aggregate(w_item["collection"], w_pipeline)
                        w_result = self._manage_return_result_from_many_instance(w_item, res, a_params, True)
                        self._call_trigger_post("read", w_result)
                        return w_result

                w_result = self.get_many(a_item_id, a_params, a_subject)
                self._call_trigger_post("read", w_result)


        return w_result

    def up_sert(self, a_item_id, a_id, a_new_field, a_subject=None):
        """ update (insert if no exists) a collection with bson (a_new_field) for the id specify in parameter and return the models create """

        if self._storage is not None:
            w_item = self._items[a_item_id]

            if w_item is not None:
                model = w_item["_class_obj"]()
                model.on_update()
                for prop in a_new_field:
                    if prop[0] == "_":
                        getattr(model,prop[1:])(a_new_field[prop])
                    else:
                        getattr(model,prop)(a_new_field[prop])

                res = self._up_sert(w_item, a_id, model.__dict__, a_subject)
                if res is not None:
                    return Model(res)
        return None

    def _up_sert(self, a_item, a_id, a_new_field, a_subject=None):
        if a_subject is not None:
            a_new_field["_mongo_model"]["_tid"] =  a_subject["tid"]
            a_new_field["_mongo_model"]["_account"] = a_subject["sub"]

        self._call_trigger_pre("upsert", a_item["id"], a_new_field)
        res = self._storage.up_sert(a_item, a_id, a_new_field)
        self._call_trigger_post("upsert", a_item["id"], a_new_field)

        if res is not None:
            return res

    def up_sert_model(self, a_id, a_model, a_subject=None):
        """ update (insert if no exists) a collection with bson (a_new_field) for the id specify in parameter and return the models create """

        if self._storage is not None:
            w_item = self._items_class[a_model.__class__.__name__]

            if w_item is not None:

                res = self._up_sert(w_item, a_id, a_model.__dict__, a_subject)

                if res is not None:
                    return res
        return None

    def up_sert_many(self, a_item_id,a_new_fields, a_subject=None):
        res = []

        for w_dict in a_new_fields:
            w_res = self.up_sert(a_item_id, w_dict._id,w_dict, a_subject)

            if w_res is not None:
                res.append(w_res)
        return res

    def up_sert_many_model(self,  a_new_models, a_subject=None):
        res = []

        for w_dict in a_new_models:
            w_res = self.up_sert_model( w_dict._id, w_dict, a_subject)

            if w_res is not None:
                res.append(w_res)
        return res

    def delete(self, a_item_id, a_id, a_subject=None):
        if self._storage is not None:
            w_item = self._items[a_item_id]

            if w_item is not None:
                read = self._storage.get_one(w_item["collection"], a_id)
                self._call_trigger_pre("upsert", a_item_id, read)

                self._storage.delete(w_item["collection"], a_id)
                self._call_trigger_post("delete", a_item_id, read)

        return None

    @BindField("_list_trigger")
    def bind_trigger(self, a_field, a_service, a_service_reference):
        if a_service is not None and a_service.get_item() in self._items.keys():
            for a_action in a_service.get_actions():
                if a_action not in self._map_triggers:
                    self._map_triggers[a_action] = {}
                self._map_triggers[a_action][a_service.get_name()] = a_service

    @UnbindField("_list_trigger")
    def un_bind_trigger(self, a_field, a_service, a_service_reference):
        if a_service is not None and a_service.get_item() in self._items.keys():
            for a_action in a_service.get_actions():
                if a_action not in self._map_triggers:
                    self._map_triggers[a_action] = {}
                if a_service.get_name() in self._map_triggers[a_action]:
                    del self._map_triggers[a_action][a_service.get_name()]

    def _call_trigger_pre(self, a_action, a_item_id, a_model=None):
        if a_action in self._map_triggers:
            for w_service in self._map_triggers[a_action].values():
                if not w_service.is_post() and w_service.get_item() == a_item_id:
                    w_service.execute(a_action, a_model)
    def _call_trigger_post(self, a_action, a_item_id, a_model=None):
        if a_action in self._map_triggers:
            for w_service in self._map_triggers[a_action].values():
                if w_service.is_post() and w_service.get_item() == a_item_id:
                    w_service.execute(a_action, a_model)

    def delete_many(self, a_item_id, a_filter, a_subject=None):
        if self._storage is not None:
            w_item = self._items[a_item_id]
            self._manage_filter(a_filter, a_subject["tid"])

            if w_item is not None:
                reads = self._storage.get_many(w_item["collection"], a_filter)
                for w_elem in reads:
                    self._call_trigger_pre("delete", a_item_id, w_elem)
                self._storage.delete_many(w_item["collection"], a_filter)
                for w_elem in reads:
                    self._call_trigger_post("delete", a_item_id, w_elem)

        return None


@ComponentFactory('Manager-Proxy-Factory')
@Provides(specifications=IManager.name)
@Property('_item_id', "item_id", "models",)
@Requires('_default_manager', IDefaultManager.name)
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@App(name="ycappuccino.storage")
class ProxyManager(IManager, Proxy):

    def __init__(self):
        super(ProxyManager, self).__init__()
        self._item_id = None
        self._obj = None
        self._log = None

    @Validate
    def validate(self, context):
        self._log.info("ProxyManager {} validating".format(self._item_id))
        try:
            self._obj = self._default_manager
            self._obj._objname = "proxy-{}".format(self._item_id)
        except Exception as e:
            self._log.error("ProxyManager Error default".format(e))
            self._log.exception(e)

        self._log.info("ProxyManager {} validated".format(self._item_id))

    @Invalidate
    def invalidate(self, context):
        self._log.info("ProxyManager default invalidating")

        self._log.info("ProxyManager default invalidated")


@ComponentFactory('Manager-ProxyMedia-Factory')
@Provides(specifications=IManager.name)
@Property('_item_id', "item_id", "models",)
@Requires('_upload_manager', IUploadManager.name)
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@App(name="ycappuccino.storage")
class ProxyMediaManager(IManager, Proxy):

    def __init__(self):
        super(ProxyMediaManager, self).__init__()
        self._item_id = None
        self._obj = None
        self._log = None

    @Validate
    def validate(self, context):
        self._log.info("ProxyMediaManager {} validating".format(self._item_id))
        try:
            self._obj = self._upload_manager
            self._obj._objname = "proxy-{}".format(self._item_id)
        except Exception as e:
            self._log.error("Manager Error default".format(e))
            self._log.exception(e)

        self._log.info("ProxyMediaManager {} validated".format(self._item_id))

    @Invalidate
    def invalidate(self, context):
        self._log.info("ProxyMediaManager  invalidating")

        self._log.info("ManProxyMediaManagerager  invalidated")




@ComponentFactory('DefaultManager-Factory')
@Provides(specifications=[IDefaultManager.name])
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_storage",IStorage.name,optional=True)
@Requires('_list_trigger', ITrigger.name, aggregate=True, optional=True)
@Requires('_filters', IFilter.name, aggregate=True, optional=True)
@Instantiate("Manager-default")
@App(name="ycappuccino.storage")
class DefaultManager(AbsManager):

    def __init__(self):
        super(DefaultManager, self).__init__()
        self._list_trigger = None
        self._map_trigger = {}

    def add_item(self, a_item, a_bundle_context):
        """ add item in map manage by the manager"""
        super(DefaultManager,self).add_item(a_item, a_bundle_context)
        if not a_item["multipart"]:
            self.create_proxy_manager(a_item, a_bundle_context)

    def remove_item(self, a_item, a_bundle_context):
        """ add item in map manage by the manager"""
        super(DefaultManager,self).remove_item(a_item, a_bundle_context)
        if not a_item["multipart"]:
            self.remove_proxy_manager(a_item, a_bundle_context)

    def create_proxy_manager(self, a_item, a_bundle_context):

        with use_ipopo(a_bundle_context) as ipopo:
            # use the iPOPO core service with the "ipopo" variable
            self._log.info("create proxy {}".format(a_item["id"]))
            ipopo.instantiate("Manager-Proxy-Factory", "Manager-Proxy-{}".format(a_item["id"]),
                                  {"item_id": a_item["id"]})

            self._log.info("end create proxy {}".format(a_item["id"]))


    def remove_proxy_manager(self, a_item, a_bundle_context):
        if a_item["id"] in self._list_component:
            with use_ipopo(a_bundle_context) as ipopo:
                ipopo.kill(self._list_component[a_item["id"]].name)

    @Validate
    def validate(self, context):
        self._log.info("Manager default validating")
        try:
            pass
        except Exception as e:
            self._log.error("Manager Error default".format(e))
            self._log.exception(e)

        self._log.info("Manager default validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("Manager default invalidating")

        self._log.info("Manager default invalidated")
