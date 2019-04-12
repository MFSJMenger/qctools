import sys
from functools import wraps
from copy import deepcopy
from string import Template


def substitute_args_kwargs(dct, args, kwargs):

    for key in dct:
        if type(dct[key]) == int:
            dct[key] = args[dct[key]]
        else:
            dct[key] = kwargs[dct[key]]
    return dct


def try_function_decorator(msg, subargs=None):
    """ Tries if Function works, else will raise an Exception """
    msg = Template(msg)

    def _inner_decorator(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # local copy of msg
                out_msg = deepcopy(msg)
                if subargs is not None:
                    #  create local of args dict
                    dct = deepcopy(subargs)
                    #
                    dct = substitute_args_kwargs(dct, args, kwargs)
                    out_msg = out_msg.substitute(dct)
                print(e)
            finally:
                print("Could not execute function '%s': %s"
                      % (func.__name__, out_msg))
                sys.exit()
        return _wrapper
    return _inner_decorator
