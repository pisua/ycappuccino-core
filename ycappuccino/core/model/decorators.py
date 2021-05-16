# decorators to describe item and element to store in mongo if it's mongo element
import functools
from ycappuccino.core.model.utils import YDict
primitive = (int, str, bool, float, )

map_item = {}


class Item(object):
    # Make copy of original __init__, so we can call it without recursion
    def __init__(self, collection, name, module="system", secureRead=False,secureWrite=False):
        self._meta_name = name
        self._meta_collection = collection
        self._meta_module = module

        w_model = YDict({
            "id": name,
            "module": module,
            "collection": collection,
            "secureRead":secureRead,
            "secureWrite": secureWrite

        })
        map_item[name] = w_model

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
