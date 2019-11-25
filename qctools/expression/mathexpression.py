import sys
#
import pyparsing
from .pp_parser import eval_expr
from .pp_grammar import EXPRESSION


class MathExpression(object):
    """Way to handel simple mathematical operations"""

    def __init__(self, in_value, asis=False):

        self.isfunc = False
        self.isexpr = False
        self.isvalue = False

        if asis is True:
            self.isvalue = True
            self._value = in_value


        elif isinstance(in_value, list):
            if callable(in_value[0]):
                self.isfunc = True
                self._func = in_value[0]
                self._args = in_value[1]
            else:
                self.isvalue = True
                self._value = in_value
        elif isinstance(in_value, str):
            self.isexpr = True
            try:
                self._args = EXPRESSION.parseString(in_value, parseAll=True)
            except pyparsing.ParseException:
                print(f"Error Termaination: Parsing of expression '{in_value}' not possible")
                sys.exit()
        else:
            self.isvalue = True
            self._value = in_value

    def eval(self, dct):
        if self.isfunc:
            kwargs = dict((key, value) for key, value in dct.items()
                          if key in self._args)
            return self._func(**kwargs)
        if self.isexpr:
            return eval_expr(self._args, dct=dct)
        if self.isvalue:
            return self._value
