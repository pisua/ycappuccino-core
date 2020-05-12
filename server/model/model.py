

class Model(object):
    def __init__(self, a_dict):
        for k, v in a_dict.items():
            setattr(self, k, v)


class Item(Model):

    def __init__(self, *args, **kwargs):
        super(Model,self).__init__(args,kwargs)

    def get_collection_name(self):
        """ """
        return self.collection

    def get_shema(self):
        return self.schema
