from .converter import Converter


energy_converter = Converter.from_dct('energy', 'au', {
    'au': (1.0, 'direct'),
    'eV': (27.211399, 'direct'),
    'nm': (1239.84193/27.211399, 'inverse'),
    'fs': (4.13567/27.211399, 'inverse'),
    'kjmol': (2625.5002, 'direct'),
    'kcalmol': (627.509608, 'direct'),
    'cminv': (219474.63068, 'direct'),
    'cm-1': (219474.63068, 'direct'),
})


length_converter = Converter.from_dct('length', 'ang', {
        'au': (1.88971616463207, 'direct'),
        'ang':  (1.0, 'direct'),
        'nm':  (0.1, 'direct'),
        'bohr':  (1.88971616463207, 'direct'),
        'pm':  (100, 'direct'),
})


force_converter = Converter.from_dct('force', 'au', {
        'au/ang':  (1.0/0.5291772105638411, 'direct'),
        'au/nm':  (1.0/0.05291772105638411, 'direct'),
        'kjmol/nm':  (2625.5002/0.05291772105638411, 'direct'),
        'kjmol/ang':  (2625.5002/0.5291772105638411, 'direct'),
        'kcal/nm':  (627.509608/0.05291772105638411, 'direct'),
        'kcal/ang':  (627.509608/0.5291772105638411, 'direct'),
})


time_converter = Converter.from_dct('time', 'fs', {
        'fs': (1.0, 'direct'),
        'au': (1.0/0.02418884254, 'direct'),
        'sec': (1.0*10**(-15), 'direct'),
        's': (1.0*10**(-15), 'direct'),
        'ms': (1.0*10**(-12), 'direct'),
        'mus': (1.0*10**(-9), 'direct'),
        'ns': (1.0*10**(-6), 'direct'),
        'ps': (1.0*10**(-3), 'direct'),
        'min': ((1.0/60.0)*(10**(-15)), 'direct'),
        'h': ((1.0/(3600.0))*10**(-15), 'direct'),
        'day': ((1.0/86400)*10**(-15), 'direct'),
        'week': ((1.0/604800.0)*10**(-15), 'direct'),
})
