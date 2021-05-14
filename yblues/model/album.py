from ycappuccino.core.model.decorators import Item, Property
from ycappuccino.core.model.model import Model

@Item(collection="albums",name="album")
class Album(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Property(name="productor")
    def productor(self, a_value):
        self._productor = a_value

    @Property(name="image_url")
    def image_url(self, a_value):
        self._image_url = a_value

    @Property(name="release_date")
    def release_date(self, a_value):
        self._release_date = a_value

    @Property(name="label")
    def label(self, a_value):
        self._label = a_value