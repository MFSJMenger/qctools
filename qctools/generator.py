from copy import deepcopy
from collections import namedtuple
#
from .colt.generator import GeneratorBase
from .colt import parser as LineParser
#
from .events import Event
from .parser import generate_filereader as _generate_filereader


class EventDict(dict):
    pass


class Grep:

    __slots__ = ('name', 'keyword', 'ilen', 'ishift')
    seperator = '::'

    def __init__(self, string):

        if not isinstance(string, str):
            raise ValueError('Grep can only be called using strings!')

        self.keyword, self.ilen, self.ishift = self._parse_string(string)
        if isinstance(self.ilen, str) or self.ilen > 1:
            self.name = 'xgrep'
        else:
            self.name = 'grep'

    def _parse_string(self, string):
        # defaults
        ilen = 1
        ishift = 0
        #
        cols = [col.strip() for col in string.split(self.seperator)]
        ncols = len(cols)
        if ncols == 0:
            raise Exception('at least keyword needs to be set!')

        keyword = cols[0]

        if ncols > 1:
            try:
                ilen = int(cols[1])
            except ValueError:
                ilen = cols[1]

        if ncols > 2:
            try:
                ishift = int(cols[2])
            except ValueError:
                ishift = cols[2]
        return keyword, ilen, ishift


class Split:

    __slots__ = ('idx', 'typ', 'bylines')

    seperator = '::'

    _func_types = {
            'int': int,
            'float': float,
            'str': str,
            }

    def __init__(self, string):

        self.idx, self.typ = self._parse_string(string)

    def _parse_string(self, string):
        cols = [col.strip() for col in string.split(self.seperator)]
        if len(cols) != 2:
            raise ValueError('Split needs to be define as \n split = idx :: typ\n')

        idx = LineParser.ilist_parser(cols[0])
        types = [self._func_types[entry] for entry in LineParser.list_parser(cols[1])]
        if len(idx) == 1:
            idx = idx[0]
        if len(types) == 1:
            if isinstance(idx, list):
                types = [types[0] for _ in idx]
            else:
                types = types[0]

        return idx, types


class Settings:

    __slots__ = ('value', )

    seperator = '::'

    def __init__(self, value):
        self.value = self._parse_string(value)

    def _parse_string(self, string):
        '''settings = mulit :: reset :: delete'''
        dct = deepcopy(Event.default_settings)
        if self.seperator not in string:
            dct.update(self._string_to_dict(string))
            return dct
        cols = [col.strip() for col in string.split(self.seperator)]
        ncols = len(cols)
        if ncols == 0:
            return dct
        if ncols >= 1:
            dct['multi'] = LineParser.bool_parser(cols[0])
        if ncols >= 2:
            dct['reset'] = LineParser.bool_parser(cols[1])
        if ncols >= 3:
            dct['delete'] = LineParser.bool_parser(cols[2])
        return dct

    def _string_to_dict(self, string):
        dct = {}
        for key_value in  LineParser.list_parser(string):
            key, value = tuple(key_value.split('='))
            dct[key] = LineParser.bool_parser(value)
        return dct


class EventGenerator(GeneratorBase):

    node_type = EventDict
    leafnode_type = (Grep, Split, Settings)


    @classmethod
    def new_branching(cls, name, leaf=None):
        raise NotImplementedError('branching not supported!')

    def leaf_from_string(self, name, value, parent):
        if name == 'grep':
            return Grep(value)
        if name == 'split':
            return Split(value)
        if name == 'settings':
            return Settings(value)
        raise InputError('cannot parse tree')



def event_from_dct(name, dct):
    default_settings = Settings('')
    if not all(key in dct for key in ('grep',)):
        raise KeyError('necessary keys needed')

    if 'settings' not in dct:
        dct['settings'] = default_settings

    grep = dct['grep']

    if 'split' not in dct:
        return Event(name,
                     grep.name, {'keyword': grep.keyword,
                                 'ilen': grep.ilen,
                                 'ishift': grep.ishift},
                     settings=dct['settings'].value,
                     )

    split = dct['split']

    return Event(name,
                 grep.name, {'keyword': grep.keyword,
                             'ilen': grep.ilen,
                             'ishift': grep.ishift},
                 func='split',
                 func_kwargs={'idx': split.idx,
                              'typ': split.typ},
                 settings=dct['settings'].value,
                 )


def generate_events(eventstring):
    events = EventGenerator(eventstring).tree
    return {name: event_from_dct(name, eventdct) for name, eventdct in events.items()}


def generate_filereader(name, events):
    if isinstance(events, str):
        events = generate_events(events)
    if not isinstance(events, dict):
        raise ValueError
    return _generate_filereader(name, events)
