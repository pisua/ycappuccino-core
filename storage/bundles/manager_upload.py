#app="all"
from pelix.ipopo.constants import use_ipopo
from ycappuccino.core.api import IActivityLogger
from ycappuccino.storage.api import IUploadManager,  IStorage, IDefaultManager, ITrigger, IManager
from ycappuccino.storage.bundles.managers import AbsManager
from ycappuccino.core.decorator_app import App
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Property,  Invalidate, Provides, BindField, UnbindField, \
    Instantiate
import base64, os
import logging

_logger = logging.getLogger(__name__)

@ComponentFactory('UploadManager-Factory')
@Provides(specifications=[IUploadManager.name])
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_storage",IStorage.name,optional=True)
@Requires("_default_manager",IDefaultManager.name)
@Requires('_list_trigger', ITrigger.name, aggregate=True, optional=True)
@App(name="ycappuccino.storage")
@Instantiate("Manager-upload")
@App(name="ycappuccino.storage")
class UploadManager(AbsManager):

    def __init__(self):
        super(UploadManager, self).__init__()
        self._list_trigger = None
        self._default_manager = None
        self._map_trigger = {}

    def get_one(self, a_item_id, a_id, a_params=None, a_subject=None):
        w_result = self._default_manager.get_one(a_item_id, a_id, a_params, a_subject)
        return w_result

    def get_one_blob(self, a_item_id, a_id, a_params=None, a_subject=None):
        w_result = None
        return w_result

    def get_aggregate_one(self, a_item_id, a_id, a_params=None, a_subject=None):
        w_result = self._default_manager.get_aggregate_one(a_item_id, a_id, a_params, a_subject)

        return w_result

    def get_many(self, a_item_id, a_params=None, a_subject=None):
        w_result = self._default_manager.get_many(a_item_id, a_params, a_subject)

        return w_result

    def get_aggregate_many(self, a_item_id, a_params=None, a_subject=None):
        w_result = self._default_manager.get_aggregate_many(a_item_id, a_params, a_subject)
        return w_result

    def up_sert(self, a_item_id, a_id, a_new_field, a_subject=None):
        """ update (insert if no exists) a collection with bson (a_new_field) for the id specify in parameter and return the models create """
        self._store_file(a_new_field)
        w_result = self._default_manager.up_sert(a_item_id, a_id, a_new_field, a_subject)

        return w_result

    def _store_file(self, a_new_field):
        if "content64" in a_new_field.keys():
            # store file if we have all information that indicate the file name
            w_content_base64 = a_new_field["content64"]
            w_content_byte = base64.b64decode(w_content_base64)
            w_content = w_content_byte.decode("utf8")
            del a_new_field["content64"]
        if "content" in a_new_field.keys():
            w_content = a_new_field["content"]
            del a_new_field["content"]

        w_file_name_full = "{}/{}.{}".format(a_new_field["path"], a_new_field["file_name"], a_new_field["extension"])
        with open(w_file_name_full,"w") as f:
            f.write(w_content)
    def _store_file_model(self, a_model):
        self._store_file(a_model)
    def _delete_file(self, a_item_id, a_id):
        # store file if we have all information that indicate the file name
        w_model = self._default_manager.get_one(a_item_id, a_id)
        w_file_name_full = "{}/{}.{}".format(w_model["path"], w_model["file_name"], w_model["extension"])
        os.remove(w_file_name_full)

    def up_sert_model(self, a_id, a_model, a_subject=None):
        """ update (insert if no exists) a collection with bson (a_new_field) for the id specify in parameter and return the models create """
        self._store_file_model(a_model)
        w_result = self._default_manager.up_sert_model( a_id, a_model, a_subject)

        return w_result
    def up_sert_many(self, a_item_id, a_new_fields, a_subject=None):
        for a_new_field in a_new_fields:
            self._store_file(a_new_field)
        w_result = self._default_manager.up_sert_many( a_item_id, a_new_fields, a_subject)
        return w_result

    def up_sert_many_model(self, a_new_models, a_subject=None):
        for a_model in a_new_models:
            self._store_file_model(a_model)
        w_result = self._default_manager.up_sert_many_model( a_new_models, a_subject)
        return w_result

    def delete(self, a_item_id, a_id, a_subject=None):
        self._delete_file(a_item_id, a_id)
        w_result = self._default_manager.delete( a_item_id, a_id , a_subject)
        return w_result
    def add_item(self, a_item, a_bundle_context):
        """ add item in map manage by the manager"""
        super(UploadManager,self).add_item(a_item, a_bundle_context)
        self.create_proxy_manager(a_item, a_bundle_context)

    def remove_item(self, a_item, a_bundle_context):
        """ add item in map manage by the manager"""
        super(UploadManager,self).remove_item(a_item, a_bundle_context)
        self.remove_proxy_manager(a_item, a_bundle_context)

    def create_proxy_manager(self, a_item, a_bundle_context):

        with use_ipopo(a_bundle_context) as ipopo:
            # use the iPOPO core service with the "ipopo" variable
            self._log.info("create proxy {}".format(a_item["id"]))
            ipopo.instantiate("Manager-ProxyMedia-Factory", "Manager-ProxyMedia-{}".format(a_item["id"]),
                                  {"item_id": a_item["id"]})
            self._log.info("end create proxy {}".format(a_item["id"]))


    def remove_proxy_manager(self, a_item, a_bundle_context):
        if a_item["id"] in self._list_component:
            with use_ipopo(a_bundle_context) as ipopo:
                ipopo.kill(self._list_component[a_item["id"]].name)

    @Validate
    def validate(self, context):
        self._log.info("Manager upload validating")
        try:
            pass
        except Exception as e:
            self._log.error("Manager Error upload".format(e))
            self._log.exception(e)

        self._log.info("Manager upload validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("Manager upload invalidating")

        self._log.info("Manager upload invalidated")

