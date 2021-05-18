from ycappuccino.core.model.decorators import Item, Property
from ycappuccino.core.model.model import Model
import hashlib
import os

@Item(collection="logins",name="login")
class Login(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._password = None
        self._salt = None
        self._login = None
        self._account_ref = None

    @Property(name="login")
    def login(self, a_value):
        self._login = a_value

    @Property(name="salt")
    def salt(self, a_value):
        self._salt = a_value

    @Property(name="password")
    def _private_password(self, a_value):
        self._password = a_value


    def password(self, a_value):
        self.salt(os.urandom(32).hex())
        w_concat = "{}{}".format(self._salt, a_value).encode("utf-8")
        self._private_password(hashlib.md5(w_concat).hexdigest())

    @Property(name="account_ref")
    def account_ref(self, a_value):
        self._account_ref = a_value


