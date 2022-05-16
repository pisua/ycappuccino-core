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


class IClientIndexPath(object):
    """ Activity logger of the application. admit a property name that identified the logger"""
    name = CFQCN.build("IClientIndexPath")

    def __init__(self):
        """ abstract constructor """
        pass

    def get_path(self):
        pass

    def get_id(self):
        pass


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

    def get_name(self):
        pass

    def post(self, a_header, a_params, a_body):
        pass

    def put(self, a_header, a_params, a_body):
        pass

    def get(self, a_header, a_params):
        pass

    def delete(self, a_header, a_params):
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

class ILoginService(object):
    """ """
    name = CFQCN.build("ILoginService")

    def __init__(self):
        pass


class IProxyManager(object):
    """ """
    name = CFQCN.build("IProxyManager")

    def __init__(self):
        pass

class IDefaultManager(IManager):
    """ """
    name = CFQCN.build("IDefaultManager")

    def __init__(self):
        pass


class IItemManager(IManager):
    """ """
    name = CFQCN.build("IItemManager")

    def __init__(self):
        super(IManager, self).__init__()

