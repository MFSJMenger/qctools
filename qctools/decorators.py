from functools import wraps
import time


def str_logger(string):
    print(string)


def time_function_decorator(debug=False, logger=str_logger):
    """time a function"""
    def _time_func(func):

        @wraps(func)
        def _timed(*args, **kwargs):
            if debug is False:
                logger('Starting call: %r (%r, %r)' %
                       (func.__name__, args, kwargs))
            else:
                import inspect
                (Iargs, Ivarargs, Ikeywords,
                    Idefaults) = inspect.getargspec(func)
                logger('Starting call: %r (%r)' % (func.__name__, Iargs))
                for i, arg in enumerate(Iargs):
                    # first N elements are arguments
                    if i < len(args):
                        logger("%s = %s" % (arg, args[i]))
                    # the others are given in kwds/defaults
                    else:
                        if arg in kwargs:
                            logger("%s = %s " % (arg, kwargs[arg]))
                        else:
                            logger("%s = %s " % (arg, Idefaults[i-len(args)]))
            ts = time.time()
            result = func(*args, **kwargs)
            te = time.time()
            logger('Finishing call: %r (%r, %r)' %
                   (func.__name__, args, kwargs))
            logger('Execution time = %20.2f sec' %
                   (te-ts))
            return result
        return _timed
    return _time_func
