from ycappuccino.storage.models.decorators  import Item, Property, Empty
from ycappuccino.storage.models.model import Model
from ycappuccino.core.decorator_app import App

@Empty()
def empty():
    _empty = Scheduler()
    _empty.id("test")
    _empty.name("test")
    return _empty

@App(name="ycappuccino.scheduler")
@Item(collection="schedulers", name="scheduler", plural="schedulers",  secure_write=True, secure_read=True)
class Scheduler(Model):
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        self._name = None
        self._cron = None

    @Property(name="name")
    def name(self, a_value):
        self._name = a_value

    @Property(name="cron")
    def cron(self, a_value):
        self._cron = a_value
empty()