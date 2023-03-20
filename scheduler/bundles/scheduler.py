#app="all"
import json

from ycappuccino.core.api import IActivityLogger, IService, YCappuccino
from ycappuccino.storage.api import IManager
from ycappuccino.endpoints.api import IJwt
from ycappuccino.core.decorator_app import App
from ycappuccino.scheduler.api import IScheduler
import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, Instantiate
import hashlib


_logger = logging.getLogger(__name__)


@ComponentFactory('SchedulerService-Factory')
@Provides(specifications=[IService.name, YCappuccino.name,IScheduler.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_manager_task", IManager.name, spec_filter="'(item_id=task)'")
@Requires("_jwt", IJwt.name)
@Instantiate("SchedulerService")
@App(name="ycappuccino.rest-app")
class SchedulerService(IService):

    def __init__(self):
        super(IService, self).__init__();
        self._manager_task = None
        self._log = None
        self._jwt = None

    def is_secure(self):
        return False

    def get_name(self):
        return "scheduler"

    def post(self, a_header, a_url_path, a_body):
        """ return tuple of 2 element that admit a dictionnary of header and a body"""
        # execute
        return None


    def put(self, a_header, a_url_path, a_body):
        return None

    def get(self, a_header, a_url_path):
        return None

    def delete(self, a_header, a_url_path):
        return None

    @Validate
    def validate(self, context):
        self._log.info("SchedulerService validating")

        self._log.info("SchedulerService validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("SchedulerService invalidating")

        self._log.info("SchedulerService invalidated")
