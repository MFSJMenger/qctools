import os

from ..parser import GaussianReader

# get absolute path for h2o.log file
pwd = os.path.dirname(os.path.abspath(__file__))
h2o = os.path.join(pwd, "h2o.log")


def test_gaussian_reader_default():
    """add a default value and check for it"""
    val = GaussianReader(h2o, [], {"NAtoms": 10})
    assert val["NAtoms"] == 10


def test_gaussian_reader_natoms():
    """read natoms"""
    val = GaussianReader(h2o, ["NAtoms"])
    assert val["NAtoms"] == 3


def test_gaussian_reader_forces():
    val = GaussianReader(h2o, ["NAtoms", "forces"])
    assert len(val["forces"]) == 7
