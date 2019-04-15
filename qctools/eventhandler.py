from collections import OrderedDict

from .fileio import file_reading_iterator_raw
from .utils import classfunction_decorator


class EventHandler(object):
    """Class to read information from ASCII text files"""

    _events = OrderedDict()
    _get_iterator = classfunction_decorator(file_reading_iterator_raw)

    def __init__(self, filename, reset=True):
        self._name = filename
        self._reset = reset
        self._values = dict((key, None) for key in self._events.keys())

    @classmethod
    def add_event(cls, name, event):
        cls._events[name] = event

    @property
    def parse(self):
        self._parse_file()

    def _set_iterator(self):
        return self._get_iterator(self._name)

    def _trigger_event(self, iterator, key):
        event = self._events[key]
        # reset iterator before event call
        if event.reset is True:
            iterator = self._set_iterator()
        self._values[key], ierr = event.trigger(iterator, self._values)
        # reset iterator after event call
        if ierr == -1 and self._reset is True:
            iterator = self._set_iterator()
        return iterator, ierr

    def _parse_file(self):
        iterator = self._set_iterator()
        for key in self.keys:
            iterator, ierr = self._trigger_event(iterator, key)

    @property
    def filename(self):
        return self._name

    @property
    def keys(self):
        return self._events.keys()

    def __getitem__(self, key):
        assert key in self.keys
        return self._values[key]
