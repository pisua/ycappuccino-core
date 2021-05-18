import logging


class CFQCN(object):
    """
    CFQCN class : Ful Qualified Class Name
    """
    @staticmethod
    def build(aClassName):
        wFQCN =  '.'.join([CFQCN.__module__, aClassName])
        wLog = logging.getLogger(__name__)
        wLog.info("FQCN '{0}' ...".format(wFQCN))
        return wFQCN


class IActivityLogger(object):
    """ Activity logger of the application. admit a property name that identified the logger"""
    name = CFQCN.build("IActivityLogger")

    def __init__(self):
        """ abstract constructor """


class IManagerBootStrapData(object):
    """ Manage bootstrap interface. it allow to initialize for an item data or do a bootstrap operation"""
    name = CFQCN.build("IManagerBootStrapData")

    def __init__(self):
        """ abstract constructor """
        pass

    def bootstrap(self):
        """ method call while manage is initialized and finish to allow to bootstrap operation """


class IConfiguration(object):
    """ interface of proxy component that allow to bind all
    YCappuccino ycappuccino_core component and notify client ipopo of ycappuccino_core component"""
    name = CFQCN.build("IConfiguration")

    def __init__(self):
        """ abstract constructor """

class IJwt(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("IJwt")

    def __init__(self):
        """ abstract constructor """
        pass

class IStorage(object):
    """ interface of proxy component that allow to bind all
    YCappuccino ycappuccino_core component and notify client ipopo of ycappuccino_core component"""
    name = CFQCN.build("IStorage")

    def __init__(self):
        """ abstract constructor """
        pass

class IServerProxy(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("IServerProxy")

    def __init__(self):
        """ abstract constructor """
        pass

class YCappuccino(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("YCappuccino")

    def __init__(self):
        """ abstract constructor """
        pass




class IEndpoint(object):
    """ interface of generic endpoint that manage all redirection of request with specific parameter """
    name = CFQCN.build("IEndpoint")

    def __init__(self):
        """ abstract constructor """

    def post(self, a_item_id, a_header, a_params, a_body):
        pass

    def put(self, a_item_id, a_header, a_params, a_body):
        pass

    def get(self, a_item_id, a_header, a_params):
        pass

    def delete(self, a_item_id, a_header, a_params):
        pass


class IService(object):
    """ """
    name = CFQCN.build("IService")

    def __init__(self):
        pass


class IManager(object):
    """ """
    name = CFQCN.build("IManager")

    def __init__(self):
        pass

    def get_item(self):
        pass

    def is_secure(self):
        pass

    def get_one(self, a_id):
        pass

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


class IItemManager(IManager):
    """ """
    name = CFQCN.build("IItemManager")

    def __init__(self):
        super(IManager, self).__init__()

