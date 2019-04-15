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
                     event_type, event_type_kwargs,
                     func=post_process_function,
                     func_args=post_process_function_kwargs,
                     )

e.g. get natoms from gaussian log file::
    
    # Get NAtoms
    NAtoms = Event('NAtoms',
                   'grep', {'keyword': 'NAtoms=',
                            'ilen': 1,
                            'ishift': 0},
                   func=str_split,
                   func_kwargs={'idx': 1, 'typ': int})

    forces = Event('forces',
                   'xgrep', {'keyword': 'Forces (Hartrees/Bohr)',
                            'ilen': 'NAtoms',
                            'ishift': 3},
                   func=map_function,
                   func_kwargs={'func': partial(split_line_and_map, start=2, end=5)},
                   settings={'multi': True, 'reset': False})


Event Types:
~~~~~~~~~~~~

Predefined event types:

'grep'::

    kwargs: 

        keyword (str):
            defines the keyword to grep for

        ilen (int):
            how many lines of the file to return

        ishift (int):
            how many lines starting from the keyword to skip

    returns:
        
        string (str):
            Context of the `ilen` lines
            
'xgrep'::

    kwargs: 

        keyword (str):
            defines the keyword to grep for

        ilen (int):
            how many lines of the file to return

        ishift (int):
            how many lines starting from the keyword to skip

    returns:
        
        list (lst):
            List of the `ilen` lines


