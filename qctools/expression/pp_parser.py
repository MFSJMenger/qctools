import pyparsing as pp


def get_partial_expression(entry, dct):
    if isinstance(entry, pp.ParseResults):
        return eval_expr(entry, dct)

    if isinstance(entry, str):
        return dct[entry]

    if isinstance(entry, (int, float, complex)):
        return entry


def handle_expression_cases(func):

    def _wrapper(lst, dct=None):
        """Handle parsing!"""
        if dct is None:
            dct = {}
        if isinstance(lst, str):
            return dct[lst]

        if isinstance(lst, (int, float, complex)):
            return lst

        lst[0] = get_partial_expression(lst[0], dct)
        try:
            lst[2]
        except IndexError:
            return lst[0]

        lst[2] = get_partial_expression(lst[2], dct)

        return func(lst)
    return _wrapper


@handle_expression_cases
def c_mult(lst):
    return lst[0] * lst[2]


@handle_expression_cases
def c_divide(lst):
    return lst[0] / lst[2]


@handle_expression_cases
def c_minus(lst):
    return lst[0] - lst[2]


@handle_expression_cases
def c_add(lst):
    return lst[0] + lst[2]


@handle_expression_cases
def eval_expr(lst, dct=None):
    cases = {
        '+': c_add,
        '-': c_minus,
        '*': c_mult,
        '/': c_divide,
    }

    case = cases.get(lst[1], None)
    if case is None:
        raise ValueError("Operator {lst[1]} unknown, use [{', '.join(cases.keys())}]")
    return case(lst, dict)
