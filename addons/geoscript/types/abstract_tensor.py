#!/usr/bin/python3

from .abstract_socket import AbstractSocket


class AbstractTensor(AbstractSocket):
    """A mathematical object on which various operations can be performed.

    A mathematical object such as a Scalar or a Vector, on which mathematical
    operations can be performed.
    """

    @staticmethod
    def math_operation_unary(self, operation: str = "ADD", use_clamp: bool = False):
        return NotImplemented

    @staticmethod
    def math_operation_binary(
        left, right, operation: str = "ADD", use_clamp: bool = False
    ):
        return NotImplemented

    @staticmethod
    def math_comparison(
        left, right, epsilon, operation: str = "LESS_THAN", mode="ELEMENT"
    ):
        return NotImplemented

    # Add:
    def __add__(self, other):
        return self.math_operation_binary(self, other, operation="ADD")

    def __radd__(self, other):
        return self.math_operation_binary(other, self, operation="ADD")

    # Subtract:
    def __sub__(self, other):
        return self.math_operation_binary(self, other, operation="SUBTRACT")

    def __rsub__(self, other):
        return self.math_operation_binary(other, self, operation="SUBTRACT")

    # Multiply:
    def __mul__(self, other):
        return self.math_operation_binary(self, other, operation="MULTIPLY")

    def __rmul__(self, other):
        return self.math_operation_binary(other, self, operation="MULTIPLY")

    # Divide:
    def __div__(self, other):
        return self.math_operation_binary(self, other, operation="DIVIDE")

    def __rdiv__(self, other):
        return self.math_operation_binary(other, self, operation="DIVIDE")

    def __truediv__(self, other):
        return self.math_operation_binary(self, other, operation="DIVIDE")

    def __rtruediv__(self, other):
        return self.math_operation_binary(other, self, operation="DIVIDE")

    # Modulo:
    def __mod__(self, other):
        return self.math_operation_binary(self, other, operation="MODULO")

    def __rmod__(self, other):
        return self.math_operation_binary(other, self, operation="MODULO")

    # Power:
    def __pow__(self, other):
        return self.math_operation_binary(self, other, operation="POWER")

    def __rpow__(self, other):
        return self.math_operation_binary(other, self, operation="POWER")

    # Unary operations:
    def __abs__(self):
        return self.math_operation_unary(self, operation="ABSOLUTE")

    def __neg__(self):
        return self.math_operation_binary(-1.0, self, operation="MULTIPLY")

    def __round__(self):
        return self.math_operation_unary(self, operation="ROUND")

    def __trunc__(self):
        return self.math_operation_unary(self, operation="TRUNC")

    def __floor__(self):
        return self.math_operation_unary(self, operation="FLOOR")

    def __ceil__(self):
        return self.math_operation_unary(self, operation="CEIL")
