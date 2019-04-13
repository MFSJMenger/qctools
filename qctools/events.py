from functools import partial
from copy import deepcopy

from .fileinput import pygrep_iterator_lines
from .functions import identity

class Event(object):

    default_settings = {
        'multi': False, # call the event multiple times, till the end of the iterator is reached
        'reset': False, # reset the iterator before calling the event
    }

    def __init__(self, name, event, event_kwargs, func=identity, settings={}):
        """ intialize an event """
        self._name = name
        self._func = None
        self._set_event(event, event_kwargs)
        self._process_func = func
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
        """ set the event """
        if event == 'grep':
            self._pygrep_lines(kwargs)

    @staticmethod
    def _check_keys(set_keys, optional_set_keys, kwargs): 

        keys = {}
        replace_keys = {}

        for key in set_keys:
            if key not in kwargs:
                raise Exception('Keyword "%s" needs to be set in grep Event' % key)
        
        for key in optional_set_keys:
            if key not in kwargs:
                raise Exception('Keyword "%s" needs to be set in grep Event' % key)
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

        self._keys, self._replace_keys = self._check_keys(set_keys, keys, kwargs)

        self._func = partial(pygrep_iterator_lines, keyword = kwargs['keyword'])

    def _get_needed_kwargs(self, dct):

        kwargs = deepcopy(self._keys)
        for key, dct_key in self._replace_keys.items():
            if dct_key not in dct: 
                raise Exception('Event "%s" needs to be set and called before this Event "%s"' % key, self._name)
            kwargs[key] = dct[dct_key]
            if kwargs[key] is None:
                raise Exception('Event "%s" needs to be called before this Event "%s"' % key, self._name)
        return kwargs

    def trigger(self, iterator, dct):
        """ trigger the event using interator as input """
        kwargs = self._get_needed_kwargs(dct)
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
            result.append(self._process_func(tmp_result))
        return result, ierr

    def _trigger(self, iterator, kwargs):
        """ trigger an event once """
        result, ierr = self._func(iterator, **kwargs)
        if ierr != -1:
            result = self._process_func(result)
        return result, ierr
