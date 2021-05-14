from ycappuccino.core.model.decorators import Item, Property
from ycappuccino.core.model.model import Model

@Item(collection="logins",name="login")
class Login(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)

    @Property(name="login")
    def login(self, a_value):
        self._login = a_value

    @Property(name="password")
    def password(self, a_value):
        self._password = a_value

    @Property(name="account_ref")
    def account_ref(self, a_value):
        self._account_ref = a_value


