from ycappuccino.core.model.decorators import Item, Property,  Reference, ItemReference
from ycappuccino.core.model.model import Model

@Item(collection="clientPaths", name="clientPath", plural="clientPaths", app="core.ui")
@ItemReference(field="_layout_parent", item="layout")
class ClientPath(Model):
    """ describe an account in the application """
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._secure = None
        self._path = None

    @Property(name="path")
    def path(self, a_value):
        self._path = a_value

    @Property(name="secure")
    def secure(self, a_value):
        self._secure = a_value

