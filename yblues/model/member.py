from ycappuccino.core.model.decorators import Item,  Property, Reference, ItemReference
from ycappuccino.core.model.model import Model

@Item(collection="members",name="member", secureWrite=True)
@ItemReference(field_name="_band", item_name="band")
class Member(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._band = None
        self._name = None
        self._role = None

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Property(name="role")
    def role(self, a_value):
        self._role = a_value

    @Reference(name="band")
    def band(self, a_value):
        self._band = a_value