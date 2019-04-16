from functools import partial
from copy import deepcopy

from .fileinput import pygrep_iterator_lines
from .fileinput import pyxgrep_iterator_lines
from .functions import identity


def event_getter_pygrep(func=pygrep_iterator_lines):
    """ Predefined pygrep event based on pygrep_iterator_lines"""

    optional_keys = {
            'ilen': int,
            'ishift': int,
            }
    defined_keys = ['keyword']

    return optional_keys, defined_keys, func


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
        if type(entry) != types[i]:
            raise Exception(("Entry has to be of type '%s'", str(types[i])))


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


class _BasicEvent(object):
    """ Basic Class contains all possible event types """

    _events = {
            'grep': event_getter_pygrep,
            'xgrep': partial(event_getter_pygrep, func=pyxgrep_iterator_lines),
            'pass': _check_event_getter([{}, [], pass_function]),
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


class Event(_BasicEvent):
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
        'multi': False,  # call the event multiple times,
                         # till the end of the iterator is reached
        'reset': False,  # reset the iterator before calling the event
        'delete': False, # delete the file afterwards
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
        self._process_func = func
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

    @property
    def delete(self):
        return self._settings['delete']

    def post_process(self, value):
        """
        function to perform postprocessing on the data generated by the event
        """



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
            raise Exception('Event "%s" unknown, please register before usage'
                            % event)

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
                raise Exception('Keyword "%s" needs to be set in grep Event'
                                % key)
            keys[key] = kwargs[key]

        for key in optional_set_keys:
            if key not in kwargs:
                raise Exception('Keyword "%s" needs to be set in grep Event'
                                % key)
            if type(kwargs[key]) == optional_set_keys[key]:
                keys[key] = kwargs[key]
            else:
                replace_keys[key] = kwargs[key]

        return keys, replace_keys

    def _get_needed_kwargs(self, dct):

        kwargs = deepcopy(self._keys)
        for key, dct_key in self._replace_keys.items():
            if dct_key not in dct:
                raise Exception(('Event "%s" needs to be set ' % key,
                                 'and called before this Event "%s"'
                                 % self._name))
            kwargs[key] = dct[dct_key]
            if kwargs[key] is None:
                raise Exception(('Event "%s" needs to be called ',
                                'before this Event "%s"')
                                % key, self._name)
        return kwargs

    def trigger(self, iterator, arg_dct):
        """ trigger the event

            Args:
                iterator (iterator):
                        basic iterator used for the event call

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
        if self._settings['multi'] is False:
            return self._trigger(iterator, kwargs)
        else:
            return self._multi_trigger(iterator, kwargs)

    def _multi_trigger(self, iterator, kwargs):
        """ trigger an event multiple times """
        result = []
        while True:
            tmp_result, ierr = self._func(iterator, **kwargs)
            if ierr == -1:
                break
            result.append(self._process_func(tmp_result,
                                             **self._process_func_kwargs))
        return result, ierr

    def _trigger(self, iterator, kwargs):
        """ trigger an event once """
        result, ierr = self._func(iterator, **kwargs)
        if ierr != -1:
            result = self._process_func(result, **self._process_func_kwargs)
        return result, ierr


reset_event = Event('reset', 'pass', {}, settings={'reset': True})
