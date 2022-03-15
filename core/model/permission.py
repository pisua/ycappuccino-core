from ycappuccino.core.model.decorators import Item, Property
from ycappuccino.core.model.model import Model


@Item(collection="permissions", name="permission")
class Permission(Model):
    def __init__(self, a_dict):
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
