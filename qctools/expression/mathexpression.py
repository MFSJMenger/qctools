from .pp_parser import eval_expr
from .pp_grammar import expression


class MathExpression(object):

    def __init__(self, in_value, asis=False):

        self.isfunc = False
        self.isexpr = False
        self.isvalue = False

        if asis is True:
            self.isvalue = True
            self._value = in_value

        elif isinstance(in_value, (list, tuple)):

            if callable(in_value[0]):
                self.isfunc = True
                self._func = in_value[0]
                self._args = in_value[1]
            else:
                self.isvalue = True
                self._value = in_value

        elif isinstance(in_value, str):
            self.isexpr = True
            self._args = expression.parseString(in_value)
        else:
            self.isvalue = True
            self._value = in_value

    def eval(self, dct={}):
        """Compute result"""
        if self.isfunc is True:
            kwargs = dict((key, value) for key, value in dct.items()
                          if key in self._args)
            return self._func(**kwargs)

        if self.isexpr is True:
            return eval_expr(self._args, dct=dct)

        if self.isvalue is True:
            return self._value
        raise Exception

