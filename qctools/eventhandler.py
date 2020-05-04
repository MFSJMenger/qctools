from collections.abc import Mapping
#
from .fileio import file_reading_iterator_raw
# from .cppgrep import Iterator
from .events import _CoreEvent
from .events import JoinedEvent


class EventHandler(Mapping):
    """Basic Event Handler to loop over events"""

    _events = dict()

    def __init__(self, reset=True):
        self._reset = reset
        self._values = dict((key, None) for key in self.keys())
        self._ignore_keys = []

    def _initialize_passed_object(self):
        """Define an Python object that is handed to all events"""
        return None

    @classmethod
    def add_event(cls, name, event):
        """register an event to an event handler"""
        if isinstance(event, _CoreEvent):
            cls._events[name] = event
        else:
            raise TypeError("Added event '%s' needs to be an event!" % name)

    # Implement Mappings
    def __getitem__(self, key):
        """Return result values"""
        return self._values.get(key, None)

    def __iter__(self):
        """Iter over results"""
        return iter(self._values)

    def __len__(self):
        """give the length of results"""
        return len(self._values)

    def event_keys(self):
        return self._events.keys()

    @property
    def perform_events(self):
        self._loop_over_events()

    def _unfold_joined(self, dct, key):
        """Unfold joined events!"""
        for key, value in dct[key].items():
            if key not in dct:
                if isinstance(value, list):
                    if len(value) == 1:
                        value = value[0]
                dct[key] = value
                self._ignore_keys.append(key)

    def _trigger_event(self, passed_obj, key):
        """Triger a specific event and do error handling"""
        event = self._events[key]
        # reset iterator before event call
        if event.reset is True:
            passed_obj = self._initialize_passed_object()
        self._values[key], ierr = event.trigger(passed_obj, self._values)
        if isinstance(event, JoinedEvent):
            self._unfold_joined(self._values, key)
        # reset iterator after event call
        if ierr == -1 and self._reset is True:
            passed_obj = self._initialize_passed_object()
        return passed_obj, ierr

    def _post_process(self):
        """Post process the data in the event"""
        # post process data
        for key in self._values:
            if key in self._ignore_keys:
                continue
            event = self._events[key]
            event.post_process(self._values[key])
        # delete keys that are not needed
        for key in self._values:
            if key in self._ignore_keys:
                continue
            if event.delete is True:
                del self._values[key]

    def _loop_over_events(self):
        """Main event loop"""
        passed_obj = self._initialize_passed_object()
        for key in self.keys():
            passed_obj, ierr = self._trigger_event(passed_obj, key)
        self._post_process()


class BaseEventFileReader(EventHandler):
    """Base Class to read information from ASCII text files"""

    _iterator = staticmethod(file_reading_iterator_raw)

    def __init__(self, filename, keys, default_values=None, reset=True):
        """Base Event File Reader"""

        if default_values is None:
            default_values = {}
        self._name = filename
        self._check_all_events(keys)
        self._keys = keys
        super(BaseEventFileReader, self).__init__(reset=reset)
        for key in default_values:
            self._ignore_keys.append(key)
            self._values[key] = default_values[key]
        self.perform_events

    @property
    def filename(self):
        return self._name

    def keys(self):
        return self._keys

    @property
    def all_keys(self):
        return self._keys + self._ignore_keys

    def _initialize_passed_object(self):
        """Define an Python object that is handed to all events"""
        return self._iterator(self._name)

    def _check_all_events(self, keys):

        for key in keys:
            if key not in self._events.keys():
                raise Exception("'%s' not in %s keys, please specify event"
                                % (key, str(list(self._events.keys()))))


# class EventFileReader(BaseEventFileReader):
#
#    def _initialize_passed_object(self):
#        """Define an Python object that is handed to all events"""
#        return Iterator(self._name)


def generate_event_class(name, possible_events, BaseClass=BaseEventFileReader):
    return type(name, (BaseClass, ), {'_events': possible_events})
