from functools import partial
# Base Classes
from .events import register_event_type, Event
from .eventhandler import BaseEventFileReader
from .eventhandler import generate_event_class
# Configs
from .gaussian_config import gaussian_config
# from .orca_config import orca_config


def get_gaussian_block(iterator, iblock=0):

    icount = 0
    out = []

    for line in iterator:
        if line.strip() == "":
            icount += 1
            continue
        if icount == iblock:
            out.append(line)

    if out != "":
        return out[1:], 1
    return None, -1


register_event_type("get_gaussian", [{"iblock": int}, [], get_gaussian_block])


get_coordinate_section = Event('coords',
                               'get_gaussian', {'iblock': 2})


# function
generate_filereader = partial(generate_event_class, BaseClass=BaseEventFileReader)
# Gaussian
GaussianReader = generate_filereader('GaussianReader', gaussian_config)
GaussianInputReader = generate_filereader('GaussianInputParser',
                                          {'coords': get_coordinate_section})
# Orca
# OrcaReader = generate_filereader("OrcaReader", orca_config)
