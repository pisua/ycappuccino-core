from ycappuccino.core.model.decorators import Item
from ycappuccino.core.model.utils import YDict

@Item(collection="bands",name="band")
class Band(YDict):
    def __init__(self, a_dict):
        super(YDict, self).__init__(a_dict)

