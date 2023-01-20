from ycappuccino.storage.models.decorators  import Item, Property, Empty, Reference, ItemReference
from ycappuccino.storage.models.model import Model
import os

@Empty()
def empty():
    _empty = Channel()
    _empty.id("admin")
    _empty.name("admin")
    return _empty


@Item(collection="channels",name="channel", plural="channels", app="all", secure_write=True, secure_read=True)
@ItemReference(from_name="channel", field="device", item="device")
class Channel(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._name = None
        self._device = None
        self._type = None

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Reference(name="device")
    def device(self, a_value):
        self._device = a_value

    @Property(name="type")
    def type(self, a_value):
        self._type = a_value




empty()