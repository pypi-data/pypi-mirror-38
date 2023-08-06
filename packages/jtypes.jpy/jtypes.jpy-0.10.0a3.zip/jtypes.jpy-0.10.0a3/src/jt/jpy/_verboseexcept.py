# Copyright 2014-2018 Adam Karpierz
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

from ..jvm.lib.compat import *
from ..jvm.lib import annotate
from ..jvm.lib import public


@public
class VerboseExceptions(object):

    """Controls python exception verbosity"""

    # "jpy.VerboseExceptions" # tp_name #

    _enabled = False

    @property
    def enabled(self):

        return bool(VerboseExceptions._enabled)

    @enabled.setter
    def enabled(self, value):

        if not isinstance(value, bool):
            raise ValueError("value for 'enabled' must be a boolean")

        VerboseExceptions._enabled = bool(value)
