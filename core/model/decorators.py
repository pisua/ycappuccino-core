# decorators to describe item and element to store in mongo if it's mongo element
import functools
from ycappuccino.core.model.utils import YDict
primitive = (int, str, bool, float, )

# identified item by id
map_item = {}
# identified item by class name
map_item_by_class = {}
# identified list of ref by class name on source item
map_item_link_by_class = {}
# identified list of ref by item name target
map_item_link_by_target = {}


def get_map_items():
    w_items = []
    for w_key in map_item:
        w_items.append(YDict(map_item[w_key]))
    return w_items;




class Item(object):
    # Make copy of original __init__, so we can call it without recursion
    def __init__(self, collection, name, module="system", secureRead=False,secureWrite=False):
        self._meta_name = name
        self._meta_collection = collection
        self._meta_module = module

        w_model = {
            "id": name,
            "module": module,
            "collection": collection,
            "secureRead": secureRead,
            "secureWrite": secureWrite,
            "refs": [],
            "reverse_refs": []
        }
        map_item[name] = w_model
        map_item_by_class[self.get_class_name()] = w_model
        self.add_refs(w_model)
        self.add_reverse_refs(name, w_model)

    def __call__(self, obj):
        return obj

    def get_class_name(self):
        return self.__class__.__name__

    def add_refs(self, a_model):
        if self.get_class_name() in map_item_link_by_class:
            for w_ref in map_item_link_by_class:
                # retrieve item from ref if it's not resolved
                if "item" not in w_ref and  w_ref["item_name"] in map_item:
                    w_ref["item"] = map_item[w_ref.item_name]
                # add the refs
                a_model["refs"].append(w_ref)

    def add_reverse_refs(self, name, a_model):
        if name in map_item_link_by_target:
            for w_ref in map_item_link_by_target[name]:
                # retrieve item from ref if it's not resolved
                if "item" not in w_ref and w_ref["item_name"] in map_item:
                    w_ref["item"] = map_item[w_ref["item_name"]]
                # add the refs
                a_model["reverse_refs"].append(w_ref)


class ItemReference(object):
    # Make copy of original __init__, so we can call it without recursion
    def __init__(self, field_name,  item_name, module="system"):
        """
        create a link between item
        :param field_name:
        :param item_name: 
        :param module: 
        """
        if self.__class__.__name__ not in map_item_link_by_class:
            map_item_link_by_class[self.__class__.__name__] = []

        w_ref = {
            "local_field": field_name,
            "item_name": item_name,
            "module_name": module,
            "class": self.__class__.__name__
        }

        map_item_link_by_class[self.__class__.__name__].append(w_ref)
        if item_name not in map_item_link_by_target:
            map_item_link_by_target[item_name] = []

        map_item_link_by_target[item_name].append(w_ref)
        # Item decoration has been processed
        if item_name in map_item:
            w_ref["item"] = map_item[item_name]
        self.add_ref(w_ref)
        self.add_reverse_refs(item_name,w_ref )


    def add_reverse_refs(self, item_name, a_ref):
        if item_name in map_item:
            if "reverse_refs" not in map_item[item_name]:
                map_item[item_name]["reverse_refs"] = []

            map_item[item_name]["reverse_refs"].append(a_ref)

    def get_class_name(self):
        return self.__class__.__name__

    def add_ref(self, a_ref):
        if self.get_class_name() in map_item_by_class:
            if "refs" not in map_item_by_class[self.get_class_name()]:
                map_item_by_class[self.get_class_name()]["refs"] = []

            map_item_by_class[self.get_class_name()]["refs"].append(a_ref)

    def __call__(self, obj):

        return obj

def Property(name):
    """ decoration that manage property with another collection """
    def decorator_property(func):
        @functools.wraps(func)
        def wrapper_proprety(*args, **kwargs):
            value = func(*args, **kwargs)
            if "_mongo_model" not in  args[0].__dict__:
                args[0]._mongo_model = {}
            if isinstance(args[1],YDict):
                args[0]._mongo_model[name] = args[1]._mongo_model
            else:
                args[0]._mongo_model[name] = args[1]
            return value
        return wrapper_proprety
    return decorator_property


def Reference(name):
    """ decoration that manage reference with another collection """
    def decorator_reference(func):
        @functools.wraps(func)
        def wrapper_reference(*args, **kwargs):
            value = func(*args)
            if "_mongo_model" not in  args[0].__dict__:
                args[0]._mongo_model = {}
            if isinstance(args[1],YDict):
                args[0]._mongo_model[name] = {
                   "ref": args[1].id
                }
            else:
                args[0]._mongo_model[name] = {
                    "ref": args[1]
                }
            if len(args) > 2 and isinstance(args[2],dict):
                # admit dictionnary property of the relation we add it
                args[0]._mongo_model[name]["properties"] = args[2]

            return value
        return wrapper_reference
    return decorator_reference


if __name__ == "__main__":

    @Item(collection="col", name="name")
    class Test(object):

        def __init__(self):
            self._toto = "toto"
            self._name = None

        @Property(name="foo")
        def name(self, a_value):
            self._name = a_value


    test = Test()
    test.name("test")
    print(test.__dict__)

    test2 = Test()
    test2.name(test)
    print(test2.__dict__)
