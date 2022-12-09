from core import CFQCN


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
