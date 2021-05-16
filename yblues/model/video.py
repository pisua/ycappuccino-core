from ycappuccino.core.model.decorators import Item, Property
from ycappuccino.core.model.model import Model

@Item(collection="videos",name="video")
class Video(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._name = None

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value
