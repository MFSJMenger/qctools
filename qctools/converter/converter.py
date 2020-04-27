from __future__ import print_function, division

from collections.abc import MutableMapping
from functools import partial

from .container import ConversionContainer

# relations:
#
# direct direct:
# val = l2/l1 * x

# direct inverse
# val = (l1*l2)/x

# inverse direct
# val = (l1 * l2)/x

# inverse inverse
# val = (l2/l1) * x


class Converter(MutableMapping):

    def __init__(self, container):
        self.container = container

    def __str__(self):
        return str(self.container)

    def __getitem__(self, key):
        return self.container[key]

    def __iter__(self):
        return iter(self.container)

    def __delitem__(self, key):
        del self.container[key]

    def __setitem__(self, key, value):
        self.container[key] = value

    def __len__(self):
        return len(self.container)

    @property
    def ref(self):
        return self.container.ref

    @property
    def name(self):
        return self.container.name

    @classmethod
    def from_dct(cls, name, ref, dct):
        container = ConversionContainer(name, ref, dct)
        return cls(container)

    def _generate_converter_expression(self, tin, tout):
        if not all(typ in self.container for typ in (tin, tout)):
            raise ValueError(f"cannot convert from '{tin}' to '{tout}'")

        input_conversion = self.container[tin]
        output_conversion = self.container[tout]

        if input_conversion.relation == output_conversion.relation:
            factor = output_conversion.factor/input_conversion.factor
            string = f"""
def _call(self, x):
    return {factor} * x
                """
        else:
            factor = output_conversion.factor*input_conversion.factor
            string = f"""
def _call(self, x):
    return {factor} / x
"""

        def _repr(xself):
            return f"<ConverterFunction: '{self.name}' from  '{tin}' to '{tout}'>"

        def _str(xself):
            return f"<ConverterFunction: '{self.name}' from  '{tin}' to '{tout}'>"

        classdct = {}

        exec(string, classdct)

        ConverterFunction = type('ConverterFunction', (), {'__slots__': (),
                                                           '__repr__': _repr,
                                                           '__str__': _str,
                                                           '__call__': classdct['_call']})

        return ConverterFunction()

    def convert(self, value, tin, tout):
        return self._generate_converter_expression(tin, tout)(value)

    def get_converter(self, tin, tout):
        """ return converter function from tin to tout """
        return self._generate_converter_expression(tin, tout)

    def add_entry(self, name, factor, relation, other=None):
        if other is None:
            self.container[name] = (factor, relation)
        else:
            intermediate = self.container[other]
            if intermediate.relation == 'direct' and relation == 'direct':
                self.container[name] = (factor*intermediate.factor, 'direct')
            elif intermediate.relation == 'inverse' and relation == 'inverse':
                self.container[name] = (factor*intermediate.factor, 'direct')
            elif intermediate.relation == 'inverse' or relation == 'inverse':
                self.container[name] = (factor*intermediate.factor, 'inverse')
            else:
                raise ValueError("relation can only be in ['inverse', 'direct']")
