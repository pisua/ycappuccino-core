from ycappuccino.core.model.decorators import Item, Property, Reference, ItemReference
from ycappuccino.core.model.model import Model


@Item(collection="roles", name="role", plural="roles", app="core")
@ItemReference(field="permission", item="permission")
class Role(Model):
    def __init__(self):
        super().__init__()
        self._name = None
        self._permissions = None

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Reference(name="permission")
    def rights(self, a_values):
        """ list of right permission """
        self._permissions = a_values
