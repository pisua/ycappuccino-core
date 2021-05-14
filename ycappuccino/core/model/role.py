from ycappuccino.core.model.decorators import Item, Property
from ycappuccino.core.model.model import Model

@Item(collection="roles",name="role")
class Role(Model):
    def __init__(self, a_dict):
        super().__init__(a_dict)

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Property(name="rights")
    def rights(self, a_values):
        """ list of right permission """
        self._rights = a_values
