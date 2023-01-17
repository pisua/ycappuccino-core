from ycappuccino.storage.models.decorators  import Item, Property, Empty
from ycappuccino.storage.models.model import Model

@Empty()
def empty():
    _empty = Organization()
    _empty.id("test")
    _empty.name("test")
    _empty.comment("txt")

    return _empty


@Item(collection="organizations", name="organization", plural="organizations", app="all", secure_write=True, secure_read=True)
class Organization(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._name = None
        self._comment = None
        self._father = None

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Property(name="father")
    def father(self, a_value):
        self._father = a_value

    @Property(name="comment")
    def comment(self, a_value):
        self._comment = a_value



empty()