from collections import OrderedDict
from functools import partial

from .events import Event
from .functions import str_split, identity
from .functions import split_line_and_map, map_by_lines

from .atominfo import atomnumber_to_atomname


def get_scf_done(line):
    line = line.partition("=")[2]
    return float(line.split()[0])


def get_crd(line):
    columns = line.split()
    return ([atomnumber_to_atomname[int(columns[1])]]
            + list(map(float, columns[3:6])))


# Get NAtoms
NAtoms = Event('NAtoms',
               'grep', {'keyword': 'NAtoms=',
                        'ilen': 1,
                        'ishift': 0},
               func=str_split,
               func_kwargs={'idx': 1, 'typ': int})
# Get NBasis
NBasis = Event('NBasis',
               'grep', {'keyword': 'NBasis=',
                        'ilen': 1,
                        'ishift': 0},
               func=str_split,
               func_kwargs={'idx': 1, 'typ': int})
# Get Standard Orientation
standard_orientation = Event('standard_orientation',
                             'grep', {'keyword': 'Standard orientation:',
                                      'ilen': 'NAtoms',
                                      'ishift': 5},
                             func=map_by_lines,
                             func_kwargs={'func': get_crd},
                             settings={'multi': True, 'reset': True})
# Get Input Orientation
input_orientation = Event('input_orientation',
                          'grep', {'keyword': 'Input orientation:',
                                   'ilen': 'NAtoms',
                                   'ishift': 5},
                          func=map_by_lines,
                          func_kwargs={'func': get_crd},
                          settings={'multi': True, 'reset': True})

ESCF = Event('ESCF',
             'grep', {'keyword': 'SCF Done',
                      'ilen': 1,
                      'ishift': 0},
             func=get_scf_done)

# normal termination
normal_termination = Event('normal_termination',
                           'grep', {'keyword': 'Normal termination',
                                    'ilen': 1,
                                    'ishift': 0},
                           func=identity)
# Forces
forces = Event('forces',
               'grep', {'keyword': 'Forces (Hartrees/Bohr)',
                        'ilen': 'NAtoms',
                        'ishift': 3},
               func=map_by_lines,
               func_kwargs={'func': partial(split_line_and_map, start=2, end=5)},
               settings={'multi': True, 'reset': False})


_gaussian_events = [
        NAtoms,
        NBasis,
        standard_orientation,
        input_orientation,
        ESCF,
        normal_termination,
        forces,
]


gaussian_config = OrderedDict(dict((event.name, event)
                              for event in _gaussian_events))
