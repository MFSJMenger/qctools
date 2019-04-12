from ..qctools import QCReader
from ..parser import GaussianReader
import os

pwd = os.path.dirname(os.path.abspath(__file__))
h2o = os.path.join(pwd, "h2o.log")

def test_qcreader():
    QCReader(h2o)

def test_gaussian_reader():
    val = GaussianReader(h2o, ["NAtoms"])
