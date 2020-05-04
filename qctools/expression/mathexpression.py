import sys


class MathExpression(object):
    """Way to handel simple mathematical operations"""
    __slots__ = ('eval', '_expr', '_names')

    placeholder = "__MATHEXPR__ANSWER__"

    def __init__(self, expr):

        if isinstance(expr, str):
            expr = self._preprocess_expr(expr)
            expr = compile(expr, "mathexpr", "exec")
            self._expr, self._names = self._check_expr(expr)
            self.eval = self._eval
        elif isinstance(expr, int):
            # default set by value
            self._expr = expr
            self.eval = self._return_value
        elif hasattr(expr, '__call__'):
            self.eval = expr
        else:
            raise ValueError("Expression can only be int or a python expression!")

    def _preprocess_expr(self, expr):
        lines = [line for line in expr.splitlines() if line.strip() != ""]
        lines[-1] = f"{self.placeholder} = {lines[-1]}"
        out = "\n".join(lines)
        return out

    def _check_expr(self, expr):
        names = tuple(name for name in expr.co_names if name != self.placeholder)
        dct = {name: 1 for name in names}
        exec(expr, dct)
        # get rid of functions etc.
        names = tuple(name for name in names if not hasattr(dct[name], '__call__'))
        if not isinstance(dct[self.placeholder], int):
            raise ValueError("MathExpression has to return integer!")
        return expr, names

    def _return_value(self, dct=None):
        return self._expr

    def _eval(self, dct=None):
        """Compute result"""
        if dct is None:
            dct = {}
        out = {name: dct[name] for name in self._names}
        exec(self._expr, out)
        return out[self.placeholder]
