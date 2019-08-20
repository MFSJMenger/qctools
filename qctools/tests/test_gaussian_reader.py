import pytest
import os

from ..parser import GaussianReader

# get absolute path for h2o.log file
pwd = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture
def gaussian_h2o_file():
    return os.path.join(pwd, "h2o.log")


def test_gaussian_reader_default(gaussian_h2o_file):
    """add a default value and check for it"""
    val = GaussianReader(gaussian_h2o_file, [], {"NAtoms": 10})
    assert val["NAtoms"] == 10


def test_gaussian_reader_natoms(gaussian_h2o_file):
    """read natoms"""
    val = GaussianReader(gaussian_h2o_file, ["NAtoms"])
    assert val["NAtoms"] == 3


def test_gaussian_reader_forces(gaussian_h2o_file):
    val = GaussianReader(gaussian_h2o_file, ["NAtoms", "forces"])
    assert len(val["forces"]) == 7
