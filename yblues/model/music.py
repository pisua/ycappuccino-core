from ycappuccino.core.model.decorators import Item, Property
from ycappuccino.core.model.utils import YDict

@Item(collection="musics",name="music")
class Music(YDict):
    def __init__(self, a_dict):
        super(YDict, self).__init__(a_dict)

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Property(name="author")
    def author(self, a_value):
        self._author = a_value

    @Property(name="composer")
    def composer(self, a_value):
        self._composer = a_value

    @Property(name="video_ref")
    def video_ref(self, a_value):
        self._video_ref = a_value