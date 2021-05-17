from ycappuccino.core.model.decorators import Item, Property, Reference, ItemReference
from ycappuccino.core.model.model import Model

@Item(collection="lyrics", name="lyric", secureWrite=True)
@ItemReference(field_name="_music", item_name="music")
class Lyrics(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._music = None
        self._lyrics = None

    @Reference(name="music")
    def music(self, a_value):
        self._music = a_value

    @Property(name="lyrics")
    def lyrics(self, a_value):
        self._lyrics = a_value