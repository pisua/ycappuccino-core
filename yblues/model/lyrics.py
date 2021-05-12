from ycappuccino.core.model.decorators import Item, Property
from ycappuccino.core.model.utils import YDict

@Item(collection="lyrics",name="lyric")
class Lyrics(YDict):
    def __init__(self, a_dict):
        super(YDict, self).__init__(a_dict)

    @Property(name="music_ref")
    def music_ref(self, a_value):
        self._music_ref = a_value

    @Property(name="lyrics")
    def lyrics(self, a_value):
        self._lyrics = a_value