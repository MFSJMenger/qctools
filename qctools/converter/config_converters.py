from .converter import Converter


energy_converter = Converter.from_dct('energy', 'au', {
    'au': (1.0, 'direct'),
    'eV': (27.211399, 'direct'),
    'nm': (1239.84193/27.211399, 'inverse'),
    'fs': (4.13567/27.211399, 'inverse'),
    'kjmol': (2625.5002, 'direct'),
    'kcalmol': (627.509608, 'direct'),
})


length_converter = Converter.from_dct('length', 'ang', {
        'ang':  (1.0, 'direct'),
        'nm':  (10.0, 'direct'),
        'bohr':  (1.88971616463207, 'direct'),
        'pm':  (0.01, 'direct'),
})


force_converter = Converter.from_dct('force', 'au', {
        'au/ang':  (1.0/1.88971616463207, 'direct'),
        'au/nm':  (1.0/18.8971616463207, 'direct'),
        'kjmol/nm':  (2625.5002/18.8971616463207, 'direct'),
})


time_converter = Converter.from_dct('time', 'fs', {
        'sec': (1.0/(10**(15)), 'direct'),
        's': (1.0/(10**(15)), 'direct'),
        'ms': (1.0/(10**(12)), 'direct'),
        'mus': (1.0/(10**(9)), 'direct'),
        'ns': (1.0/(10**(6)), 'direct'),
        'ps': (1.0/(10**(3)), 'direct'),
        'min': (1.0/(60*10**(15)), 'direct'),
        'h': (1.0/(60*60*10**(15)), 'direct'),
        'day': (1.0/(24*60*60*10**(15)), 'direct'),
        'week': (1.0/(7*24*60*60*10**(15)), 'direct'),
})
