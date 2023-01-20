from ycappuccino.storage.models.decorators  import Item, Property, Empty, Reference, ItemReference
from ycappuccino.storage.models.model import Model
import os

@Empty()
def empty():
    _empty = Sensor()
    _empty.id("admin")
    _empty.name("admin")
    return _empty


@Item(collection="sensors",name="sensor", plural="sensors", app="all", secure_write=True, secure_read=True)
@ItemReference(from_name="sensor", field="referenceChannel", item="referenceChannel")
@ItemReference(from_name="sensor", field="device", item="device")
class Sensor(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._name = None
        self._reference_channel = None
        self._serialization_type = None
        self._device = None


    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Reference(name="device")
    def device(self, a_value):
        self._device = a_value

    @Property(name="serialization_type")
    def serialization_type(self, a_value):
        self._serialization_type = a_value
    @Reference(name="referenceChannel")
    def reference_channel(self, a_value):
        self._reference_channel = a_value




empty()