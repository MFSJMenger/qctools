from .fileio import file_reading_iterator_raw


class EventHandler(object):
    """Basic Event Handler to loop over events"""

    _events = dict()

    def __init__(self, reset=True):
        self._reset = reset
        self._values = dict((key, None) for key in self.keys)
        self._ignore_keys = []

    @property
    def filename(self):
        return self._name

    @classmethod
    def add_event(cls, name, event):
        cls._events[name] = event

    @property
    def keys(self):
        return self._events.keys()

    @property
    def perform_events(self):
        self._loop_over_events()

    def _set_passed_object(self):
        """Define an Python object that is handed to all events"""
        return None

    def _trigger_event(self, passed_obj, key):
        event = self._events[key]
        # reset iterator before event call
        if event.reset is True:
            passed_obj = self._set_passed_object()
        self._values[key], ierr = event.trigger(passed_obj, self._values)
        # reset iterator after event call
        if ierr == -1 and self._reset is True:
            passed_obj = self._set_passed_object()
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
        passed_obj = self._set_passed_object()
        for key in self.keys:
            passed_obj, ierr = self._trigger_event(passed_obj, key)
        self._post_process()

    def __getitem__(self, key):
        return self._values[key]


class BaseEventFileReader(EventHandler):
    """Base Class to read information from ASCII text files"""

    _iterator = staticmethod(file_reading_iterator_raw)

    def __init__(self, filename, keys, default_values={}, reset=True):

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

    @property
    def keys(self):
        return self._keys

    @property
    def all_keys(self):
        return self._keys + self._ignore_keys

    def _set_passed_object(self):
        """Define an Python object that is handed to all events"""
        return self._iterator(self._name)

    def _check_all_events(self, keys):

        for key in keys:
            if key not in self._events.keys():
                raise Exception("'%s' not in %s keys, please specify event"
                                % (key, str(list(self._events.keys()))))

def generate_event_class(name, possible_events, BaseClass=BaseEventFileReader):
    return type(name, (BaseClass, ), {'_events': possible_events})
