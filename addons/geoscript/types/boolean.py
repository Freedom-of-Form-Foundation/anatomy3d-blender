#!/usr/bin/python3

import bpy

from .abstract_socket import AbstractSocket


class Boolean(AbstractSocket):
    """A mathematics operation in a Geometry Node tree. Maps to a "Math" node."""

    @staticmethod
    def get_bl_idnames():
        """Returns a list of Blender socket types that this class represents.

        Returns:
            List of strings corresponding to Blender Geometry Nodes socket
            types.
        """
        return ["BOOLEAN"]

    @staticmethod
    def math_operation_unary(self, operation: str = "ADD"):
        node = self.add_linked_node([self], "FunctionNodeBooleanMath")
        node.get_bl_node().operation = operation
        return Boolean(node, 0)

    @staticmethod
    def math_operation_binary(left, right, operation: str = "ADD"):
        if not isinstance(right, Boolean | bool):
            return NotImplemented
        if not isinstance(left, Boolean | bool):
            return NotImplemented
        if isinstance(left, bool) and isinstance(right, bool):
            return NotImplemented
        node = AbstractSocket.add_linked_node([left, right], "FunctionNodeBooleanMath")

        bl_node = node.get_bl_node()
        assert isinstance(bl_node, bpy.types.FunctionNodeBooleanMath)
        bl_node.operation = operation

        return Boolean(node, 0)

    # And:
    def __and__(self, other):
        return self.math_operation_binary(self, other, operation="AND")

    def __rand__(self, other):
        return self.math_operation_binary(other, self, operation="AND")

    # Or:
    def __or__(self, other):
        return self.math_operation_binary(self, other, operation="OR")

    def __ror__(self, other):
        return self.math_operation_binary(other, self, operation="OR")

    # Xor:
    def __xor__(self, other):
        return self.math_operation_binary(self, other, operation="XOR")

    def __rxor__(self, other):
        return self.math_operation_binary(other, self, operation="XOR")

    def __ne__(self, other):
        return self.math_operation_binary(self, other, operation="XOR")

    # Not:
    def __invert__(self, other):
        return self.math_operation_binary(self, other, operation="NOT")

    def __rinvert__(self, other):
        return self.math_operation_binary(other, self, operation="NOT")

    # Equal:
    def __eq__(self, other):
        return self.math_operation_binary(self, other, operation="XNOR")

    # Subtract:
    def __sub__(self, other):
        return self.math_operation_binary(self, other, operation="NIMPLY")
