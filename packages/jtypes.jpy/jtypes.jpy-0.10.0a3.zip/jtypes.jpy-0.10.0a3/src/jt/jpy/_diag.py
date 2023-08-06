# Copyright 2014-2018 Adam Karpierz
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

from __future__ import absolute_import, print_function

import sys

from ..jvm.lib.compat import *
from ..jvm.lib import annotate
from ..jvm.lib import public
from ..jvm.lib import const


@public
class Diag(object):

    """Controls output of diagnostic information for debugging"""

    # "jpy.Diag" # tp_name #

    F_OFF  = const(0x00, doc="Don't print any diagnostic messages")
    F_TYPE = const(0x01, doc="Type resolution: print diagnostic messages while generating Python classes from Java classes")
    F_METH = const(0x02, doc="Method resolution: print diagnostic messages while resolving Java overloaded methods")
    F_EXEC = const(0x04, doc="Execution: print diagnostic messages when Java code is executed")
    F_MEM  = const(0x08, doc="Memory: print diagnostic messages when wrapped Java objects are allocated/deallocated")
    F_JVM  = const(0x10, doc="JVM: print diagnostic information usage of the Java VM Invocation API")
    F_ERR  = const(0x20, doc="Errors: print diagnostic information when erroneous states are detected")
    F_ALL  = const(0xFF, doc="Print any diagnostic messages")

    _flags = 0x00  # F_OFF

    @property
    def flags(self):

        """Combination of diagnostic flags (F_* constants).
        If != 0, diagnostic messages are printed out."""

        return int(Diag._flags)

    @flags.setter
    def flags(self, value):

        if not isinstance(value, (int, long)):
            raise ValueError("value for 'flags' must be an integer number")

        Diag._flags = int(value)

    @staticmethod
    @annotate(flags=int, format=str)
    def print(flags, format, *args):

        if Diag._flags & flags:
            print(format.format(*args), end="")
            sys.stdout.flush()
