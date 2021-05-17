from ycappuccino.core.model.decorators import Item, Property, Reference, ItemReference
from ycappuccino.core.model.model import Model

@Item(collection="musics",name="music", secureWrite=True)
@ItemReference(field_name="_album", item_name="album")
class Music(Model):
    """ bean that represent a music of an album(or not) """
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._name = None
        self._author = None
        self._composer = None
        self._album = None
        self._arrangment = None
        self._feat = None
        self._album_properties = None

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Property(name="author")
    def author(self, a_value):
        self._author = a_value

    @Property(name="composer")
    def composer(self, a_value):
        self._composer = a_value

    @Property(name="arrangment")
    def arrangment(self, a_value):
        self._arrangment = a_value

    @Property(name="feat")
    def feat(self, a_value):
        self._feat = a_value

    @Reference(name="album")
    def album(self, a_value, a_properties):
        self._album = a_value
        self._album_properties = a_properties
