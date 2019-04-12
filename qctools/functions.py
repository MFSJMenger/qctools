def str_split(string, idx=None, typ=str):
    if idx is None:
        return map(typ, string.split())
    return typ(string.split()[idx])
