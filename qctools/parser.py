from collections import OrderedDict
from .qcreader import QCReader
# configs
from .gaussian_config import gaussian_config

class BaseConfigReader(QCReader):

    _config = OrderedDict()

    def __init__(self, filename, keys, reset=True):

        self._set_events(keys)
        super(BaseConfigReader, self).__init__(filename, reset=reset)
        self.parse

    def _set_events(self, keys):

        self._events = OrderedDict()

        for key in keys:
            if key not in self._config.keys():
                raise Exception("'%s' not in %s keys, please specify event"
                                % (key, str(list(self._config.keys()))))
            self._events[key] = self._config[key]


class GaussianReader(BaseConfigReader):
    _config = gaussian_config
