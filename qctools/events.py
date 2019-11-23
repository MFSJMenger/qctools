from functools import partial
from copy import deepcopy
#
from .fileinput import pygrep_iterator_lines
from .fileinput import pyxgrep_iterator_lines
# Functions
from .functions import identity
from .functions import str_split, str_split_multi
from .functions import map_function_by_lines, map_function
# Exceptions
from .exceptions import CustomErrorMsg
# Expression
from .expression import MathExpression


class UnkownProcessFunction(Exception):
    pass


class MissingEvent(CustomErrorMsg):

    def __init__(self, event):
        text = """Event '%s' needs to be set """
        self.custom_error_msg = text % (event)


class UnkownEvent(CustomErrorMsg):

    def __init__(self, event):
        self.custom_error_msg = ('Event "%s" unknown, please register before usage'
                                 % event)


class MissingEventKeyword(CustomErrorMsg):

    def __init__(self, keyword):
        self.custom_error_msg = ("Keyword '%s' needs to be set in Event"
                                 % keyword)


class MissingEventCall(CustomErrorMsg):

    def __init__(self, previous_event, current_event):
        text = """Event '%s' needs to be set and called before Event '%s'"""
        self.custom_error_msg = text % (previous_event, current_event)


def event_getter_pygrep(func=pygrep_iterator_lines):
    """ Predefined pygrep event based on pygrep_iterator_lines"""

    keyword_args = {
            'ilen': int,
            'ishift': int,
            }
    args = ['keyword']

    return keyword_args, args, func


def event_getter_join():

    keyword_args = {
            'ilen': int,
            'ishift': int,
            }

    args = ['events']

    def join_events(events):
        pass

    return keyword_args, args, join_events


def pass_function(*args, **kwargs):
    return None, 1


def _create_getter(dct, lst, func):
    """ helper to convert dct, list, func into a
    getter function that returns these values"""
    def _wrapper():
        return dct, lst, func
    return _wrapper


def _check_types(iterator, types):
    for i, entry in enumerate(iterator):
        if not isinstance(entry, types[i]):
            raise TypeError(("Entry has to be of type '%s'" % str(types[i])))


def _check_event_getter(getter):
    """ check getter """

    getter_func = None

    if hasattr(getter, '__call__'):
        getter_func = getter
        getter = getter_func()

    if type(getter) not in [tuple, list]:
        raise Exception("getter needs to be tuple or list, or return these")
    # check lens
    if len(getter) != 3:
        raise Exception(("getter needs to be a tuple/list",
                         "with exactly 3 entries!"))
    # check types
    _check_types(getter[:2], [dict, list])
    if not hasattr(getter[2], '__call__'):
        raise Exception("getter[2] has to be callable")

    if getter_func is None:
        getter_func = _create_getter(getter[0], getter[1], getter[2])

    return getter_func


def register_event_type(event_name, getter):
    """
    register new event type

    Args:

        event_name (str):
                Name of the event that

        getter (function or list/tuple):
                If list/tuple:
                    needs to be a list with three entries
                    (dct, lst, func)

                If function:
                    a getter function to get informations for the
                    event. The function should return a tuple:
                    (dct, lst, func)

                dct (dictionary):
                    contains all arguments for function
                    that need to be set with `func_kwargs` and that could
                    be loaded from data of previous events

                lst (list):
                    contains all arguments that are taken directly
                    from `func_kwargs`

                func (function):
                    is a python function that takes one argument and has to
                    return a tuple of two values, the first being the actuall
                    output the second being an error code (integer), with -1
                    meaning the event call was not successful.

    Note:
    -----
    Register a new possible event type to the Event class


    Example:
    --------
    define a event getter print5, that prints `Value is set to 5`
    when the event is triggered

    >>> def print5():
    ...     def prt5(*arg, **kwargs):
    ...         print("Value is set to 5")
    ...         return 5, 1
    ...     return {}, [], prt5

    >>> register_event_type("prt5", print5)

    >>> prt5 = Event('prt5', 'prt5', {})

    >>> prt5.trigger(1, {})
    5, 1

    Or as a list

    >>> def prt5(*arg, **kwargs):
    ...     print("Value is set to 5")
    ...     return 5, 1

    >>> register_event_type("prt5", [{}, [], prt5])

    >>> prt5 = Event('prt5', 'prt5', {})

    >>> prt5.trigger(1, {})
    5, 1
    """
    _BasicEvent._register_event(event_name,  _check_event_getter(getter))


def print_possible_events():
    """print all registered events"""
    print("Registered Events:")
    print(_BasicEvent.get_possible_events())
    print("******************************")


class _CoreEvent(object):
    pass


class _BasicEvent(_CoreEvent):
    """ Basic Class contains all possible event types """

    _events = {
            'grep': event_getter_pygrep,
            'xgrep': partial(event_getter_pygrep, func=pyxgrep_iterator_lines),
            'pass': _check_event_getter([{}, [], pass_function]),
            '__joined_event': ''
    }

    @property
    def events(self):
        return self._events

    @classmethod
    def _register_event(cls, key, value):
        cls._events[key] = value

    @classmethod
    def get_possible_events(cls):
        return ", ".join(cls._events.keys())


class _BasicEventProcessFunctions(object):
    """Class to store all possible event types"""

    predefined_functions = {
            'split': {'func': ['idx', str_split, str_split_multi],
                      'grep': [map_function_by_lines, False],
                      'xgrep': [map_function, True]}
            }

    @classmethod
    def _setup_split(cls, event_type, func_kwargs):

        if type(func_kwargs['idx']) != int:
            line_func = str_split_multi
        else:
            line_func = str_split

        if 'bylines' not in func_kwargs:
            bylines = cls.predefined_functions['split'][event_type][1]
        else:
            bylines = func_kwargs['bylines']
            del func_kwargs['bylines']

        if bylines is True:
            func_kwargs = {'func': partial(line_func, **func_kwargs)}
            if event_type == 'grep':
                func = map_function_by_lines
            elif event_type == 'xgrep':
                func = map_function
        else:
            func = line_func
        return func, func_kwargs

    @classmethod
    def _get_process_function(cls, event_type, func, func_kwargs):
        """ """
        if (hasattr(func, '__call__')):
            pass
        elif func == 'split':
            func, func_kwargs = cls._setup_split(event_type, func_kwargs)
        else:
            raise UnkownProcessFunction("Unkown process function")

        return func, func_kwargs


class Event(_BasicEvent, _BasicEventProcessFunctions):
    """
    Basic Event class used for event handlers

    Args:
        name (str):
                Name of the event

        event_type (str):
                Type of the event, suported e.g. 'grep'
                but you can also register your own

        event_type_kwargs (dct):
                Arguments for the event type specific function

        func (function(arg1), optional):
                Single position argument function that is invoced after
                the event was triggered to postprocess the output.
                additional arguments can be passed with `func_kwargs` as
                `keyword arguments`

        func_kwargs (dct):
                dct of keys passed to `func` additionally to the
                single output of the event call

        process_func (function(arg1), optional):
                Single position argument function that is invoced after
                all events are called by the event handler.
                It takes the result of the event as input, therefore
                it should handle the case, the value is None!
                additional arguments can be passed with `process_func_kwargs` as
                `keyword arguments`

        process_func_kwargs (dct):
                dct of keys passed to `process_func` additionally to the
                single value of the final event call

        settings (dct, optional):
                Additional settings for the Event
                default_settings = {

                # call event multiple times, till ierr is -1

                'multi': False,

                # reset iterator before the event is called

                'reset': False,

                'delete': False, # delete the result as postprocess

                }

    Notes
    -----
    A `Event` class used together with Event handlers to
    trigger certain events.

    Examples
    --------

    Register event to get NAtoms entry from gaussian output:
    The event uses the predefinded grep command and then calls
    calls str split on it

    >>> NAtoms = Event('NAtoms',
    ...                'grep', {'keyword': 'NAtoms=',
    ...                         'ilen': 1,
    ...                         'ishift': 0},
    ...                func=str_split, idx=1, typ=int)
    ...                func_kwargs={'idx': 1, 'typ': int})
    >>> Example_data = [ "NAtoms= 5", ]
    >>> result, ierr = NAtoms.trigger(Example_data)
    >>> print(result)
    5
    """

    default_settings = {
        'multi': False,   # call the event multiple times,
                          # till the end of the iterator is reached
        'reset': False,   # reset the iterator before calling the event
        'delete': False,  # delete the file afterwards
    }

    def __init__(self, name,
                 event_type, event_type_kwargs,
                 func=identity, func_kwargs={},
                 process_func=identity, process_func_kwargs={},
                 settings={}):
        """ intialize an event """
        self._name = name
        self._func = None
        self._choose_event(event_type, event_type_kwargs)
        self._process_func, func_kwargs = self._get_process_function(event_type, func, func_kwargs)
        self._process_func_kwargs = func_kwargs
        # initialize settings
        self._settings = {}
        self._update_settings(settings)

    def __str__(self):
        return ""

    @property
    def name(self):
        return self._name

    @property
    def reset(self):
        return self._settings['reset']

    @reset.setter
    def reset(self, value):
        self._settings['reset'] = value

    @property
    def delete(self):
        return self._settings['delete']

    @property
    def multi(self):
        return self._settings['multi']

    @property
    def nmax(self):
        return self._settings.get('nmax', -1)

    @nmax.setter
    def nmax(self, value):
        self._settings['nmax'] = value

    @multi.setter
    def multi(self, value):
        self._settings['multi'] = value

    @property
    def event_type(self):
        return self._event_type

    def post_process(self, value):
        """ function to perform postprocessing on the data generated by the event """
        pass

    def _update_settings(self, settings):
        """ updates the settings """
        for key in settings:
            self._settings[key] = settings[key]

        for key in self.default_settings:
            if key not in self._settings:
                self._settings[key] = self.default_settings[key]

    def _choose_event(self, event, kwargs):
        """ choose your event """

        if event not in self.events:
            raise UnkownEvent(event)

        self._event_type = event
        keys, set_keys, self._func = self.events[event]()

        self._keys, self._replace_keys = self._check_keys(set_keys,
                                                          keys, kwargs)

    @staticmethod
    def _check_keys(set_keys, optional_set_keys, kwargs):
        """

        Args:

            set_keys (list):
                    List of keywords that need to be set in kwargs,
                    they are not checked but need to be defined

            optional_set_keys (dct):
                    dct with the name of the argument as key and the
                    type as setting

            kwargs (dct):
                    dct with the keys provided by the user,
                    if `key` in optional_set_keys and
                    type(kwargs[key]) == optional_set_keys[key]
                    then set the key, else expect that the
                    argument for that key is provided by the
                    `arg_dct` of the `trigger()` function!

        Returns:

        """

        keys = {}
        replace_keys = {}

        for key in set_keys:
            if key not in kwargs:
                raise MissingEventKeyword(key)
            keys[key] = kwargs[key]

        for key in optional_set_keys:
            if key not in kwargs:
                raise MissingEventKeyword(key)
            if type(kwargs[key]) == optional_set_keys[key]:
                keys[key] = kwargs[key]
            else:
                # convert given value to MathExpression
                replace_keys[key] = MathExpression(kwargs[key])

        return keys, replace_keys

    def _get_needed_kwargs(self, dct):
        # copy args
        kwargs = deepcopy(self._keys)
        #
        for key, expr in self._replace_keys.items():
            kwargs[key] = expr.eval(dct)
            if kwargs[key] is None:
                raise MissingEventCall(key, self._name)
        return kwargs

    def trigger(self, passed_value, arg_dct):
        """ trigger the event

            Args:
                passed_value:
                        value passed by the event handler, most cases an iterator

                arg_dct (dct):
                        Dictionary conatining results of previous events,
                        can be used to pass results of previous events
                        as input to the `event function`

            Results:
                result (pyobj):
                        result of the event function call, if 'multi' was
                        set in the event settings, this is a list of the
                        output of all the events
                ierr (int):
                        Error code, used to check if event was triggered or not


            Notes
            -----
            A `Event` class used together with Event handlers to
            trigger certain events.

            Examples
            --------

            >>> NAtoms = Event('NAtoms',
            ...                'grep', {'keyword': 'NAtoms=',
            ...                         'ilen': 1,
            ...                         'ishift': 0},
            ...                func=str_split, idx=1, typ=int)
            ...                func_kwargs={'idx': 1, 'typ': int})
            >>> Example_data = [ "NAtoms= 5", ]
            >>> result, ierr = NAtoms.trigger(Example_data)
            >>> print(result)
            5
        """
        kwargs = self._get_needed_kwargs(arg_dct)

        if isinstance(self.nmax, int):
            nmax = self.nmax
        else:
            nmax = arg_dct[self.nmax]

        if self.multi is False:
            return self._trigger(passed_value, kwargs)
        else:
            return self._multi_trigger(passed_value, kwargs, nmax=nmax)

    def _multi_trigger(self, iterator, kwargs, nmax=-1):
        """ trigger an event multiple times """
        result = []
        counter = 0
        while True:
            if counter == nmax:
                break
            tmp_result, ierr = self._func(iterator, **kwargs)
            if ierr == -1:
                break
            result.append(self._process_func(tmp_result,
                                             **self._process_func_kwargs))
            counter += 1
        return result, ierr

    def _trigger(self, iterator, kwargs):
        """ trigger an event once """
        result, ierr = self._func(iterator, **kwargs)
        if ierr != -1:
            result = self._process_func(result, **self._process_func_kwargs)
        return result, ierr


class JoinedEvent(_CoreEvent):

    def __init__(self, events):
        self._events = events
        self._reset_events()
        self._settings = {}

    @property
    def nmax(self):
        return self._settings.get('nmax', -1)

    @nmax.setter
    def nmax(self, value):
        self._settings['nmax'] = value

    @property
    def reset(self):
        return False

    @property
    def delete(self):
        return False

    def post_process(self, value):
        return value

    @property
    def events(self):
        return self._events

    def _reset_events(self):
        #
        for event in self.events:
            event.multi = False
            event.reset = False

    def trigger(self, passed_value, arg_dct):
        return self._trigger(passed_value, arg_dct)

    def _trigger(self, passed_value, arg_dct):
        results = dict((event.name, []) for event in self.events)

        if isinstance(self.nmax, int):
            nmax = self.nmax
        else:
            nmax = arg_dct[self.nmax]

        counter = 0
        while True:
            if counter == nmax:
                break
            for event in self.events:
                result, ierr = event.trigger(passed_value, arg_dct)
                if ierr == 1:
                    results[event.name].append(result)
            if ierr == -1:
                break
            counter += 1
        return results, ierr


def join_events(*args):
    return JoinedEvent(args)


reset_event = Event('reset', 'pass', {}, settings={'reset': True})
