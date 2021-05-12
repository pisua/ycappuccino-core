from ycappuccino.core.model.decorators import Item, Property
from ycappuccino.core.model.utils import YDict

@Item(collection="accounts",name="account")
class Account(YDict):
    def __init__(self, a_dict):
        super(YDict, self).__init__(a_dict)

    @Property(name="name")
    def name(self, a_value):
        self._login = a_value

    @Property(name="login_ref")
    def login_ref(self, a_value):
        self._login_ref = a_value


