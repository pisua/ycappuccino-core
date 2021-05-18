import inspect
import os
list_component = {}


def ComponentFactoryCall(a_class,  name=None):
    print("ComponentFactoryCall {} {}".format(a_class.__name__, name))


class ComponentFactory(object):

    def __init__(self, name=None,  excluded=None):
        self._name = name

    def __call__(self, a_factory_class):
        print("componentFactory {} ".format(a_factory_class))


def Validate(method):
    pass


def Invalidate(method):

    pass


class Instantiate(object):

    def __init__(self, name, properties=None):
        self._name = name
        self._properties = properties

    def __call__(self, *args, **kwargs):
        print("Instantiate")
        if self._name in list_component and "instances" in list_component[self._name]:
            list_component[self._name]["instances"][self._name] = {
                "instance": self
            }

        elif  self._name in list_component:
            list_component[self._name] = {
                "instances": {}
            }
            list_component[self._name]["instances"][self._name] = {
                "instance": self
            }


class Requires(object):

    def __init__(self,  field, specification, aggregate=False, optional=False, spec_filter=None, immediate_rebind=False):
        self._field = field
        self._specification = specification
        self._aggregate = aggregate
        self._optional= optional
        self._spec_filter = spec_filter
        self._immediate_rebind = immediate_rebind

    def __call__(self, *args, **kwargs):
        print("Requires")
        if self._name in list_component:
            list_component[self._name]["factory"] = self
        else:
            list_component[self._name] = {
                "factory": self,
            }