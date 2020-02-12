from qctools.parser import GaussianReader
from qctools import reset_event
from qctools import Event

NAtoms = Event('NAtoms',
               'grep', {'keyword': 'NAtoms=',
                        'ilen': 1,
                        'ishift': 0},
               func='split',
               func_kwargs={'idx': 1, 'typ': int})

forces = Event('forces',
               'xgrep', {'keyword': 'Forces (Hartrees/Bohr)',
                         'ilen': 'NAtoms',
                         'ishift': 3},
               func='split',
               func_kwargs={'idx': [2, 3, 4], 'typ': [float, float, float], 'bylines': True},
               settings={'multi': False, 'reset': False})

GaussianReader.add_event("NAtoms", NAtoms)
GaussianReader.add_event("forces", forces)
GaussianReader.add_event("reset", reset_event)

val = GaussianReader("h2o.log", ["NAtoms", "forces"])# "standard_orientation", "reset", "normal_termination"], reset=False)

for key in val.keys:
    print("%s = %s" % (key, str(val[key])))

