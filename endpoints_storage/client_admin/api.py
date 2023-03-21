class CFQCN(object):
    """
    CFQCN class : Ful Qualified Class Name
    """
    @staticmethod
    def build(aClassName):
        wFQCN =  '.'.join(["ycappuccino.api",aClassName])
        return wFQCN
class YCappuccino(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("YCappuccino")

    def __init__(self):
        """ abstract constructor """
        self._id = None

    def id(self):
        return self._id

class IListComponent(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("IListComponent")

    def __init__(self):
        """ abstract constructor """
        pass
class ITest1(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("ITest1")

    def __init__(self):
        """ abstract constructor """
        pass

class ITest2(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("ITest2")

    def __init__(self):
        """ abstract constructor """
        pass

class ITestMain(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("ITestMain")

    def __init__(self):
        """ abstract constructor """
        pass