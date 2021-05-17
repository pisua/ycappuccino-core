from ycappuccino.core.model.decorators import Item, Property
from ycappuccino.core.model.utils import YDict

@Item(collection="models",name="model")
class Model(YDict):
    """ default bean that represent a model to manipulate / store in a database """
    def __init__(self, a_dict=None):
        super().__init__(a_dict)
        # init id regarding the dict or model pass


        if a_dict is not None :
            if isinstance(a_dict, Model):

                self.id = a_dict.id
            if isinstance(a_dict, dict):
                if "_id" in a_dict:
                    self.id = a_dict["_id"]
                elif "id" in a_dict:
                    self.id = a_dict["id"]

            else:
                self.id = None
        if "_id" in self.__dict__:
            del self.__dict__["_id"]
    @Property(name="_id")
    def id(self, a_value):
        self.id = a_value

    def update(self, a_dict):
        """ update current model dictionnary with the one in parameter. or the model dict in parameter"""
        w_dict = a_dict.__dict__ if isinstance(a_dict,Model) else a_dict
        for k, v in w_dict.items():
            if k != "_mongo_model":
                setattr(self, k, v)
            else:
                for k2, v2 in w_dict["_mongo_model"].items():
                    self._mongo_model[k2] = v2
