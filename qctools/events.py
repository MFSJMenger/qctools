from functools import partial
from copy import deepcopy

from .fileinput import pygrep_iterator_lines
from .functions import identity


class Event(object):

    """

    Basic Event class used for event handlers

    Args:
        name (str):
                Name of the event

        event (str):
                Type of the event, suported e.g. 'grep'
                but you can also register your own

        event_kwargs (dct):
                Arguments for the event function

        func (function(arg1), optional):
                Single position argument function,
                additional options can be passed with `func_kwargs` as
                `keyword arguments`

        func_kwargs (dct):
                dct of keys passed to `func` additionally to the
                single output of the event call

        settings (dct, optional):
                Additional settings for the Event
                default_settings = {
                # call event multiple times, till ierr is -1

                'multi': False,

                # reset iterator before the event is called

                'reset': False,
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
    }

    def __init__(self, name,
                 event, event_kwargs,
                 func=identity, func_kwargs={},
                 settings={}):
        """ intialize an event """
        self._name = name
        self._func = None
        self._set_event(event, event_kwargs)
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

    def _update_settings(self, settings):
        """ updates the settings """
        for key in settings:
            self._settings[key] = settings[key]

        for key in self.default_settings:
            if key not in self._settings:
                self._settings[key] = self.default_settings[key]

    def _set_event(self, event, kwargs):
        """ set your event """
        if event == 'grep':
            self._func = self._pygrep_lines(kwargs)
        else:
            raise Exception('Event "%s" unknown, please register it before'
                            % event)

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



        """

        keys = {}
        replace_keys = {}

        for key in set_keys:
            if key not in kwargs:
                raise Exception('Keyword "%s" needs to be set in grep Event'
                                % key)

        for key in optional_set_keys:
            if key not in kwargs:
                raise Exception('Keyword "%s" needs to be set in grep Event'
                                % key)
            if type(kwargs[key]) == optional_set_keys[key]:
                keys[key] = kwargs[key]
            else:
                replace_keys[key] = kwargs[key]
        return keys, replace_keys

    def _pygrep_lines(self, kwargs):
        """ predefined pygrep event """

        keys = {'ilen': int,
                'ishift': int}
        set_keys = ['keyword']

        self._keys = {}
        self._replace_keys = {}

        self._keys, self._replace_keys = self._check_keys(set_keys,
                                                          keys, kwargs)

        return partial(pygrep_iterator_lines, keyword=kwargs['keyword'])

    def _get_needed_kwargs(self, dct):

        kwargs = deepcopy(self._keys)
        for key, dct_key in self._replace_keys.items():
            if dct_key not in dct:
                raise Exception(('Event "%s" needs to be set ',
                                'and called before this Event "%s"')
                                % key, self._name)
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
