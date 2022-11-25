from ycappuccino.core.model.decorators import Item, Property, Reference, ItemReference, Empty
from ycappuccino.core.model.model import Model

@Empty()
def empty():
    _empty = Role()
    _empty.id("test")
    _empty.name("test")
    return _empty


@Item(collection="roles", name="role", plural="roles", app="core", secure_write=True, secure_read=True)
class Role(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._name = None
        self._permissions = None

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

empty()