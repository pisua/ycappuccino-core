#app="all"
from ycappuccino.core.api import CFQCN

from pelix.ipopo.decorators import Validate, Invalidate, Requires, Property
from pelix.ipopo.constants import use_ipopo
from ycappuccino.storage.api import IManager

from ycappuccino.component_creator.models.component_factory import ComponentFactory
from ycappuccino.endpoints.api import IJwt


class IComponentServiceList(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("IComponentServiceList")

    def __init__(self):
        """ abstract constructor """
        pass

@Property('_model', "model", None)
class IComponentServiceFactory(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("IComponentServiceFactory")

    def __init__(self):
        """ abstract constructor """
        self._model = None

