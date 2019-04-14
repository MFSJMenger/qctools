# -*- coding: utf-8 -*-

"""Top-level package for qctools."""

__author__ = """Maximilian Menger"""
__email__ = 'maximilian.menger@univie.ac.at'
__version__ = '0.1.0'

from .eventhandler import EventHandler
from .parser import BaseEventReader
from .parser import GaussianReader
# qc configs
from .gaussian_config import gaussian_config
#
from .events import register_event
from .events import print_possible_events
from .events import Event
