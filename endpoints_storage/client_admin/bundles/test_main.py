
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property, Instantiate, BindField, UnbindField, Provides
from pyscript import Element
from api import ITestMain, ITest1, ITest2, YCappuccino


@ComponentFactory('TestMain-Factory')
@Requires("_test1", ITest1.name)
@Requires("_test2", ITest2.name)
@Provides(specifications=[ITestMain.name, YCappuccino.name])
@Property('_id', "id", "testMain")
@Instantiate("testMain")
class TestMain(ITestMain,YCappuccino):

    def __init__(self):
        super(TestMain,self).__init__()
        self._test1 = None
        self._test2 = None

    def activate_test_1(self):
        self._test1.set_activate(True)
        self._test2.set_activate(False)
        self.display()

    def activate_test_2(self):
        self._test1.set_activate(False)
        self._test2.set_activate(True)
        self.display()

    def display(self):

        w_html = '<button class="button" id="test1" type="submit" onclick="test(\''+self.id()+'\',\'activate_test_1\')">Test1</button>'
        w_html = w_html+'<button class="button" id="test2" type="submit" onclick="test(\''+self.id()+'\',\'activate_test_2\')">Test2</button>'

        if self._test1 is not None and  self._test1.is_activate() :
            w_html =w_html + self._test1.get_display()
        if self._test2 is not None and self._test2.is_activate() :
            w_html =w_html + self._test2.get_display()

        manual_div = Element("main")
        manual_div.element.innerHTML = w_html


    @BindField("_test1")
    def bind_test1(self, field, a_service, a_service_reference):
        self._test1 = a_service
        print("bind test1")
        self.display()
    @UnbindField("_test1")
    def unbind_test1(self, field, a_service, a_service_reference):
        self._test1 = None
        self.display()

    @BindField("_test2")
    def bind_test2(self, field, a_service, a_service_reference):
        self._test2 = a_service
        print("bind test2")
        self.display()

    @UnbindField("_test2")
    def unbind_test2(self, field, a_service, a_service_reference):
        self._test2 = None
        self.display()

    @Validate
    def validate(self, context):


        self.display()

    @Invalidate
    def invalidate(self, context):
        pass
