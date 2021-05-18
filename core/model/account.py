from ycappuccino.core.model.decorators import Item, Property, ItemReference, Reference
from ycappuccino.core.model.model import Model

@Item(collection="accounts" ,name="account")
@ItemReference(item_name="login", field_name="_login")
class Account(Model):
    """ describe an account in the application """
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._login = None
        self._name = None

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Reference(name="login")
    def login(self, a_value):
        self._login = a_value


