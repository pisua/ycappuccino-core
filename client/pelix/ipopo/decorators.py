
list_components = {}
list_instances = {}
list_requires_by_factory = {}


def ComponentFactoryCall(a_class,  name=None):
    print("ComponentFactoryCall {} {}".format(a_class.__name__, name))
    w_component = ComponentFactory(name)
    list_components[name] = w_component

def InstantiateCall(a_class, **kwargs):
    print("InstantiateCall {} {}".format(a_class.__name__,  kwargs))
    w_instance = Instantiate(kwargs)
    list_instances[kwargs["name"]] = w_instance
    w_factory=kwargs["factory"];
    for w_require in list_requires_by_factory:
        w_require.bind(w_instance)
    w_instance.set_factory(list_components[w_factory])

def RequireCall(a_class, **kwargs):
    print("RequireCall {} {}".format(a_class.__name__,  kwargs))
    w_require = Requires(kwargs)
    w_instance = list_instances[kwargs["instance"]]
    w_factory_name = kwargs["specification"]
    list_requires_by_factory[w_factory_name] = w_require
    w_instance.add_require(w_require)

def PropertyCall(a_class, **kwargs):
    print("PropertyCall {} {}".format(a_class.__name__,  kwargs))


class ComponentFactory(object):

    def __init__(self, name=None,  excluded=None):
        self._name = name
        self._instances = []

    def __call__(self, a_factory_class):
        pass

    def add_instance(self, a_instance):
        self._instances.append(a_instance)

    def get_instances(self):
        return self._instances

def Validate(method):
    """ """
    pass


def Invalidate(method):
    """ """
    pass


class Instantiate(object):

    def __init__(self, name ="", properties=None):
        self._name = name
        self._properties = properties
        self._factory = None
        self.require = []

    def __call__(self, *args, **kwargs):

    def set_factory(self, a_factory):
        self._factory = a_factory
        self._factory.add_instance(self)
        # check all require this factory to notify a new instance
        if self._factory in list_requires_by_factory:
            for w_require in list_requires_by_factory[self._factory]:
                w_require.bind(self)
        if self._is_ok_to_validate():
            # TODO call validated method

    def add_require(self,a_require):
        self.require.append(a_require)


    def _is_ok_to_validate(self):
        w_ok = True
        for a_require in self.require:
            w_ok = w_ok && a_require.is_resolved()
        return w_ok

class Requires(object):

    def __init__(self,  field="", specification="", aggregate=False, optional=False, spec_filter=None, immediate_rebind=False):
        self._field = field
        self._specification = specification
        self._aggregate = aggregate
        self._optional= optional
        self._spec_filter = spec_filter
        self._immediate_rebind = immediate_rebind
        self._instance = None

        if self._specification in list_components:
            w_factory = list_components[self._specification]
            for w_instance in w_factory.get_instances():
                self.bind(w_instance)

    def __call__(self, *args, **kwargs):
        pass

    def bind(self, a_instance):
        self._instance = a_instance

    def is_resolved(self):
        return self._instance is not None