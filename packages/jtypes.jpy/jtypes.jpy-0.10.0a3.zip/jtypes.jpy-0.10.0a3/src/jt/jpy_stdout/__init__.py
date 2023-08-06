# Copyright 2014-2018 Adam Karpierz
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

"""Redirect 'stdout' to the console in embedded mode"""

from __future__ import absolute_import

from ..jvm.lib import annotate
from ..jvm.lib import public


@public
@annotate(text=str)
def write(text):

    """Internal function. Used to print to stdout in embedded mode."""

    if stdout != NULL:
        #const char* text;
        #if (!PyArg_ParseTuple(args, "s", &text)):
        #    return NULL;
        fprintf(stdout, "%s", text)


@public
@annotate()
def flush():

    """Internal function. Used to flush to stdout in embedded mode."""

    if stdout != NULL:
        fflush(stdout)
