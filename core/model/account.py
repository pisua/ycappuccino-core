from ycappuccino.core.model.decorators import Item, Property,  Reference, ItemReference
from ycappuccino.core.model.model import Model

@Item(collection="accounts" ,name="account", plural="accounts", app="core", secureWrite=True, secureRead=True)
@ItemReference(field="login" ,item="login")
@ItemReference(field="role" ,item="role")
class Account(Model):
    """ describe an account in the application """
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._login = None
        self._name = None
        self._role = None

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Reference(name="login")
    def login(self, a_value):
        self._login = a_value

    @Reference(name="role")
    def role(self, a_value):
        self._role = a_value
