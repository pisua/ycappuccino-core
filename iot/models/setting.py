from ycappuccino.storage.models.decorators  import Item, Property, Empty, Reference, ItemReference
from ycappuccino.storage.models.model import Model
import os
from ycappuccino.core.decorator_app import App

@Empty()
def empty():
    _empty = Setting()
    _empty.id("client_admin")
    _empty.name("client_admin")
    return _empty

@App(name="ycappuccino.iot")
@Item(collection="settings",name="setting", plural="settings", secure_write=True, secure_read=True)
@ItemReference(from_name="setting", field="actuator", item="actuator")
class Setting(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._name = None
        self._actuator = None
        self._val = None
        self._ts = None


    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Reference(name="actuator")
    def actuator(self, a_value):
        self._actuator = a_value

    @Property(name="val")
    def val(self, a_value):
        self._val = a_value
    @Reference(name="ts")
    def ts(self, a_value):
        self._ts = a_value




empty()