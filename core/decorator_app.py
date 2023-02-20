

map_app_class = {}
class App(object):
    # Make copy of original __init__, so we can call it without recursion
    def __init__(self, name):
        self.name = name
        pass

    def __call__(self, obj):
        map_app_class[obj.__name__] = self.name
        return obj



