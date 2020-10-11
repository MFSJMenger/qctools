import pytest
import random

from qctools.converter import Converter


@pytest.fixture
def example_converter():
    ''' Returns an example converter '''
    converter = Converter.from_dct('example', 'ref', {
        'ref': (1, 'direct'),
        'eV': (27, 'direct'),
        'cm': (27, 'inverse'),
    })
    return converter


@pytest.fixture
def random_value():
    ''' Returns an random value'''
    return random.uniform(0.00001, 10000000.0)


def test_conversion_inverse(example_converter, random_value):
    '''test conversion for inverse type'''
    fac = example_converter.container['cm'].factor
    assert (round(fac/random_value, 8)
            == round(example_converter.convert(random_value, 'ref', 'cm'), 8))


def test_conversion_direct(example_converter, random_value):
    '''test conversion for inverse direct'''
    fac = example_converter.container['eV'].factor
    assert (round(fac*random_value, 8)
            == round(example_converter.convert(random_value, 'ref', 'eV'), 8))


def test_add_entry_direct(example_converter, random_value):
    factor = example_converter.container['eV'].factor
    example_converter.add_entry('ex1', factor, 'direct')
    assert round(random_value, 7) == round(example_converter.convert(
                                              random_value, 'ex1', 'eV'), 7)


def test_add_entry_direct_via_second_direct_element(example_converter):
    example_converter.add_entry('ex2', 1.0, 'direct', other='eV')
    for i in range(1, 100):
        res1 = example_converter.convert(i, 'ref', 'ex2')
        res2 = example_converter.convert(i, 'ref', 'eV')
        assert round(res1, 6) == round(res2, 6)


def test_add_entry_direct_via_second_inverse_element(example_converter):
    fac = 3.0
    example_converter.add_entry('ex3', fac, 'direct', other='cm')
    for i in range(1, 100):
        res1 = example_converter.convert(i, 'eV', 'ex3')
        res2 = example_converter.convert(i, 'eV', 'cm')*fac
        assert round(res1, 8) == round(res2, 8)


def test_add_entry_inverse_via_second_inverse_element(example_converter):
    example_converter.add_entry('ex4', 1.0/27.0, 'inverse', other='cm')
    for i in range(1, 100):
        res1 = example_converter.convert(i, 'ref', 'ex4')
        res2 = example_converter.convert(i, 'ref', 'ref')
        assert round(res1, 8) == round(res2, 8)


def test_add_entry_inverse(example_converter):
    example_converter.add_entry('ex5', 27, 'inverse')
    for i in range(1, 100):
        result = example_converter.convert(i, 'ex5', 'cm')
        assert round(i, 8) == round(result, 8)


def test_add_entry(example_converter):
    example_converter.add_entry('en', 1, 'direct')
    assert 'en' in example_converter


def test_add_entry_fail(example_converter):
    with pytest.raises(Exception):
        assert 'en' in example_converter
