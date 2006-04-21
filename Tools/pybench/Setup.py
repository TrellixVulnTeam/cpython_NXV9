#!python

# Setup file for pybench
#
# This file has to import all tests to be run; it is executed as
# Python source file, so you can do all kinds of manipulations here
# rather than having to edit the tests themselves.
#
# Note: Please keep this module compatible to Python 1.5.2.
#
# Tests may include features in later Python versions, but these
# should then be embedded in try-except clauses in this configuration
# module.

# Defaults
Number_of_rounds = 10
Warp_factor = 20

# Import tests
from Arithmetic import *
from Calls import *
from Constructs import *
from Lookups import *
from Instances import *
from Lists import *
from Tuples import *
from Dict import *
from Exceptions import *
from Imports import *
from Strings import *
from Numbers import *
try:
    from Unicode import *
except (ImportError, SyntaxError):
    pass
