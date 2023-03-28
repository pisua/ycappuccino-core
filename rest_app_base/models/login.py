from ycappuccino.core.models.decorators  import Item, Property, Empty
from ycappuccino.storage.models.model import Model
import hashlib
import os
from ycappuccino.core.decorator_app import App

@Empty()
def empty():
    _empty = Login()
    _empty.id("client_pyscript_core")
    _empty.password("client_pyscript_core")
    return _empty

@App(name="ycappuccino.rest-app")
@Item(collection="logins",name="login", plural="logins",  secure_write=True, secure_read=True)
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




empty()