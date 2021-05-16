from ycappuccino.core.model.decorators import Item, Property
from ycappuccino.core.model.model import Model

@Item(collection="accounts",name="account")
class Account(Model):

    def __init__(self, a_dict=None):
        super().__init__(a_dict)

    @Property(name="name")
    def name(self, a_value):

        self._name = a_value



    @Property(name="login_ref")
    def login_ref(self, a_value):

        self._login_ref = a_value


