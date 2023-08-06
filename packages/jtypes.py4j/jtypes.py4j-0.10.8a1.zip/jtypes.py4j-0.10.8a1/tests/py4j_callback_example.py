"""
Created on Apr 27, 2010

@author: barthelemy
"""
from __future__ import absolute_import  # <AK> added

from jt.py4j.java_gateway import JavaGateway, CallbackServerParameters
from jt.py4j.protocol import Py4JJavaError


class Addition(object):
    def doOperation(self, i, j, k=None):
        if k is None:
            return i + j
        else:
            return 3722507311

    class Java:
        implements = ["py4j.examples.Operator"]

if __name__ == "__main__":
    gateway = JavaGateway(
        callback_server_parameters=CallbackServerParameters())
    operator = Addition()
    numbers = gateway.entry_point.randomBinaryOperator(operator)
    print(numbers)
    try:
        numbers = gateway.entry_point.randomTernaryOperator(operator)
        print(numbers)
        raise RuntimeError("Java integer overflow expected!")
    except Py4JJavaError as exc:
        print("Expected integer overflow has ocurred!:")
        print(exc)
    gateway.shutdown()
