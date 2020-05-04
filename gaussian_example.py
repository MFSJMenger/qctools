from qctools.parser import GaussianReader
from qctools import reset_event, register_event_type
from qctools import Event

def get_natoms(NAtoms=0):
    return NAtoms

NAtoms = Event('NAtoms',
               'grep', {'keyword': 'NAtoms=',
                        'ilen': 1,
                        'ishift': 0},
               func='split',
               func_kwargs={'idx': 1, 'typ': int},
)

forces = Event('forces',
               'xgrep', {'keyword': 'Forces (Hartrees/Bohr)',
                         'ilen': [get_natoms, "NAtoms"],
                         'ishift': 3},
               func='split',
               func_kwargs={'idx': [2, 3, 4], 'typ': [float, float, float], 'bylines': True},
               settings={'multi': False, 'reset': True})



def print_value():

    def prt_val(iterator, value=None, name="Dagmar"):
        return value, 1

    return {"value": int}, ["name"], prt_val


def prt_val(iterator, value=None):
    for line in iterator:
        print(line)
    print("Value is %d " % value)
    return value, 1


#register_event_type("prt_val", ({"value": int}, [], prt_val))
register_event_type("prt_val", print_value)

print5 = Event('print5',
               'prt_val', {'value': "NAtoms", 
                           "name": "Dagmar",
                   },
)

GaussianReader.add_event("NAtoms", NAtoms)
GaussianReader.add_event("forces", forces)
GaussianReader.add_event("print_natoms", print5)

val = GaussianReader("h2o.log", ["print_natoms", "forces"], {"NAtoms": 3})# "standard_orientation", "reset", "normal_termination"], reset=False)

for key in val.keys:
    print("%s = %s" % (key, str(val[key])))

