from __future__ import print_function, division

from functools import partial

from .container import ConversionContainer
from .decorators import with_repr


def _c_direct(val, conversion, to=True):
    """val: float, value that is to be converted
       conversion: float, conversion factor

       return:
           float, converted value

    """
    if to is True:
        return val*conversion
    else:
        return val*(1.0/conversion)


def _c_inverse(val, conversion):
    """val: float, value that is to be converted
       conversion: float, conversion factor

       return:
           float, converted value
    """
    return conversion/val


def _convert_to_reference(tin, value):
    if tin.relation == 'direct':
        return _c_direct(value, tin.factor, to=False)
    elif tin.relation == 'inverse':
        return _c_inverse(value, tin.factor)
    else:
        return Exception("relation can only be 'direct' or 'inverse'!")


def _convert_from_reference(tout, value):
    if tout.relation == 'direct':
        return _c_direct(value, tout.factor, to=True)
    elif tout.relation == 'inverse':
        return _c_inverse(value, tout.factor)
    else:
        return Exception("relation can only be 'direct' or 'inverse'!")


class Converter(object):

    def __init__(self, container):
        self._container = container

    def __str__(self):
        return str(self.container)

    def __getitem__(self, value):
        return self._container[value]

    def __iter__(self):
        return iter(self._container)

    @property
    def ref(self):
        return self._container.ref

    @property
    def name(self):
        return self._container.name

    @property
    def container(self):
        return self._container

    @classmethod
    def from_dct(cls, name, ref, dct):
        container = ConversionContainer(name, ref, dct)
        return cls(container)

    def convert(self, value, tin, tout):
        return self._converter_compose(tin, tout)(value)

    def get_converter(self, tin, tout):
        """ return converter function from tin to tout """
        return self._converter_compose(tin, tout)

    def add_entry(self, name, factor, relation, other=None):
        if other is None:
            self._container[name] = (factor, relation)
        else:
            intermediate = self._container[other]
            if intermediate.relation == 'direct' and relation == 'direct':
                print('we are here!, indirect, indirect')
                self._container[name] = (factor*intermediate.factor, 'direct')
            elif intermediate.relation == 'inverse' and relation == 'inverse':
                print('we are here!, indirect, indirect')
                self._container[name] = (factor*intermediate.factor, 'direct')
            elif intermediate.relation == 'inverse' or relation == 'inverse':
                self._container[name] = (factor*intermediate.factor, 'inverse')
            else:
                raise Exception(
                        "relation can only be in ['inverse', 'direct']")

    def _converter_compose(self, tin, tout):
        """ compose the function to form the final converter function """

        funcIn = partial(_convert_to_reference, self[tin])
        funcOut = partial(_convert_from_reference, self[tout])

        @with_repr(lambda x: "<ConverterFunction: '%s'  from  '%s' to '%s'>"
                             % (self.name, tin, tout))
        def _inner_func(data, in_func=funcIn, out_func=funcOut):
            return out_func(in_func(data))

        return _inner_func
