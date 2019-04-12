from ..fileinput import pygrep_str
from ..fileinput import pygrep_iterator
from ..fileinput import pygrep_iterator_lines
from ..fileio import file_reading_iterator_raw
import os

pwd = os.path.dirname(os.path.abspath(__file__))

h2o = os.path.join(pwd, "h2o.log")

def test_pygrep():
    with open(h2o, "r") as f:
        txt = f.read()
    iterator = file_reading_iterator_raw(h2o)
    #
    ilen = 100
    #
    val_str = pygrep_str(txt, "NAtoms=", length=ilen)
    val_iter = pygrep_iterator(iterator, "NAtoms=", ilen=ilen)
    #
    assert val_str[0] == val_iter[0]

def test_pygrep_long():
    with open(h2o, "r") as f:
        txt = f.read()

    for ilen in [10, 100, 10000, 1000000, 100000000]:
        iterator = file_reading_iterator_raw(h2o)
        val_str = pygrep_str(txt, "NAtoms=", length=ilen)
        val_iter = pygrep_iterator(iterator, "NAtoms=", ilen=ilen)
        assert val_str[0] == val_iter[0]

def test_pygrep_iterator_lines():
    with open(h2o, "r") as f:
        txt = f.read()

    for ilen in [10]:
        for ishift in [0, 1, 2, 3]:
            print("ilen = %d, ishift = %d" % (ilen, ishift))
            iterator = file_reading_iterator_raw(h2o)
            val_iter = pygrep_iterator_lines(iterator, "NAtoms=", ilen=ilen, ishift=ishift)
            print("length= %d" % len(val_iter.splitlines()))
            print(val_iter)
