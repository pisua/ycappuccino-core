from ycappuccino.core.model.decorators import Item, Property,  Reference, ItemReference
from ycappuccino.core.model.model import Model
_empty = None

@Item(collection="clientPaths", name="clientPath", plural="clientPaths", app="core.ui")
@ItemReference(field="_layout_parent", item="layout")
class ClientPath(Model):
    """ describe an account in the application """
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._secure = None
        self._path = None
        self._subpath = ""
        self._priority = ""

    @Property(name="path")
    def path(self, a_value):
        self._path = a_value

    @Property(name="subpath")
    def subpath(self, a_value):
        self._subpath = a_value

    @Property(name="priority")
    def priority(self, a_value):
        self._priority = a_value

    @Property(name="secure")
    def secure(self, a_value):
        self._secure = a_value
