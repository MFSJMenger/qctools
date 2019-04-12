from collections import OrderedDict
from functools import partial

from .functions import str_split, identity
from .functions import split_line_and_map, map_by_lines 

from .atominfo import atomnumber_to_atomname


def get_scf_done(line):
    line = line.partition("=")[2]
    return float(line.split()[0])


def get_crd(line):
    columns = line.split()
    return [ atomnumber_to_atomname[int(columns[1])] ] + list(map(float, columns[3:6])) 


GaussianConfig = OrderedDict({
        'NAtoms': {
            'grep': {
              'keyword': 'NAtoms=',
              'ilen': 1,
              'ishift': 0,
            },
            'func': partial(str_split, idx=1, typ=int),
            },
       'NBasis': {
           'grep': {
             'keyword': 'NBasis=',
             'ilen': 1,
             'ishift': 0,
           },
            'func': partial(str_split, idx=1, typ=int),
           },
       'escf': {
           'grep': {
             'keyword': 'SCF Done',
             'ilen': 1,
             'ishift': 0,
           },
           'func': get_scf_done,
           },
        'standard_orientation': {
           'grep': {
             'keyword': 'Standard orientation:',
             'ilen': 'NAtoms',
             'ishift': 5,
           },
          'func': partial(map_by_lines, 
                  func=get_crd),
           'multigrep': True,
           'reset': True,
           },
        'input_orientation': {
           'grep': {
             'keyword': 'Input orientation:',
             'ilen': 'NAtoms',
             'ishift': 5,
           },
          'func': partial(map_by_lines, 
                  func=get_crd),
           'multigrep': True,
           'reset': True,
           },
        'forces': {
          'grep': {
            'keyword': 'Forces (Hartrees/Bohr)',
            'ilen': 'NAtoms',
            'ishift': 3,
            },
          'multigrep': True,
          'reset': True,
          'func': partial(map_by_lines, 
              func=partial(split_line_and_map, 
                  start=2, end=5)),
          },
        'termination': {
          'grep': {
            'keyword': 'Normal termination',
            'ilen': 1,
            'ishift': 0,
            },
          'func': identity,
          },
})
