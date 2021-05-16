from ycappuccino.core.model.decorators import Item, Property, Reference
from ycappuccino.core.model.model import Model

@Item(collection="lyrics",name="lyric")
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