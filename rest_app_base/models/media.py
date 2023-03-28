from ycappuccino.core.models.decorators  import Item, Property, Empty
from ycappuccino.storage.models.model import Model
from ycappuccino.core.decorator_app import App

@Empty()
def empty():
    _empty = Media()
    _empty.id("test")
    _empty.file_name("test")
    _empty.extension("txt")
    _empty.content_type("txt")
    _empty.path("path")

    return _empty

@App(name="ycappuccino.rest-app")
@Item(collection="medias", name="media", plural="medias", secure_write=True, secure_read=True,
      multipart="path")
class Media(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
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

    def get_file_name(self):
        return self._file_name

    def get_extension(self):
        return self._extension

    def get_path(self):
        return self._path


empty()