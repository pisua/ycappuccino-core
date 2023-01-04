#app="all"
import types
from pprint import pformat

class YDict(object):

    def __init__(self, *a_tuple):
        for t in a_tuple:
            if isinstance(t,dict):
                for k,v in t.items():
                    setattr(self, k, v)

class ProxyMethodWrapper:
    """
    Wrapper object for a method to be called.
    """

    def __init__( self, obj, func, name ):
        self.obj, self.func, self.name = obj, func, name
        assert obj is not None
        assert func is not None
        assert name is not None

    def __call__( self, *args, **kwds ):
        return self.obj._method_call(self.name, self.func, *args, **kwds)

class Proxy(object):

    def __init__(self):
        self._objname = None
        self._obj = None


    def __getattribute__(self, name):
        """
        Return a proxy wrapper object if this is a method call.
        """
        if name.startswith('_'):
            return object.__getattribute__(self, name)
        else:
            att = getattr(self._obj, name)
            if type(att) is types.MethodType:
                return ProxyMethodWrapper(self, att, name)
            else:
                return att

    def __setitem__(self, key, value):
        """
        Delegate [] syntax.
        """
        name = '__setitem__'
        att = getattr(self._obj, name)
        pmeth = ProxyMethodWrapper(self, att, name)
        pmeth(key, value)

    def _call_str(self, name, *args, **kwds):
        """
        Returns a printable version of the call.
        This can be used for tracing.
        """
        pargs = [pformat(x) for x in args]
        for k, v in kwds.iteritems():
            pargs.append('%s=%s' % (k, pformat(v)))

        return '%s.%s(%s)' % (self._objname, name, ', '.join(pargs))

    def _method_call(self, name, func, *args, **kwds):
        """
        This method gets called before a method is called.
        """
        # pre-call hook for all calls.
        try:
            prefunc = getattr(self, '_pre')
        except AttributeError:
            pass
        else:
            prefunc(name, *args, **kwds)

        # pre-call hook for specific method.
        try:
            prefunc = getattr(self, '_pre_%s' % name)
        except AttributeError:
            pass
        else:
            prefunc(*args, **kwds)

        # get real method to call and call it
        rval = func(*args, **kwds)

        # post-call hook for specific method.
        try:
            postfunc = getattr(self, '_post_%s' % name)
        except AttributeError:
            pass
        else:
            postfunc(*args, **kwds)

        # post-call hook for all calls.
        try:
            postfunc = getattr(self, '_post')
        except AttributeError:
            pass
        else:
            postfunc(name, *args, **kwds)

        return rval
