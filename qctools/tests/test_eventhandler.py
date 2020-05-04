import pytest

from ..eventhandler import EventHandler
from ..events import Event, register_event_type


@pytest.fixture
def example_eventhandler_none():

    class ExampleEventHandlerNone(EventHandler):
        _events = {}

        def __init__(self, keys, reset=True):
            self._reset = reset
            self._values = dict((key, None) for key in keys)
            self._ignore_keys = []

        def _initialize_passed_object(self):
            """Define an Python object that is handed to all events"""
            class Value(object):

                def __init__(self, val):
                    self._val = val

                @property
                def val(self):
                    self._val += 1
                    return self._val

            return Value(1)

    return ExampleEventHandlerNone


@pytest.fixture
def register_print():
    def fprint(stuff, *args, **kwargs):
        return stuff.val, 1
    register_event_type('print', [{}, [], fprint])
    return None


@pytest.fixture
def print_event(register_print):
    return Event('Print', 'print', {})


def test_register_event(register_print):
    """check that register of an event works"""
    pass


def test_example(example_eventhandler_none, print_event):
    example_eventhandler_none._events['print'] = print_event
    example_eventhandler_none._events['print2'] = print_event
    handle = example_eventhandler_none(['print', 'print2'])
    handle.perform_events
    #
    assert 'print' in handle.keys()
    assert handle['print'] == 2
    #
    assert 'print2' in handle.keys()
    assert handle['print2'] == 3
    assert handle.get('print3') == None
