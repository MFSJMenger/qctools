from __future__ import print_function, division

from collections import namedtuple
from copy import deepcopy


Conversion = namedtuple("Conversion", ["factor", "relation"])


class UnknownUnitError(Exception):
    pass


class ConversionContainer(object):

    named_tuple = Conversion

    def __init__(self, name, ref, dct):
        self.name = name
        self.ref = ref
        self.values = self._parse_dct(dct)

        if self.ref not in self:
            self[self.ref] = self.named_tuple(factor=1.0, relation='direct')

    def keys(self):
        return self.values.keys()

    def items(self):
        return self.values.items()

    def add_entry(self, name, fac, rel):
        self.values[name] = Conversion(factor=fac, relation=rel)

    def __str__(self):
        return ("\nConversionContainer('%s')\n" % (self.name)
                + "----------------------------------------------------\n"
                + "".join(["Unit '%8s': %25s\n" % (key, value)
                           for key, value in self.items()])
                + "----------------------------------------------------\n")

    def __iter__(self):
        self._lkeys = list(self.keys())
        self._count = 0
        self._nmax = len(self._lkeys)
        return self

    def __next__(self):
        if self._count < self._nmax:
            result = self._lkeys[self._count]
            self._count += 1
            return result
        raise StopIteration

    def __getitem__(self, key):
        return_value = self.values.get(key, None)
        if return_value is None:
            raise UnknownUnitError(
                    "Unknown Unit '%s' for type '%s'" % (key, self.name))
        return return_value

    def __setitem__(self, key, value):
        if not isinstance(value, self.named_tuple):
            if type(value) in [tuple, list]:
                self.values[key] = self.named_tuple(
                        factor=value[0],
                        relation=value[1])
            else:
                raise TypeError('entries need to be either ')
        else:
            self.values[key] = value

    def _parse_dct(self, in_dct):
        dct = deepcopy(in_dct)
        if 'reference' in dct:
            del dct['reference']
        for key, value in dct.items():
            if not isinstance(value, self.named_tuple):
                if type(value) in [tuple, list]:
                    dct[key] = self.named_tuple(
                            factor=value[0],
                            relation=value[1])
                else:
                    raise TypeError('entries need to be either ')
        return dct
