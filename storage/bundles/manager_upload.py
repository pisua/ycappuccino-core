from pelix.ipopo.constants import use_ipopo
from ycappuccino.core.api import IUploadManager, IActivityLogger, IStorage, ITrigger
from ycappuccino.core.bundles.managers import AbsManager

import logging

_logger = logging.getLogger(__name__)

@ComponentFactory('UploadManager-Factory')
@Provides(specifications=[IUploadManager.name])
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_storage",IStorage.name,optional=True)
@Requires('_list_trigger', ITrigger.name, aggregate=True, optional=True)
#@Instantiate("Manager-upload")
class UploadManager(AbsManager):

    def __init__(self):
        super(AbsManager, self).__init__()
        self._list_trigger = None
        self._map_trigger = {}

    def add_item(self, a_item, a_bundle_context):
        """ add item in map manage by the manager"""
        super(AbsManager,self).add_item(a_item, a_bundle_context)
        self.create_proxy_manager(a_item, a_bundle_context)

    def remove_item(self, a_item, a_bundle_context):
        """ add item in map manage by the manager"""
        super(AbsManager,self).remove_item(a_item, a_bundle_context)
        self.remove_proxy_manager(a_item, a_bundle_context)

    def create_proxy_manager(self, a_item, a_bundle_context):

        with use_ipopo(a_bundle_context) as ipopo:
            # use the iPOPO core service with the "ipopo" variable
            ipopo.instantiate("Manager-Proxy-Factory", "Manager-Proxy-{}".format(a_item["id"]),
                              {"item_id": a_item["id"]})

    def remove_proxy_manager(self, a_item, a_bundle_context):
        if a_item["id"] in self._list_component:
            with use_ipopo(a_bundle_context) as ipopo:
                ipopo.kill(self._list_component[a_item["id"]].name)

    @BindField("_list_trigger")
    def bind_trigger(self, a_field, a_service, a_service_reference):
        if a_service is not None and a_service.get_item() == self._item_id:
            self._map_trigger[a_service.get_name()] = a_service

    @UnbindField("_list_trigger")
    def un_bind_trigger(self, a_field, a_service, a_service_reference):
        if a_service is not None and a_service.get_item() == self._item_id:
            if a_service.get_name() in self._map_trigger[a_service.get_name()]:
                del self._map_trigger[a_service.get_name()]

    def upload(self, a_file_blob, a_file_path):
        """ update (insert if no exists) a collection with bson (a_new_field) for the id specify in parameter and return the models create """

        return None

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
