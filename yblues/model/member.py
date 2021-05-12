from ycappuccino.core.model.decorators import Item,  Property
from ycappuccino.core.model.utils import YDict

@Item(collection="members",name="member")
class Member(YDict):
    def __init__(self, a_dict):
        super(YDict, self).__init__(a_dict)

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Property(name="role")
    def role(self, a_value):
        self._role = a_value

    @Property(name="band_ref")
    def band_ref(self, a_value):
        self._band_ref = a_value