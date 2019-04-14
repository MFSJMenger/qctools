from collections import OrderedDict
from .eventhandler import EventHandler
# configs
from .gaussian_config import gaussian_config

class BaseEventReader(EventHandler):

    def __init__(self, filename, keys, reset=True):

        self._check_all_events(keys)
        self._keys = keys
        super(BaseEventReader, self).__init__(filename, reset=reset)
        self.parse

    def _check_all_events(self, keys):

        for key in keys:
            if key not in self._events.keys():
                raise Exception("'%s' not in %s keys, please specify event"
                                % (key, str(list(self._config.keys()))))

    @property
    def keys(self):
        return self._keys



class GaussianReader(BaseEventReader):
    _events = gaussian_config
