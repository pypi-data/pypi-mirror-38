**Currently only as placeholder (because a base package jtypes.jvm is still in development)**

jtypes.jpy
==========

Bi-directional Python-Java bridge.

Overview
========

  **jtypes.jpy** is a bi-directional bridge between Python and Java which can be use
  to call Java from Python and Python from Java.

  `PyPI record`_.

  | **jtypes.jpy** is a lightweight Python package, based on the *ctypes* or *cffi* library.
  | It is an almost fully compliant implementation of Norman Fomferra's **Jpy** package
    by reimplementing its functionality in a clean Python instead of C.

About Jpy:
----------

Borrowed from the `original website`_:

  **jpy** is a bi-directional Java-Python bridge allowing you to call Java from Python
  and Python from Java.

  **jpy** is a **bi-directional** Python-Java bridge which you can use to embed Java code
  in Python programs or the other way round. It has been designed particularly with
  regard to maximum data transfer speed between the two languages. It comes with a
  number of outstanding features:

  * Fully translates Java class hierarchies to Python
  * Transparently handles Java method overloading
  * Support of Java multi-threading
  * Fast and memory-efficient support of primitive Java array parameters via
    `Python buffers <http://docs.python.org/3.3/c-api/buffer.html>`__
    (e.g. `numpy arrays <http://docs.scipy.org/doc/numpy/reference/arrays.html>`__)
  * Support of Java methods that modify primitive Java array parameters (mutable
    parameters)
  * Java arrays translate into Python sequence objects
  * Java API for accessing Python objects (``jpy.jar``)

Installation
============

Prerequisites:

+ Python 2.7 or higher or 3.4 or higher

  * http://www.python.org/
  * 2.7 and 3.6 are primary test environments.

+ pip and setuptools

  * http://pypi.python.org/pypi/pip
  * http://pypi.python.org/pypi/setuptools

To install run::

    python -m pip install --upgrade jtypes.jpy

To ensure everything is running correctly you can run the tests using::

    python -m jt.jpy.tests

Development
===========

Visit `development page`_

Installation from sources:

Clone the `sources`_ and run::

    python -m pip install ./jtypes.jpy

or on development mode::

    python -m pip install --editable ./jtypes.jpy

Prerequisites:

+ Development is strictly based on *tox*. To install it run::

    python -m pip install tox

License
=======

  | Copyright 2014-2018 Adam Karpierz
  |
  | Licensed under the Apache License, Version 2.0
  | http://www.apache.org/licenses/LICENSE-2.0
  | Please refer to the accompanying LICENSE file.

Authors
=======

* Adam Karpierz <adam@karpierz.net>

.. _PyPI record: https://pypi.python.org/pypi/jtypes.jpy
.. _original website: http://jpy.readthedocs.org/en/latest
.. _development page: https://github.com/karpierz/jtypes.jpy
.. _sources: https://github.com/karpierz/jtypes.jpy
