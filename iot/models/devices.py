from ycappuccino.storage.models.decorators  import Item, Property, Empty, Reference, ItemReference
from ycappuccino.storage.models.model import Model
import os

@Empty()
def empty():
    _empty = Device()
    _empty.id("admin")
    _empty.name("admin")
    return _empty


@Item(collection="devices",name="device", plural="devices", app="all", secure_write=True, secure_read=True)
@ItemReference(from_name="device", field="script_actuator", item="media")
@ItemReference(from_name="device", field="script_sensor", item="media")
class Device(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._name = None
        self._acquire = None
        self._script_sensor = None
        self._script_actuator = None



    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Property(name="acquire")
    def acquire(self, a_value):
        self._acquire = a_value

    @Reference(name="script_sensor")
    def script_sensor(self, a_value):
        self._script_sensor = a_value
    @Reference(name="script_actuator")
    def script_actuator(self, a_value):
        self._script_actuator = a_value




empty()