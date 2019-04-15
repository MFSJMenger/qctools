=====
Usage
=====

To use qctools in a project::

    import qctools

Use predefined handlers to read Quantum Chemistry Software:

Gaussian
~~~~~~~~

Read Forces from Gaussian logfile::

    from qctools import GaussianReader

    output = GaussianReader(filename, ["NAtoms", "forces"])

    forces = output["forces"]


Event Handler:
~~~~~~~~~~~~~~

Create own event handler for file reading::
                     
    from qctools import BaseEventReader

    class MyReader(BaseEventReader):
        _events = myevents

    file = MyReader(filename, [event1, event2, ...])

myevent needs to be a dictionary of possible events


Create own events::

    from qctools import Event

    NewEvent = Event('newevent', 
                     event_type, event_kwargs,
                     post_process_function,
                     post_process_function_kwargs,
                     )

e.g. get natoms from gaussian log file::
    
    # Get NAtoms
    NAtoms = Event('NAtoms',
                   'grep', {'keyword': 'NAtoms=',
                            'ilen': 1,
                            'ishift': 0},
                   func=str_split,
                   func_kwargs={'idx': 1, 'typ': int})


predefined currently only `grep` is defined as event_type


