from ycappuccino.storage.models.decorators  import Item, Property, Empty, Reference, ItemReference
from ycappuccino.storage.models.model import Model
import os
from ycappuccino.core.decorator_app import App

@Empty()
def empty():
    _empty = Measure()
    _empty.id("client_pyscript_core")
    _empty.name("client_pyscript_core")
    return _empty

@App(name="ycappuccino.iot")
@Item(collection="measures",name="measure", plural="measures", secure_write=True, secure_read=True)
@ItemReference(from_name="measure", field="sensor", item="sensor")
class Measure(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._name = None
        self._sensor = None
        self._val = None
        self._ts = None


    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Reference(name="sensor")
    def sensor(self, a_value):
        self._sensor = a_value

    @Property(name="val")
    def val(self, a_value):
        self._val = a_value
    @Reference(name="ts")
    def ts(self, a_value):
        self._ts = a_value




empty()