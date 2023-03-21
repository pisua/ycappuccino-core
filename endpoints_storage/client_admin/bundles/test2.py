
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property, Provides, Instantiate
from api import ITest2, YCappuccino

@ComponentFactory('test2-Factory')
@Provides(specifications=[ITest2.name, YCappuccino.name])
@Property('_id', "id", "test2")
@Instantiate("test2")
class Test2(ITest2, YCappuccino):
    def __init__(self):
        super(Test2,self).__init__()

        self._activate = True

    def get_display(self):
       return "<p><b>Hello World2</b></p>"

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
