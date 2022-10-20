from ycappuccino.core.model.decorators import Item, Property
from ycappuccino.core.model.utils import YDict
from ycappuccino.core.model.decorators import get_item_by_class


@Item(collection="models", name="model", plural="models", abstract=True, app="core")
class Model(YDict):
    """ default bean that represent a model to manipulate / store in a database """
    def __init__(self, a_dict=None):
        # init id regarding the dict or model pass
        self._dict = a_dict if a_dict is not None else {}
        self._id = None
        self._mongo_model = {}

    def on_read(self):
        w_item = get_item_by_class(self.__class__)
        for key in self._dict.keys():
            w_method = "";
            w_key_model = "";
            if key == "_id":
                w_key_model = "_id"
            else:
                w_key_model = "_"+key

            if w_key_model is not None and w_key_model in self.__dict__:
                self.__dict__[w_key_model] = self._dict[key]
                self._mongo_model[key] = self._dict[key]

    def on_update(self):
        w_item = get_item_by_class(self.__class__)
        for key in self._dict.keys():
            w_method = "";
            w_key_model = "";
            if key == "_id":
                w_method = "id"
                w_key_model = "_id"
            else:
                w_method = key
                w_key_model = key

            try:
                w_method_obj = getattr(self, w_method)
            except:
                w_method_obj = None

            if w_method_obj is not None :
                w_method_obj(self._dict[w_key_model])
            else:
                self._mongo_model[w_key_model] = self._dict[w_key_model]

    @Property(name="_id")
    def id(self, a_value=None):
        self._id = a_value

    def get_storage_model(self):
        return self["_mongo_model"]

    def update(self, a_dict):
        """ update current model dictionnary with the one in parameter. or the model dict in parameter"""
        w_dict = a_dict.__dict__ if isinstance(a_dict,Model) else a_dict
        for k, v in w_dict.items():
            if k != "_mongo_model":
                setattr(self, k, v)
            else:
                for k2, v2 in w_dict["_mongo_model"].items():
                    self._mongo_model[k2] = v2
