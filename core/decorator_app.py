class App(object):
    # Make copy of original __init__, so we can call it without recursion
    def __init__(self, name):
       pass

    def __call__(self, obj):

        return obj


