# -*- coding: utf-8 -*-
"""Main module."""
from collections import OrderedDict
from .fileinput import pygrep_iterator_lines
from .fileio import file_reading_iterator_raw


class QCReader(object):
    """Class to read information from ASCII text files"""

    _elements = OrderedDict()
    _funcs = { 'iterator': file_reading_iterator_raw,
               'grep': pygrep_iterator_lines }

    def __init__(self, filename, reset=True):
        self._name = filename
        self._reset = reset
        self._values = dict( (key, None) for key in self._elements.keys() )


    @property
    def parse(self):
        self._parse_file()

    def _get_ilen(self, ilen):
        """Get ILEN as a function of local variables"""
        if type(ilen) == int:
            return ilen
        else:
            return self._values[ilen]

    def _set_iterator(self):
        return self._funcs['iterator'](self._name)

    def _grep(self, iterator, key, ilen, ishift):

        grep, ierr = self._funcs['grep'](
                    iterator,
                    self._elements[key]['grep']['keyword'],
                    ilen = ilen,
                    ishift = ishift,
            )

        if ierr == -1 and self._reset is True:
            # reset iterator
            iterator = self._set_iterator()

        return iterator, grep, ierr

    def _parse_file(self):
        iterator = self._set_iterator()

        for key in self._elements:
            #print("Key = %s" % key)
            ilen = self._get_ilen(self._elements[key]['grep']['ilen'])
            #print("ilen = %d" % ilen)
            ishift = self._get_ilen(self._elements[key]['grep']['ishift'])
            #print("ishift = %d" % ishift)
            if 'reset' in self._elements[key] and self._elements[key]['reset'] is True:
                # reset iterator
                iterator = self._set_iterator()
            # do multiple mapping
            if ('multigrep' in self._elements[key]) and (self._elements[key]['multigrep'] is True):
                ierr = 0
                self._values[key] = []
                while True:
                    iterator, grep, ierr = self._grep(iterator, key, ilen, ishift)
                    if ierr == -1:
                        break
                    self._values[key].append(self._elements[key]['func'](grep))
            # single mapping
            else:
                iterator, grep, ierr = self._grep(iterator, key, ilen, ishift)
                if ierr == -1:
                    self._values[key] = None
                    continue
                self._values[key] = self._elements[key]['func'](grep)

    @property
    def filename(self):
        return self._name

    @property
    def keys(self):
        return self._elements.keys()

    def __getitem__(self, key):
        assert key in self.keys
        return self._values[key]


class BaseConfigQCReader(QCReader):

    _config = OrderedDict()

    def __init__(self, filename, keys, reset=True):

        self._set_elements(keys)
        super(BaseConfigQCReader, self).__init__(filename, reset=reset)
        self.parse

    def _set_elements(self, keys):

        self._elements = OrderedDict()

        for key in keys:
            assert key in self._config.keys()
            self._elements[key] = self._config[key]
