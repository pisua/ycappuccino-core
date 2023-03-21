
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property, Provides, Instantiate
from api import ITest1, YCappuccino
@ComponentFactory('test-Factory')
@Provides(specifications=[ITest1.name, YCappuccino.name])
@Property('_id', "id", "test1")
@Instantiate("test")
class Test(ITest1,YCappuccino):
    def __init__(self):
        super(Test,self).__init__()
        self._activate = True
    def get_display(self):
        return "<p><b>Hello World</b></p>"

    def set_activate(self, a_bool=False):
        self._activate = a_bool

    def is_activate(self):
        return self._activate
    @Validate
    def validate(self, context):
        pass

    @Invalidate
    def invalidate(self, context):
        pass
