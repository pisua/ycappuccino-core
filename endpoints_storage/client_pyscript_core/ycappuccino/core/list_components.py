from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Instantiate, BindField, \
    UnbindField, Provides
from pyscript import Element
from ycappuccino.api import IListComponent,YCappuccino

list_component = None
@ComponentFactory('ListComponent-Factory')
@Requires("_list_component", YCappuccino.name, aggregate=True, optional=True)
@Provides(specifications=[IListComponent.name])
@Instantiate("ListComponent")
class ListComponent(IListComponent):
    def __init__(self):
        global list_component;
        list_component = self
        self._list_component = []
        self._map_component = {}


    def call(self, a_comp_name, a_method):
        if a_comp_name in self._map_component.keys():
            getattr(self._map_component[a_comp_name],a_method)()

    @BindField("_list_component")
    def bind_component(self, field, a_service, a_service_reference):
        self._map_component[a_service.id()] = a_service

    @UnbindField("_list_component")
    def unbind_test1(self, field, a_service, a_service_reference):
        del self._map_component[a_service.id()]



    @Validate
    def validate(self, context):
        print("test")


    @Invalidate
    def invalidate(self, context):
        pass
