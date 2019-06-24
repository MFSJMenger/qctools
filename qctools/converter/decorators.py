from functools import update_wrapper


class GetFunctionRepr(object):

    def __init__(self, repr, func):
        self._repr = repr
        self._func = func
        update_wrapper(self, func)

    def __call__(self, *args, **kw):
        return self._func(*args, **kw)

    def __repr__(self):
        return self._repr(self._func)

    def __str__(self):
        return self._repr(self._func)


def with_repr(reprfun):
    def _wrap(func):
        return GetFunctionRepr(reprfun, func)
    return _wrap
