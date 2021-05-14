from ycappuccino.core.api import IStorage, IActivityLogger, YCappuccino

import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate,  Provides, Instantiate
from pymongo import MongoClient

from ycappuccino.core.model.model import Model

_logger = logging.getLogger(__name__)


@ComponentFactory('Storage-Factory')
@Provides(specifications=[IStorage.name, YCappuccino.name])
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
        return self._db[a_collection].aggregate(a_pipeline)

    def get_one(self, a_collection, a_id):
        """ get dict identify by a Id"""
        w_filter = {"_id": a_id}
        return self._db[a_collection].find(w_filter)

    def get_many(self, a_collection, a_filter):
        """ return iterable of dict regarding filter"""
        return self._db[a_collection].find(a_filter)

    def up_sert(self, a_collection, a_id, a_new_dict):
        """" update or insert new dict"""

        w_filter = {"_id": a_id}
        res = self._db[a_collection].find(w_filter)
        if res.count() == 1:
            model = Model(res[0])
            if isinstance(a_new_dict, Model):
                model.update(a_new_dict._mongo_model)
            else:
                model.update(a_new_dict)

            w_update = {
                "$set": a_new_dict._mongo_model
            }
        else:
            if isinstance(a_new_dict, Model):
                w_update = {
                    "$set":a_new_dict._mongo_model
                }
            else:
                w_update = {
                    "$set": a_new_dict
                }
        return self._db[a_collection].update_one(w_filter, w_update, upsert=True)

    def up_sert_many(self, a_collection, a_filter, a_new_dict):
        """ update or insert document with new dict regarding filter """
        if isinstance(a_new_dict,Model):
            w_update = {
                "$set": a_new_dict._mongo_model
            }
        else:
            w_update = {
                "$set":a_new_dict
            }
        return self._db[a_collection].update_many(a_filter, w_update, upsert=True)

    def delete(self, a_collection, a_id):
        """ delete document identified by id if it exists """
        w_filter = {"_id": a_id}
        self._db[a_collection].delete_one(w_filter, upsert=True)

    def delete_many(self, a_collection, a_filter):
        self._db[a_collection].delete_many(a_filter, upsert=True)


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