import sys
from functools import partial
#
import pyparsing
from .pp_parser import eval_expr
from .pp_grammar import EXPRESSION


class MathExpression(object):
    """Way to handel simple mathematical operations"""
    __slots__ = ('eval', '_value')

    def __init__(self, in_value, asis=False):

        if isinstance(in_value, (list, tuple)):
            if callable(in_value[0]):
                self.eval = partial(self._feval, func=in_value[0], args=in_value[1])
                return

        elif isinstance(in_value, str):
            try:
                self._value = EXPRESSION.parseString(in_value, parseAll=True)
            except pyparsing.ParseException:
                print(f"Error Termaination: Parsing of expression '{in_value}' not possible")
                sys.exit()
            self.eval = self._eval
            return
        # default set by value
        self._value = in_value
        self.eval = self._return_value

    def _feval(self, dct={}, func=None, args=None):
        kwargs = dict((key, value) for key, value in dct.items()
                      if key in args)
        return func(**kwargs)

    def _return_value(self, dct={}):
        return self._value

    def _eval(self, dct={}):
        """Compute result"""
        return eval_expr(self._value, dct=dct)
