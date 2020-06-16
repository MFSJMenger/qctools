from copy import deepcopy
#
from .colt.generator import GeneratorBase, BranchingNode
from .colt.validator import Validator
#
from .events import Event
from .parser import generate_filereader as _generate_filereader


ilist_parser = Validator('ilist').validate
list_parser = Validator('list').validate
bool_parser = Validator('bool').validate


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
        cols = tuple(col.strip() for col in string.split(self.seperator))
        if len(cols) != 2:
            raise ValueError('Split needs to be define as \n split = idx :: typ\n')
        idx, types = cols

        idx = ilist_parser(idx)
        types = tuple(self._func_types[entry] for entry in list_parser(types))
        if len(idx) == 1:
            idx = idx
        if len(types) == 1:
            types = tuple(types[0] for _ in idx)
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
            dct['multi'] = bool_parser(cols[0])
        if ncols >= 2:
            dct['reset'] = bool_parser(cols[1])
        if ncols >= 3:
            dct['delete'] = bool_parser(cols[2])
        return dct

    def _string_to_dict(self, string):
        dct = {}
        for key_value in  list_parser(string):
            key, value = tuple(key_value.split('='))
            dct[key] = bool_parser(value)
        return dct


class EventDict(dict):
    pass


class JoinedEventContainer(BranchingNode):

    def __init__(self, name, leaf, subnodes=None):
        BranchingNode.__init__(self, name, leaf, subnodes)


class EventGenerator(GeneratorBase):

    node_type = EventDict
    leafnode_type = (Grep, Split, Settings)
    branching_type = JoinedEventContainer

    @classmethod
    def new_branching(cls, name, leaf=None):
        if leaf is not None:
            raise Exception("Generator accepts no leaf key for branching")
        return JoinedEventContainer(name, leaf)

    @staticmethod
    def new_node():
        return EventDict()

    @staticmethod
    def tree_container():
        return EventDict()

    def leaf_from_string(self, name, value, parent):
        if not self._is_single_layer(parent):
            raise Exception("Generator accepts only one layer")
        if name == 'grep':
            return Grep(value)
        if name == 'split':
            return Split(value)
        if name == 'settings':
            return Settings(value)
        raise InputError('cannot parse tree')

    @classmethod
    def _is_single_layer(cls, parent):
        if parent == "":
            return False
        parent, child = cls.rsplit_keys(parent)
        if child is None:
            return True
        return False


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
    out = {}
    for name, eventdct in events.items():
        if isinstance(eventdct, EventDict):
            out[name] = event_from_dct(name, eventdct)
        elif isinstance(eventdct, JoinedEventContainer):
            out[name] = tuple(event_from_dct(key, event) for key, event in eventdct.items())
        else:
            raise Exception("")
    return out


def generate_filereader(name, events):
    if isinstance(events, str):
        events = generate_events(events)
    if not isinstance(events, dict):
        raise ValueError
    return _generate_filereader(name, events)
