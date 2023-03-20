#app="all"
from ycappuccino.core.api import CFQCN
from ycappuccino.core.api import  IService

class IScheduler(IService):
    """ Manage bootstrap interface. it allow to initialize for an item data or do a bootstrap operation"""
    name = CFQCN.build("IScheduler")

    def __init__(self):
        """ abstract constructor """
        pass

