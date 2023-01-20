from ycappuccino.storage.models.decorators  import Item, Property, Empty, Reference, ItemReference
from ycappuccino.storage.models.model import Model
import os

@Empty()
def empty():
    _empty = ActuatorSensor()
    _empty.id("admin")
    _empty.name("admin")
    return _empty


@Item(collection="actuatorSensors",name="actuatorSensor", plural="actuator-sensors", abstract=True,  app="all", secure_write=True, secure_read=True)
@ItemReference(from_name="actuatorSensor", field="channel", item="channel")
@ItemReference(from_name="actuatorSensor", field="device", item="device")
class ActuatorSensor(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._name = None
        self._channel = None
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
    @Reference(name="channel")
    def channel(self, a_value):
        self._channel = a_value




empty()