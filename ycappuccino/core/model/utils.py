class YDict(object):

    def __init__(self, *a_tuple):
        for t in a_tuple:
            if isinstance(t,dict):
                for k,v in t.items():
                    setattr(self, k, v)