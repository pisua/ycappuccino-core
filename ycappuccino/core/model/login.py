from ycappuccino.core.model.decorators import Item, Property
from ycappuccino.core.model.utils import YDict

@Item(collection="logins",name="login")
class Login(YDict):
    def __init__(self, a_dict):
        super(YDict, self).__init__(a_dict)

    @Property(name="login")
    def login(self, a_value):
        self._login = a_value

    @Property(name="password")
    def login(self, a_value):
        self._password = a_value

    @Property(name="account_ref")
    def account_ref(self, a_value):
        self._account_ref = a_value


