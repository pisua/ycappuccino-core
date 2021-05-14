from ycappuccino.core.model.decorators import Item, Property
from ycappuccino.core.model.model import Model

@Item(collection="bands",name="band")
class Band(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value
        
    @Property(name="address")
    def address(self, a_value):
        self._address = a_value

    @Property(name="city")
    def city(self, a_value):
        self._city = a_value