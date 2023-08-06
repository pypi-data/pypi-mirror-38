**Currently only as placeholder (because a base package jtypes.jvm is still in development)**

jtypes.py4j
===========

Enables Python to dynamically access arbitrary Java objects.

Overview
========

  **jtypes.py4j** enables Python programs to dynamically access arbitrary Java objects via
  Java's Native Invocation Interface (JNI).

  `PyPI record`_.

  | **jtypes.py4j** is a lightweight Python package, based on the *ctypes* or *cffi* library.
  | It is an almost fully compliant implementation of Barthelemy Dagenais's **Py4J** package
    by reimplementing its functionality in a clean Python via JNI instead of Python and
    Java via custom API service.

About Py4J:
-----------

Borrowed from the `original website`_:

  **Py4J** enables Python programs running in a Python interpreter to dynamically
  access Java objects in a Java Virtual Machine. Methods are called as if the
  Java objects resided in the Python interpreter and Java collections can be
  accessed through standard Python collection methods. **Py4J** also enables Java
  programs to call back Python objects.

  | Here is a brief example of what you can do with **Py4J**.
  | The following Python program creates a java.util.Random instance from a JVM
    and calls some of its methods.

  .. code:: python

     >>> from py4j.java_gateway import JavaGateway
     >>> gateway = JavaGateway()                  # connect to the JVM
     >>> random = gateway.jvm.java.util.Random()  # create a java.util.Random instance
     >>> number1 = random.nextInt(10)             # call the Random.nextInt method
     >>> number2 = random.nextInt(10)
     >>> print(number1,number2)
     (2, 7)

Requirements
============

- Java Runtime (JRE) or Java Development Kit (JDK), and NumPy.

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

    python -m pip install --upgrade jtypes.py4j

To ensure everything is running correctly you can run the tests using::

    python -m jt.py4j.tests

Development
===========

Visit `development page`_

Installation from sources:

Clone the `sources`_ and run::

    python -m pip install ./jtypes.py4j

or on development mode::

    python -m pip install --editable ./jtypes.py4j

Prerequisites:

+ Development is strictly based on *tox*. To install it run::

    python -m pip install tox

License
=======

  | Copyright (c) 2015-2018, Adam Karpierz
  |
  | Licensed under the BSD license
  | http://opensource.org/licenses/BSD-3-Clause
  | Please refer to the accompanying LICENSE file.

Authors
=======

* Adam Karpierz <adam@karpierz.net>

.. _PyPI record: https://pypi.python.org/pypi/jtypes.py4j
.. _original website: https://www.py4j.org
.. _development page: https://github.com/karpierz/jtypes.py4j
.. _sources: https://github.com/karpierz/jtypes.py4j
