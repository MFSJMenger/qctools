from qctools.utils import substitute_args_kwargs


def substitute_help_func(dct, *args, **kwargs):
    return substitute_args_kwargs(dct, args, kwargs)


def test_substitute_args_kwargs_single_arg():
    assert substitute_help_func({'name': 0}, 1) == {'name': 1}


def test_substitute_args_kwargs_multiple_arg():
    expected = {'name': "hi", 'hi': None, 'du': 333}
    assert substitute_help_func({'name': 0, 'hi': 2, 'du': 3},
                                "hi", 100, None, 333) == expected


def test_substitute_args_kwargs_single_kwargs():
    expected = {'name': "hi"}
    assert substitute_help_func({'name': 'name'}, 100, None, 333, name="hi") == expected


def test_substitute_args_kwargs_multiple_args_kwargs():
    expected = {'name': "hi", 'du': 333}
    assert substitute_help_func({'name': 'name', 'du': 2}, 100, None, 333, name="hi") == expected
