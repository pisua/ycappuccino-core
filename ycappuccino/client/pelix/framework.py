

framework = None

def get_framework():
    return framework

def create_framework():
    """
    Creates a Pelix framework, installs the given bundles and returns its
    instance reference.
    If *auto_start* is True, the framework will be started once all bundles
    will have been installed
    If *wait_for_stop* is True, the method will return only when the framework
    will have stopped. This requires *auto_start* to be True.
    If *auto_delete* is True, the framework will be deleted once it has
    stopped, and the method will return None.
    This requires *wait_for_stop* and *auto_start* to be True.

    :param bundles: Bundles to initially install (shouldn't be empty if
                    *wait_for_stop* is True)
    :param properties: Optional framework properties
    :param auto_start: If True, the framework will be started immediately
    :param wait_for_stop: If True, the method will return only when the
                          framework will have stopped
    :param auto_delete: If True, deletes the framework once it stopped.
    :return: The framework instance
    :raise ValueError: Only one framework can run at a time
    """
    # create map of factory and instance

    framework = Framework()
    return framework

class Factory(object):

    def __init__(self, a_factory_name):
        self._requires = [] # list of requires




class Framework(object):

    def __init__(self):
        self._map_factory = {}
        self._map_component = {}

    def add_factory(self,a_factory_name, a_factory_class):
        """ a factory name and factory description """
        print("add_factory {}, {}".format(a_factory_name,a_factory_class))

        if a_factory_name not in self._map_factory:
            self._map_factory[a_factory_name]=[]
        self._map_factory[a_factory_name].append(a_factory_class)

    def add_require(self, a_factory_name, a_factory):
        """ a factory name and factory description """
        print("add_require {}, {}".format(a_factory_name,a_factory))

        if a_factory_name not in self._map_factory:
            self._map_factory[a_factory_name] = []
        self._map_factory[a_factory_name].append(a_factory)

    def instantiate(self, a_instance_name, a_factory_name):
        print("instantiate {}, {}".format(a_instance_name,a_factory_name))

        if a_instance_name not in self._map_component:
            self._map_component[a_instance_name] = a_factory_name

    def start(self):
        # regarding every component start framework by validating resolve component
        pass