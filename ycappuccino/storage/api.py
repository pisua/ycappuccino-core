import logging

from ycappuccino.core.api import CFQCN

class IBootStrap(object):
    """ Manage bootstrap interface. it allow to initialize for an item data or do a bootstrap operation"""
    name = CFQCN.build("IBootStrap")

    def __init__(self):
        """ abstract constructor """
        pass

    def bootstrap(self):
        """ method call while manage is initialized and finish to allow to bootstrap operation """
        pass

    def get_id(self):
        pass


class IStorage(object):
    """ interface of proxy component that allow to bind all
    YCappuccino ycappuccino_core component and notify client ipopo of ycappuccino_core component"""
    name = CFQCN.build("IStorage")

    def __init__(self):
        """ abstract constructor """
        pass


class ITrigger(object):
    """ """
    name = CFQCN.build("ITrigger")

    def __init__(self, a_name, a_item_id, a_synchronous=False, a_post=False):
        self._synchronous = a_synchronous
        self._post = a_post
        self._name = a_name
        self._item_id = a_item_id

    def execute(self, a_model_before, a_model_after):
        pass

    def is_synchronous(self):
        return self._synchronous

    def get_item_id(self):
        return self._item_id

    def get_name(self):
        return self._name

    def is_post(self):
        return self._post

    def is_pre(self):
        return not self._post


class IManager(object):
    """ """
    name = CFQCN.build("IManager")

    def __init__(self):
        pass


class IDefaultManager(IManager):
    """ """
    name = CFQCN.build("IDefaultManager")

    def __init__(self):
        pass


class IUploadManager(IDefaultManager):
    """ """
    name = CFQCN.build("IUploadManager")

    def __init__(self):
        pass


class IItemManager(IManager):
    """ """
    name = CFQCN.build("IItemManager")

    def __init__(self):
        super(IManager, self).__init__()

