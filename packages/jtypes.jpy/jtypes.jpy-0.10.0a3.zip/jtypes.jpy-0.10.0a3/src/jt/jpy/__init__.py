# Copyright 2014-2018 Adam Karpierz
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

from . import __config__ ; del __config__
from .__about__ import * ; del __about__

#__name__ = "jpy"
__doc__ = """Bi-directional Python-Java Bridge"""

__all__ = ('has_jvm', 'create_jvm', 'destroy_jvm', 'get_type', 'cast', 'array',
           'JType', 'JField', 'JMethod', 'JOverloadedMethod', 'JException',
           'types', 'type_callbacks', 'type_translations',
           'diag', 'VerboseExceptions')

from ._main import has_jvm, create_jvm, destroy_jvm, get_type, cast, array

from ._jtype   import JType
from ._jfield  import JField
from ._jmethod import JOverloadedMethod, JMethod
from ._main    import JException

from ._main    import types, type_callbacks, type_translations
from ._main    import diag, VerboseExceptions
