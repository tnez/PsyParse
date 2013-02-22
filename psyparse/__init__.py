"""
PSYPARSE:
========

PYSPARSE is a package designed to parse the logfiles of psychopy in
order to ease the manipulation and analyzation of data.

AUTHOR: Travis Nesland <nesland@musc.edu>
VERSION: alpha 0.0.1

"""  

from .logfile import Logfile as Logfile
from .handler.debug_handler import DebugHandler
from .varmap import Mapping, VarMap, read_varmap, available_classes
