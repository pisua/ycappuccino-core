#app="all"
from ycappuccino.core.api import CFQCN


class IScriptInterpreter(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("IScriptInterpreter")

    def __init__(self):
        """ abstract constructor """
        pass

