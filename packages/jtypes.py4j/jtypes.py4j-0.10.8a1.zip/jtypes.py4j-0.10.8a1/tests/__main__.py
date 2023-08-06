# Copyright (c) 2015-2018, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from __future__ import absolute_import, print_function

import unittest
import sys
import os
import importlib
import logging

from . import test_dir


def test_suite(names=None, omit=()):

    from .python import __name__ as pkg_name
    from .python import __path__ as pkg_path
    import unittest
    import pkgutil
    if names is None:
        names = [name for _, name, _ in pkgutil.iter_modules(pkg_path)
                 if name != "__main__" and name not in omit]
    names = [".".join((pkg_name, name)) for name in names]
    tests = unittest.defaultTestLoader.loadTestsFromNames(names)
    return tests


def main():

    #sys.modules["py4j"]                  = importlib.import_module("jt.py4j")
    #sys.modules["py4j.compat"]           = importlib.import_module("jt.py4j.compat")
    #sys.modules["py4j.clientserver"]     = importlib.import_module("jt.py4j.clientserver")
    #sys.modules["py4j.finalizer"]        = importlib.import_module("jt.py4j.finalizer")
    #sys.modules["py4j.java_collections"] = importlib.import_module("jt.py4j.java_collections")
    #sys.modules["py4j.java_gateway"]     = importlib.import_module("jt.py4j.java_gateway")
    #sys.modules["py4j.protocol"]         = importlib.import_module("jt.py4j.protocol")
    #sys.modules["py4j.signals"]          = importlib.import_module("jt.py4j.signals")
    #sys.modules["py4j.version"]          = importlib.import_module("jt.py4j.version")

    import jt.jvm.platform
    jvm_path = jt.jvm.platform.JVMFinder().get_jvm_path()

    print("Running testsuite using JVM:", jvm_path, "\n", file=sys.stderr)

    try:
        tests = test_suite(sys.argv[1:] or None)
        result = unittest.TextTestRunner(verbosity=2).run(tests)
    finally:
        pass

    sys.exit(0 if result.wasSuccessful() else 1)


if __name__.rpartition(".")[-1] == "__main__":
    # logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)
    main()
