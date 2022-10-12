from ycappuccino.core.model.decorators import Item, Property, Reference, ItemReference, Empty
from ycappuccino.core.model.model import Model

@Empty()
def empty():
    _empty = Media()
    _empty.id("test")
    _empty.file_name("test")
    _empty.extension("txt")
    _empty.content_type("txt")

    return _empty

@Item(collection="medias", name="media", plural="medias", app="core", secureWrite=True, secureRead=True)
class Media(Model):
    def __init__(self):
        super().__init__()
        self._file_name = None
        self._path = None
        self._extension = None
        self._content_type = None

    @Property(name="file_name")
    def file_name(self, a_value):
        self._file_name = a_value

    @Property(name="extension")
    def extension(self, a_value):
        self._extension = a_value

    @Property(name="path")
    def path(self, a_value):
        self._path = a_value

    @Property(name="content_type")
    def content_type(self, a_value):
        self._content_type = a_value


empty()