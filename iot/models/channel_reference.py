from ycappuccino.storage.models.decorators  import Item, Property, Empty, Reference, ItemReference
from ycappuccino.storage.models.model import Model
import os

@Empty()
def empty():
    _empty = ReferenceChannel()
    _empty.id("admin")
    _empty.name("admin")
    return _empty


@Item(collection="referenceChannels",name="referenceChannel", plural="reference-channels", abstract=True, app="all", secure_write=True, secure_read=True)
@ItemReference(from_name="referenceChannel", field="channel", item="channel")
class ReferenceChannel(Model):
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