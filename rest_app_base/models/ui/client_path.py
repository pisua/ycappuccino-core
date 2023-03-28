#app="all"
from ycappuccino.core.models.decorators  import Item, Property, ItemReference
from ycappuccino.storage.models.model import Model
from ycappuccino.core.decorator_app import App

_empty = None

@App(name="ycappuccino.rest-app")
@Item(collection="clientPaths", name="clientPath", plural="clientPaths")
@ItemReference(from_name="clientPath",field="_layout_parent", item="layout")
class ClientPath(Model):
    """ describe an account in the application """
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._secure = None
        self._path = None
        self._subpath = ""
        self._priority = ""
        self._type = ""
        self._core = False

    @Property(name="path")
    def path(self, a_value):
        self._path = a_value

    @Property(name="subpath")
    def subpath(self, a_value):
        self._subpath = a_value

    @Property(name="type")
    def type(self, a_value):
        self._type = a_value

    @Property(name="core")
    def core(self, a_value):
        self._core = a_value

    def get_type(self):
        return self._type

    def is_core(self):
        return self._core

    @Property(name="priority")
    def priority(self, a_value):
        self._priority = a_value

    @Property(name="secure")
    def secure(self, a_value):
        self._secure = a_value

