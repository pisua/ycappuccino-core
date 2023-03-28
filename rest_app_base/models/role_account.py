from ycappuccino.core.models.decorators  import Item, Reference, ItemReference, Empty
from ycappuccino.storage.models.model import Model
from ycappuccino.core.decorator_app import App

@Empty()
def empty():
    _empty = RoleAccount()
    _empty.id("test")
    _empty.role("test")
    _empty.account("test")
    _empty.organization("test")
    return _empty

@App(name="ycappuccino.rest-app")
@Item(collection="roleAccounts", name="roleAccount", plural="role-accounts", secure_write=True, secure_read=True)
@ItemReference(from_name="roleAccounts", field="account", item="account")
@ItemReference(from_name="roleAccounts",field="role", item="role")
@ItemReference(from_name="roleAccounts",field="organization", item="organization")
class RoleAccount(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._role = None
        self._account = None
        self._organization = None

    @Reference(name="role")
    def role(self, a_value):
        self._role = a_value

    @Reference(name="account")
    def account(self, a_values):
        """ list of right permission """
        self._account = a_values

    @Reference(name="organization")
    def organization(self, a_organization):
        """ list of right permission """
        self._organization = a_organization

empty()