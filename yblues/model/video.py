from ycappuccino.core.model.decorators import Item, Property, Reference, ItemReference
from ycappuccino.core.model.model import Model

@Item(collection="videos",name="video")
@ItemReference(field_name="_music", item_name="music")
class Video(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._name = None
        self._music = None

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Reference(name="music")
    def music(self, a_value):
        self._music = a_value
