#!/usr/bin/python3

import bpy

from typing import Optional, Union
from ..exceptions import BlenderTypeError
from .abstract_socket import AbstractSocket
from .abstract_tensor import AbstractTensor
from .boolean import Boolean


class Scalar(AbstractTensor):
    """A scalar type within a Geoscript, which acts like float."""

    @staticmethod
    def get_bl_idnames() -> list[str]:
        """Returns a list of Blender socket types that this class represents.

        Returns:
            List of strings corresponding to Blender Geometry Nodes socket
            types.
        """
        return ["VALUE", "INT"]

    @staticmethod
    def math_operation_unary(
        scalar, operation: str = "ADD", use_clamp: bool = False
    ) -> "Scalar":
        node = scalar.add_linked_node([scalar], "ShaderNodeMath")

        bl_node = node.get_bl_node()
        if not isinstance(bl_node, bpy.types.ShaderNodeMath):
            raise BlenderTypeError(bl_node, "bpy.types.ShaderNodeMath")
        bl_node.operation = operation
        bl_node.use_clamp = use_clamp

        return Scalar(node, 0)

    @staticmethod
    def math_operation_binary(
        left: Union["Scalar", float],
        right: Union["Scalar", float],
        operation: str = "ADD",
        use_clamp: bool = False,
    ) -> "Scalar":
        if not isinstance(right, Scalar | float):
            return NotImplemented
        if not isinstance(left, Scalar | float):
            return NotImplemented
        if isinstance(left, float) and isinstance(right, float):
            return NotImplemented

        node = AbstractSocket.add_linked_node([left, right], "ShaderNodeMath")

        bl_node = node.get_bl_node()
        if not isinstance(bl_node, bpy.types.ShaderNodeMath):
            raise BlenderTypeError(bl_node, "bpy.types.ShaderNodeMath")
        bl_node.operation = operation
        bl_node.use_clamp = use_clamp

        return Scalar(node, 0)

    @staticmethod
    def math_operation_ternary(
        left,
        middle,
        right,
        operation: str = "MULTIPLY_ADD",
        use_clamp: bool = False,
    ) -> "Scalar":
        node = AbstractSocket.add_linked_node([left, middle, right], "ShaderNodeMath")

        bl_node = node.get_bl_node()
        if not isinstance(bl_node, bpy.types.ShaderNodeMath):
            raise BlenderTypeError(bl_node, "bpy.types.ShaderNodeMath")
        bl_node.operation = operation
        bl_node.use_clamp = use_clamp

        return Scalar(node, 0)

    @staticmethod
    def math_comparison(
        left: Union["Scalar", float],
        right: Union["Scalar", float],
        epsilon: Optional[Union["Scalar", float]],
        operation: str = "LESS_THAN",
        mode: str = "ELEMENT",
    ) -> "Boolean":
        if not isinstance(right, Scalar | float):
            return NotImplemented
        if not isinstance(left, Scalar | float):
            return NotImplemented
        if isinstance(left, float) and isinstance(right, float):
            return NotImplemented

        arguments = [left, right, epsilon]
        node = AbstractSocket.add_linked_node(arguments, "FunctionNodeCompare")
        bl_node = node.get_bl_node()
        if not isinstance(bl_node, bpy.types.FunctionNodeCompare):
            raise BlenderTypeError(bl_node, "bpy.types.FunctionNodeCompare")

        bl_node.operation = operation
        bl_node.data_type = "FLOAT"
        if hasattr(bl_node, "mode"):
            bl_node.mode = mode

        return Boolean(node, 0)

    def __lt__(self, other):
        return self.math_comparison(self, other, None, operation="LESS_THAN")

    def __gt__(self, other):
        return self.math_comparison(self, other, None, operation="GREATER_THAN")

    def __le__(self, other):
        return self.math_comparison(self, other, None, operation="LESS_EQUAL")

    def __ge__(self, other):
        return self.math_comparison(self, other, None, operation="GREATER_EQUAL")

    def to_radians(self, value):
        return Scalar.math_operation_unary(value, operation="RADIANS")

    def to_degrees(self, value):
        return Scalar.math_operation_unary(value, operation="DEGREES")
