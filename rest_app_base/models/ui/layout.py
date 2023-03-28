#app="all"
from ycappuccino.core.models.decorators  import Item, Property,  Reference, ItemReference
from ycappuccino.storage.models.model import Model
from ycappuccino.core.decorator_app import App

_empty = None

@App(name="ycappuccino.rest-app")
@Item(collection="layouts", name="layout", plural="layouts", secure_write=True, secure_read=True)
@ItemReference(from_name="layout",field="_layout_parent", item="layout")
class Layout(Model):
    """ describe an account in the application """
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._layout_parent = None
        self._name = None
        self._content = None

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Property(name="content")
    def content(self, a_value):
        self._content = a_value

    @Reference(name="layout_parent")
    def layout_parent(self, a_value):
        self._layout_parent = a_value
