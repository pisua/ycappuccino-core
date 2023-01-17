#app="all"
from ycappuccino.core.api import CFQCN


class ILoginService(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("ILoginService")

    def __init__(self):
        """ abstract constructor """
        pass


class IClobReplaceService(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("IClobReplaceService")

    def __init__(self):
        """ abstract constructor """
        pass


class IClientIndexPathFactory(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("IClientIndexPathFactory")

    def __init__(self):
        """ abstract constructor """
        pass
class ITenantTrigger(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("ITenantTrigger")

    def __init__(self):
        """ abstract constructor """
        pass