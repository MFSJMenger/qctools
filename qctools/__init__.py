# -*- coding: utf-8 -*-
"""Top-level package for qctools."""

__author__ = """Maximilian Menger"""
__email__ = 'm.f.s.j.menger@rug.nl'
__version__ = '0.2.0'

from .generator import generate_filereader
from .parser import GaussianReader
# molden
from .molden_config import MoldenParser
# add events and show possible event types
from .events import register_event_type
from .events import print_possible_events
# Event class an special events
from .events import Event
from .events import reset_event
