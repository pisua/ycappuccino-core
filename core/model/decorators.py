# decorators to describe item and element to store in mongo if it's mongo element
import functools
from ycappuccino.core.model.utils import YDict
import sys

primitive = (int, str, bool, float, )

# identified item by id
map_item = {}
# identified item by class name
map_item_by_class = {}
# identified list of ref by class name on source item
map_item_link = {}


def get_item(a_id):
    return map_item[a_id]

def get_map_items():
    w_items = []
    for w_key in map_item:
        w_items.append(map_item[w_key])
    return w_items



def get_map_items_emdpoint():
    w_items = []
    for w_key in map_item:
        w_dict = map_item[w_key].copy()
        del w_dict["_class"]
        del w_dict["_class_obj"]

        w_items.append(w_dict)
    return w_items


def has_father_item(a_item_id):
    return map_item[a_item_id].father is not None


def get_sons_item(a_item_id):
    w_list_son = []
    for w_item in map_item.values():
        if w_item.father == a_item_id:
            w_list_son.append(w_item)
    return w_list_son


def get_sons_item_id(a_item_id):
    w_list_son = [a_item_id]
    w_item_father = map_item[a_item_id]
    for w_item in map_item.values():
        if w_item["father"] is not None and w_item["father"] == w_item_father["_class"]:
            w_list_son.append(w_item["id"])
    return w_list_son

class Item(object):
    # Make copy of original __init__, so we can call it without recursion
    def __init__(self, collection, name, plural, abstract=False,  module="system", app="core", secureRead=False,secureWrite=False):
        self._meta_name = name
        self._meta_collection = collection
        self._meta_module = module
        self._item = {
            "id": name,
            "module": module,
            "abstract": abstract,
            "collection": collection,
            "plural": plural,
            "secureRead": secureRead,
            "secureWrite": secureWrite,
            "app":app,
            "schema":{
                "$id": name,
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "title": name,
                "type": "object",
                "properties": {}
            },
            "empty":None
        }

    def __call__(self, obj):
        self._super_class = obj.__bases__[0].__name__ if len(obj.__bases__) > 0 and obj.__bases__[0].__name__ != "YDict" else None;
        self._class = obj.__name__
        self._item["father"] = self._super_class
        self._item["_class"] = self._class
        self._item["_class_obj"] = obj

        if self._class not in map_item_by_class:
            map_item_by_class[self._item["_class"]] = self._item

        w_id = self._item["id"]
        if w_id not in map_item:
            map_item[w_id] = {}
        map_item[w_id] = map_item_by_class[self._item["_class"]]
        map_item[w_id]["id"] = w_id
        map_item[w_id]["module"] = self._item["module"]
        map_item[w_id]["abstract"] = self._item["abstract"]
        map_item[w_id]["collection"] = self._item["collection"]
        map_item[w_id]["plural"] = self._item["plural"]
        map_item[w_id]["secureRead"] = self._item["secureRead"]
        map_item[w_id]["secureWrite"] = self._item["secureWrite"]
        map_item[w_id]["_class"] = self._item["_class"]
        map_item[w_id]["_class_obj"] = self._item["_class_obj"]
        map_item[w_id]["father"] = self._item["father"]
        map_item[w_id]["app"] = self._item["app"]
        map_item[w_id]["schema"] = self._item["schema"]

        # create empty

        return obj





class ItemReference(object):
    # Make copy of original __init__, so we can call it without recursion
    def __init__(self, field,  item):
        self._local_field = field
        self._item_id = item

    def __call__(self, obj):
        a_class = obj.__name__
        a_item_id = self._item_id
        local_field =  self._local_field
        if a_class not in map_item_by_class:
            map_item_by_class[a_class] = {
                "_class": a_class,
                "refs": {},
                "schema":{
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
                    "type": "object",
                    "properties": {}
                }
            }
        w_item = map_item_by_class[a_class]

        if w_item is not None:
            if a_item_id not in w_item["refs"]:
                w_item["refs"][a_item_id]={}
                w_item["refs"][a_item_id][local_field + ".ref"] = {
                    "local_field": local_field + ".ref",
                    "foreign_field": "_id",
                    "item_id": a_item_id
                }
                w_item["schema"]["properties"][local_field] = {
                    "ref":{
                        "type":"string",
                        "description":"reference to {}".format(a_item_id)
                    }
                }

            # TODO reverse ref
        return obj

def Empty():
    """ decoration that manage property with another collection """
    def decorator_property(func):
        @functools.wraps(func)
        def wrapper_proprety(*args, **kwargs):
            value = func(*args, **kwargs)

            w_item = map_item_by_class[value.__class__.__name__]
            w_item["empty"] = value._mongo_model
            return value
        return wrapper_proprety
    return decorator_property



def Property(name, type="string", minLength=None, maxLength=None, minimum=None, exclusiveMinimum=None, maximum=None, exclusiveMaximum=None,  private=False):
    """ decoration that manage property with another collection """
    def decorator_property(func):
        @functools.wraps(func)
        def wrapper_proprety(*args, **kwargs):
            value = func(*args, **kwargs)
            w_name = name
            if name == "_id":
                w_name= "id"
            if "_mongo_model" not in  args[0].__dict__:
                args[0]._mongo_model = {}
            if isinstance(args[1],YDict):
                args[0]._mongo_model[w_name] = args[1]._mongo_model
            else:
                args[0]._mongo_model[w_name] = args[1]

            w_item = map_item_by_class[args[0].__class__.__name__]
            w_item["schema"]["properties"][w_name] = {
                "type": type,
                "description": "{}".format(w_name)
            }
            if minLength:
                w_item["schema"]["properties"][w_name]["minLength"] = minLength

            if maxLength:
                w_item["schema"]["properties"][w_name]["maxLength"] = maxLength

            if minimum:
                w_item["schema"]["properties"][w_name]["minimum"] = minimum

            if exclusiveMinimum:
                w_item["schema"]["properties"][w_name]["exclusiveMinimum"] = exclusiveMinimum

            if maximum:
                w_item["schema"]["properties"][w_name]["maximum"] = maximum

            if exclusiveMaximum:
                w_item["schema"]["properties"][w_name]["exclusiveMaximum"] = exclusiveMaximum


            if "private_property" not in w_item:
                w_item["private_property"] = []
            if private and name not in w_item["private_property"]:
                w_item["private_property"].append(w_name)
            return value
        return wrapper_proprety
    return decorator_property


def Reference(name):
    """ decoration that manage reference with another collection """
    def decorator_reference(func):
        @functools.wraps(func)
        def wrapper_reference(*args, **kwargs):
            value = func(*args)
            if args[0] is not None:
                _add_ref(name,args)
            return value
        return wrapper_reference
    return decorator_reference





def _add_ref(name, args):
    w_model = args[0]
    w_ref_val = args[1]
    if isinstance(w_model, YDict):
        if "_mongo_model" not in w_model.__dict__:
            w_model["_mongo_model"] = {}
        w_model.__dict__["_mongo_model"][name] = {
            "ref": w_ref_val
        }
    else:
        w_model[name]["ref"] = w_ref_val
    # TODO property

def References(name):
    """ decoration that manage reference with another collection """
    def decorator_reference(func):
        @functools.wraps(func)
        def wrapper_reference(*args, **kwargs):
            value = func(*args)
            if args[0] is not None:
                if "_mongo_model" not in args[0].__dict__:
                    args[0]._mongo_model = {}

                if name not in args[0]._mongo_model:
                    args[0]._mongo_model[name]=[]

                w_obj_ref = _add_ref(args)

                args[0]._mongo_model[name].append(w_obj_ref)

                if len(args) > 2 and isinstance(args[2],dict):
                    # admit dictionnary property of the relation we add it
                    w_obj_ref["properties"] = args[2]

                w_item = map_item_by_class[args[0].__name__]
                w_item["schema"]["properties"][name] = {
                    "type": "string",
                    "description": "reference to {}".format(name)
                }
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
