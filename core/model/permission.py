from ycappuccino.core.model.decorators import Item, Property, Empty
from ycappuccino.core.model.model import Model

@Empty()
def empty():
    _empty = Permission()
    _empty.id("admin")
    _empty.name("admin")
    _empty.permission("tout")
    return _empty


@Item(collection="permissions", name="permission", plural="permissions", app="core", secure_write=True,
      secure_read=True)
class Permission(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._name = None
        self._permission = None

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Property(name="permission")
    def permission(self, a_value):
        """ list of right permission """
        self._permission = a_value

empty()