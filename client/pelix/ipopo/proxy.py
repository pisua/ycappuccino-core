
setattr_=object.__setattr__
getattr_=object.__getattribute__


class Instance(object):

    __slots__ = ["_func", "_params", "_kwargs", "_obj", "_loaded", "__weakref__"]

    def __init__(self, func, *params, **kwargs):
        setattr_(self, "_func", func)
        setattr_(self, "_params", params)
        setattr_(self, "_kwargs", kwargs)

        setattr_(self, "_obj", None)
        setattr_(self, "_loaded", False)

    def _get_obj(self):
        """ """
        if not getattr_(self, "_loaded"):
            print("Loading")
            setattr_(self, "_obj", getattr_(self, "_func")(*getattr_(self, "_params"), **getattr_(self, "_kwargs")))
            setattr_(self, "_loaded", True)

        return getattr_(self, "_obj")

    #
    # proxying (special cases)
    #
    def __getattribute__(self, name):
        return getattr(getattr_(self, "_get_obj")(), name)

    def __delattr__(self, name):
        delattr(getattr_(self, "_get_obj")(), name)

    def __setattr__(self, name, value):
        setattr(getattr_(self, "_get_obj")(), name, value)

    def __nonzero__(self):
        return bool(getattr_(self, "_get_obj")())

    def __str__(self):
        return str(getattr_(self, "_get_obj")())

    def __repr__(self):
        return repr(getattr_(self, "_get_obj")())
