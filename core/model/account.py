from ycappuccino.core.model.decorators import Item, Property, ItemReference, Reference
from ycappuccino.core.model.model import Model

@Item(collection="accounts" ,name="account", plural="accounts")
@ItemReference(item_name="login", field_name="_login", ref_name="login")
@ItemReference(item_name="role", field_name="_role", ref_name="role")
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

    def login(self, a_value):
        self._login = a_value

    def role(self, a_value):
        self._role = a_value
