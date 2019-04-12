

def str_split(string, idx=0, typ=str):
    return typ(string.split()[idx])


def identity(obj):
    return obj


def split_line_and_map(line, func=float, start=0, end=0):
    return list(map(float, line.split()[start:end]))


def map_by_lines(txt, func=split_line_and_map):
    return list(map(func, txt.splitlines()))
