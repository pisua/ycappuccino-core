from ycappuccino.core.model.decorators import Item, Property, Reference, ItemReference
from ycappuccino.core.model.model import Model
_empty = None

def empty():
    _empty = Role()
    _empty.id("test")
    _empty.name("test")

@Item(collection="roles", name="role", plural="roles", app="core", secureWrite=True, secureRead=True)
class Role(Model):
    def __init__(self):
        super().__init__()
        self._name = None
        self._permissions = None

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

empty()