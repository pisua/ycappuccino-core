from ycappuccino.core.models.decorators  import Item, Property, Empty
from ycappuccino.storage.models.model import Model

from ycappuccino.core.decorator_app import App

@Empty()
def empty():
    _empty = ComponentFactory()
    _empty.id("client_pyscript_core")
    return _empty

@App(name="ycappuccino.component_creator")
@Item(collection="component_factories",name="component_factory", plural="component_factories",  secure_write=True, is_writable=False, secure_read=True)
class ComponentFactory(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._name = None
        self._factory_id = None
        self._configuration_schema = None


    @Property(name="name")
    def name(self, a_value):
        self._name = a_value
    @Property(name="factory_id")
    def factory_id(self, a_value):
        self._factory_id = a_value

    def get_factory_id(self):
        return self._factory_id
    @Property(name="configuration_schema")
    def configuration_schema(self, a_value):
        self._configuration_schema = a_value


empty()