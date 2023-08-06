# Copyright 2014-2018 Adam Karpierz
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

from __future__ import absolute_import

from ..jvm.lib import py2compatible
from ..jvm.lib import annotate
from ..jvm.lib import public

from ..jvm import EJavaModifiers


@public
@py2compatible
class JField(object):

    """Java Field Wrapper"""

    # "jpy.JField" # tp_name #
    # Equivalent of: jt.jtypes.JavaField

    @annotate(declaringClass='JType*', fieldName=str, fieldType='JType*', isStatic=jni.jboolean, isFinal=jni.jboolean, fid=jni.jfieldID)
    def __new__(cls, declaringClass, fieldName, fieldType, isStatic, isFinal, fid):

        self = super(JField, cls).__new__(cls)
        self.declaringClass = declaringClass # JType*    # The declaring class.
        self.__name      = fieldName      # PyObject* # Field name.
        self.__jtype     = fieldType      # JType*    # Field type.
        self.__is_static = isStatic       # bool      # Method is static?
        self.__is_final  = isFinal        # bool      # Method is final?
        self.fid         = fid            # jfieldID  # Field ID retrieved from JNI.
        return self

    name      = property(lambda self: self.__name,      doc="Field name")
    type      = property(lambda self: self.__jtype,     doc="Field type")  #*** jtypes extension ***#
    is_static = property(lambda self: self.__is_static, doc="Tests if this is a static field")
    is_final  = property(lambda self: self.__is_final,  doc="Tests if this is a final field")

    def __get__(self, this, cls):

        pass # !!!

    def __set__(self, this, value):

        from .__config__ import config

        pass # !!!

    def __str__(self):

        return self.name

    def __repr__(self):

        name = JPy_AS_UTF8(self.name) # const char*
        return "{}(name='{}', is_static={}, is_final={}, fid={:08X})".format(
               type(self).__name__, name, self.__is_static, self.__is_final, self.fid)


@public
class JConstField(JField):

    def __get__(self, this, cls):

        return super(JConstField, self).__get__(this, cls)

    def __set__(self, this, value):

        raise AttributeError("Field is readonly")

    def __delete__(self, this):

        raise AttributeError("Field is undeletable")
