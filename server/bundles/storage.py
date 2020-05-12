from server.api import IStorage, IActivityLogger

import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property, Provides, Instantiate
from pymongo import MongoClient

_logger = logging.getLogger(__name__)


@ComponentFactory('Storage-Factory')
@Provides(IStorage.name)
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@Instantiate("MongoStorage")
class MongoStorage(IStorage):

    def __init__(self):
        super(IStorage, self).__init__();
        self._log = None
        self._client = None
        self._db = None


    def aggregate(self, a_collection, a_pipeline):
        """ aggegate data regarding filter and pipeline """
        return self.db[a_collection].aggregate(a_pipeline)

    def get_one(self, a_collection, a_id):
        """ get dict identify by a Id"""
        w_filter = {"_id": a_id}
        return self.db[a_collection].find(w_filter)

    def get_many(self, a_collection, a_filter):
        """ return iterable of dict regarding filter"""
        return self.db[a_collection].find(a_filter)

    def up_sert(self, a_collection, a_id, a_new_dict):
        """" update or insert new dict"""

        w_filter = {"_id": a_id}
        res = self.db[a_collection].find(w_filter)
        if len(res) == 1:
            model = res[0]
            model.update(a_new_dict)
        self.db[a_collection].update_one(w_filter, model, upsert=True)

    def up_sert_many(self, a_collection, a_filter, a_new_dict):
        """ update or insert document with new dict regarding filter """
        self.db[a_collection].update_many(a_filter, a_new_dict, upsert=True)

    def delete(self, a_collection, a_id):
        """ delete document identified by id if it exists """
        w_filter = {"_id": a_id}
        self.db[a_collection].delete_one(w_filter, upsert=True)

    def delete_many(self, a_collection, a_filter):
        self.db[a_collection].delete_many(a_filter, upsert=True)


    @Validate
    def validate(self, context):
        _logger.info("MongoStorage validating")
        try:
            self._client = MongoClient("localhost", 27017)
            self._db = self._client.ycappuccino

        except Exception as e:
            _logger.error("MongoStorage Error {}".format(e))
            _logger.exception(e)

        _logger.info("MongoStorage validated")

    @Invalidate
    def invalidate(self, context):
        _logger.info("MongoStorage invalidating")
        try:
            if self._client is not None:
                self._client.close()
                self._client = None
                self._db = None
        except Exception as e:
            _logger.error("MongoStorage Error {}".format(e))
            _logger.exception(e)
        _logger.info("MongoStorage invalidated")