from ycappuccino.core.models.decorators  import Item, Property, Empty
from ycappuccino.storage.models.model import Model

from ycappuccino.core.decorator_app import App

@Empty()
def empty():
    _empty = ExternalService()
    _empty.id("client_pyscript_core")
    return _empty

@App(name="ycappuccino.component_creator")
@Item(collection="component_creator",name="external_service", plural="component_creator",  secure_write=True, secure_read=True)
class ExternalService(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._factory_id = None
        self._filter = None
        self._name = None
        self._active = False
        self._component_error = None
        self._configuration = None


    @Property(name="factory_id")
    def factory_id(self, a_value):
        self._factory_id = a_value

    def get_factory_id(self):
        return self._factory_id

    @Property(name="filter")
    def filter(self, a_value):
        self._filter = a_value

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value
    @Property(name="active")
    def active(self, a_value):
        self._active = a_value

    def get_active(self):
        return self._active

    @Property(name="component_error")
    def component_error(self, a_value):
        self._component_error = a_value

    @Property(name="configuration")
    def configuration(self, a_value):
        self._configuration = a_value

empty()