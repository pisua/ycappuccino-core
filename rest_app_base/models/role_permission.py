from ycappuccino.core.models.decorators  import Item, Reference, ItemReference, Empty, Property
from ycappuccino.storage.models.model import Model
from ycappuccino.core.decorator_app import App

@Empty()
def empty():
    _empty = RolePermission()
    _empty.id("test")
    _empty.role("test")
    _empty.rights("test")
    return _empty

@App(name="ycappuccino.rest-app")
@Item(collection="rolePermissions", name="rolePermission", plural="role-permissions",  secure_write=True, secure_read=True)
@ItemReference(from_name="rolePermission", field="permission", item="permission")
@ItemReference(from_name="rolePermission",field="role", item="role")
class RolePermission(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._role = None
        self._permission = None
        self._organization = None

    @Reference(name="role")
    def role(self, a_value):
        self._role = a_value

    @Property(name="permissions")
    def rights(self, a_values):
        """ list of right permission """
        self._permissions = a_values



empty()