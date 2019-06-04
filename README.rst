=======
qctools
=======


.. image:: https://pyup.io/repos/github/MFSJMenger/qctools/shield.svg
     :target: https://pyup.io/repos/github/MFSJMenger/qctools/
     :alt: Updates



Python tools for quantum chemists


Features
--------

Define Event Handlers for straightforward parsing of Quantum Chemistry Output

Example:

Read natoms from Gaussian Output file:

1. Step: Define the Event
~~~~~~~~~~~~~~~~~~~~~~~~~

The number of atoms are written typically in the following way
in the Gaussian output file:

.Gaussian Log File 

::

 ...
 NAtoms=    3 NActive=    3 NUniq=    2 SFac= 2.25D+00 NAtFMM=   50 NAOKFM=F Big=F
 One-electron integrals computed using PRISM.
 ...


the event should do the following:

1. It should loop over all lines of the file, till it findes the 
   Keyword `NAtoms=`
2. It should return that line and extract the 2. element of that 
   line as a string

The corresponding event looks like:

>>> NAtoms = Event('NAtoms',
...                'grep', {'keyword': 'NAtoms=',
...                         'ilen': 1,
...                         'ishift': 0},
...                func='split',
...                func_kwargs={'idx': 1, 'typ': int}
...)

The first entry is the name of the event, and can be any name.
The second entry is the type of the event, in this case just grep.
The third entry gives the parameter to the corresponding event function:
[we want to search for 'NAtoms=' and return a single line (ilen=1) 
not shifted (ishift=0) from the keyword.]

Afterwards the line is given to a postprocessing function ('split') which
splits the line by spaces and returns the element[1] of the line as an integer.
Remember, this is Python/C notation to element[1] is the second element in the list.


For the Forces the event should look the following:

::

   -------------------------------------------------------------------
   Center     Atomic                   Forces (Hartrees/Bohr)
   Number     Number              X              Y              Z
   -------------------------------------------------------------------
        1        8           0.000000000    0.000000000    0.005485119
        2        1           0.000000000    0.017353174   -0.002742559
        3        1           0.000000000   -0.017353174   -0.002742559
   ------------------------------------------------------------------


>>> forces = Event('forces',
...                'xgrep', {'keyword': 'Forces (Hartrees/Bohr)',
...                          'ilen': 'NAtoms',
...                          'ishift': 3},
...                func='split',
...                func_kwargs={'idx': [2, 3, 4], 'typ': [float, float, float]},
...                settings={'multi': False},
...)

2. Step: Add the new event to an existing Event Handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

>>> GaussianReader.add_event("NAtoms", NAtoms)
>>> GaussianReader.add_event("forces", forces)

3. Step: Use the Event Handler to parse an file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

>>> gauout = GaussianReader("h2o.log", ["NAtoms", "forces"])
>>> gauout["NAtoms"] 
3
>>> gauout["forces"]
[[0.0,0.0,0.005485119],[0.0,0.017353174,-0.002742559],[0.0,-0.017353174,-0.002742559]]

=======
Credits
=======

Development Lead
----------------

* Maximilian Menger

Contributors
------------

Why not be the first?

Thanks to:
----------

* Boris Maryasin
* Gustavo Cardenas


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
