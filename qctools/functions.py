def str_split(string, idx=0, typ=str):
    return typ(string.split()[idx])


def str_split_multi(string, idx=None, typ=None):
    if idx is None:
        idx = []
    if typ is None:
        typ = []
    col = string.split()
    return [typ[j](col[i]) for j, i in enumerate(idx)]


def identity(obj):
    return obj


def split_line_and_map(line, func=float, start=0, end=0):
    return list(map(float, line.split()[start:end]))


def map_function_by_lines(txt, func=split_line_and_map):
    return list(map(func, txt.splitlines()))


def map_function(iterator, func=split_line_and_map):
    return list(map(func, iterator))


def only_first_element(iterator, func=split_line_and_map):
    return func(iterator[0])
