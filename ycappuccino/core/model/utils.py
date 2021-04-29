class YDict(object):
    def __init__(self, a_dict):
        for k, v in a_dict.items():
            setattr(self, k, v)