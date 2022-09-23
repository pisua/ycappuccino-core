from ycappuccino.core.model.decorators import Item, Property, Reference, ItemReference, Empty
from ycappuccino.core.model.model import Model

@Empty()
def empty():
    _empty = RolePermission()
    _empty.id("test")
    _empty.role("test")
    _empty.rights("test")
    return _empty

@Item(collection="rolePermissions", name="rolePermission", plural="role-permissions", app="core", secureWrite=True, secureRead=True)
@ItemReference(field="permission", item="permission")
@ItemReference(field="role", item="role")
class RolePermission(Model):
    def __init__(self):
        super().__init__()
        self._role = None
        self._permission = None

    @Reference(name="name")
    def role(self, a_value):
        self._role = a_value

    @Reference(name="permission")
    def rights(self, a_values):
        """ list of right permission """
        self._permissions = a_values

empty()