"""
PSYPARSE:
========

PYSPARSE is a package designed to parse the logfiles of psychopy in
order to ease the manipulation and analyzation of data.

AUTHOR: Travis Nesland <nesland@musc.edu>
VERSION: alpha 0.0.1

"""  

from .global_functions import *
from .logfile import Logfile as Logfile
import handler
from .varmap import VarMap, read_varmap, attributes_for_class, available_classes
