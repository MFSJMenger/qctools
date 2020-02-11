from __future__ import print_function, division

from collections import namedtuple
from collections.abc import MutableMapping
#
from copy import deepcopy


Conversion = namedtuple("Conversion", ["factor", "relation"])


class ConversionContainer(MutableMapping):

    def __init__(self, name, ref, dct):
        self.name = name
        self.ref = ref
        self._values = self._parse_dct(dct)

        if self.ref not in self:
            self[self.ref] = (1.0, 'direct')

    def add_entry(self, key, fac, rel):
        self[key] = (fac, rel)

    def __len__(self):
        return len(self._values)

    def __getitem__(self, key):
        return self._values[key]

    def __delitem__(self, key):
        del self._values[key]

    def __setitem__(self, key, value):
        if isinstance(value, Conversion):
            self._values[key] = value
            return
        if not isinstance(value, (tuple, list)):
            raise ValueError('only tuple or list of (factor, relation) pairs accepted')
        self._values[key] = Conversion(factor=value[0], relation=value[1])

    def __str__(self):
        items = "\n".join(f"Unit '{key}': {value}" for key, value in self.items())
        return f""" ConversionContainer('{self.name}')
----------------------------------------------------
{items}
----------------------------------------------------
"""

    def __iter__(self):
        return iter(self._values)

    def _parse_dct(self, in_dct):
        dct = deepcopy(in_dct)
        if 'reference' in dct:
            del dct['reference']
        for key, value in dct.items():
            if not isinstance(value, Conversion):
                if isinstance(value, (tuple, list)):
                    dct[key] = Conversion(factor=value[0], relation=value[1])
                else:
                    raise TypeError('entries need to be either Conversion or tuple/list')
            if dct[key].relation not in ('direct', 'inverse'):
                raise ValueError("Only 'direct' and 'inverse' relations implemented")
        return dct
