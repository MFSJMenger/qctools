=======
qctools
=======




.. image:: https://pyup.io/repos/github/MFSJMenger/qctools/shield.svg
     :target: https://pyup.io/repos/github/MFSJMenger/qctools/
     :alt: Updates



Python tools for quantum chemists



Features
--------

Define Event Handlers for simple parsing of Quantum Chemistry Source Code

Example:

Read natoms from Gaussian Output file:


1. Step: Define the Event
~~~~~~~~~~~~~~~~~~~~~~~~~

>>> NAtoms = Event('NAtoms',
...                'grep', {'keyword': 'NAtoms=',
...                         'ilen': 1,
...                         'ishift': 0},
...                func=str_split, idx=1, typ=int)
...                func_kwargs={'idx': 1, 'typ': int})

>>> forces = Event('forces',
...                'xgrep', {'keyword': 'Forces (Hartrees/Bohr)',
...                          'ilen': 'NAtoms',
...                          'ishift': 3},
...                func='split',
...                func_kwargs={'idx': [2, 3, 4], 'typ': [float, float, float], 'bylines': True},
...                settings={'multi': False, 'reset': False})

2. Step: Add the new event to an existing Event Handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

>>> GaussianReader.add_event("NAtoms", NAtoms)
>>> GaussianReader.add_event("forces", forces)

3. Step: Use the Event Handler to parse an file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

>>> gauout = GaussianReader("h2o.log", ["NAtoms", "forces"])
>>> gauout["NAtoms"] 
3

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
