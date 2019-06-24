import pyparsing as pp


def deco(func):

    def _wrapper(lst, dct={}):
        if isinstance(lst, str):
            return dct[lst]
        elif len(lst) == 1:
            return eval_expr(lst[0], dct)

        if isinstance(lst[0], pp.ParseResults):
            lst[0] = eval_expr(lst[0], dct)
        elif isinstance(lst[0], str):
            lst[0] = dct[lst[0]]

        if isinstance(lst[2], pp.ParseResults):
            lst[2] = eval_expr(lst[2], dct)
        elif isinstance(lst[2], str):
            lst[2] = dct[lst[2]]

        return func(lst)

    return _wrapper


@deco 
def c_mult(lst):
    return lst[0] * lst[2]


@deco 
def c_divide(lst):
    return lst[0] / lst[2]


@deco 
def c_minus(lst):
    return lst[0] - lst[2]


@deco 
def c_add(lst):
    return lst[0] + lst[2]


@deco
def eval_expr(lst, dct={}):
    if lst[1] == '+':
        return c_add(lst, dct)
    elif lst[1] == '-':
        return c_minus(lst, dct)
    elif lst[1] == '*':
        return c_mult(lst, dct)
    elif lst[1] == '/':
        return c_divide(lst, dct)
    else:
        raise Exception
