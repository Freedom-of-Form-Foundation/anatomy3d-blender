#!/usr/bin/python3

"""Class and functions related to scalar fields in Geometry Nodes."""

from typing import Optional, Union

import bpy

from .abstract_socket import AbstractSocket
from .abstract_tensor import AbstractTensor
from .boolean import Boolean


class Scalar(AbstractTensor):
    """A scalar field within a Geoscript, which acts like `float`."""

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
        operand: "Scalar", operation: str = "ADD", use_clamp: bool = False
    ) -> "Scalar":
        """Adds a Math node to the Blender NodeTree with a single input connection.

        Args:
            operand:
                The operand on which the operation is performed.
            operation:
                The operation to perform on the operand. Must be a valid Blender Math
                Node operation string. Defaults to "ADD".
            use_clamp:
                Whether to clamp the output between 0.0 and 1.0. Defaults to False.

        Returns:
            The field after the operation has been applied.

        """
        node = AbstractSocket.add_linked_node([operand], "ShaderNodeMath")

        bl_node = node.get_bl_node()
        assert isinstance(bl_node, bpy.types.ShaderNodeMath)
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
        """Adds a Math node to the Blender NodeTree with two input connections.

        Args:
            left: The left operand.
            right: The right operand.
            operation:
                The operand type. Must be a valid Blender Math Node operation
                string. Defaults to "ADD".
            use_clamp:
                Whether to clamp the output between 0.0 and 1.0. Defaults to False.

        Returns:
            The field after the operation has been applied.

        """
        if not isinstance(right, Scalar | float):
            return NotImplemented
        if not isinstance(left, Scalar | float):
            return NotImplemented
        if isinstance(left, float) and isinstance(right, float):
            return NotImplemented

        node = AbstractSocket.add_linked_node([left, right], "ShaderNodeMath")

        bl_node = node.get_bl_node()
        assert isinstance(bl_node, bpy.types.ShaderNodeMath)
        bl_node.operation = operation
        bl_node.use_clamp = use_clamp

        return Scalar(node, 0)

    @staticmethod
    def math_operation_ternary(
        left: Union["Scalar", float],
        middle: Union["Scalar", float],
        right: Union["Scalar", float],
        operation: str = "MULTIPLY_ADD",
        use_clamp: bool = False,
    ) -> "Scalar":
        """Adds a Math node to the Blender NodeTree with three input connections.

        Args:
            left: The first operand.
            middle: The second operand.
            right: The third operand.
            operation:
                The operand type. Must be a valid Blender Math Node operation
                string. Defaults to "ADD".
            use_clamp:
                Whether to clamp the output between 0.0 and 1.0. Defaults to False.

        Returns:
            The field after the operation has been applied.

        """
        node = AbstractSocket.add_linked_node([left, middle, right], "ShaderNodeMath")

        bl_node = node.get_bl_node()
        assert isinstance(bl_node, bpy.types.ShaderNodeMath)
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
    ) -> Boolean:
        """Adds a Comparison node to the Blender NodeTree.

        Args:
            left: The first field to be compared.
            right: The second field to be compared.
            epsilon: The maximum deviation allowed in case of an "is equal" comparison.
            operation:
                The operand type. Must be a valid Blender Comparison Node operation
                string. Defaults to "LESS_THAN".
            mode:
                Which field gets compared.

        Returns:
            A boolean field which is true for each element where the comparison returned
            True, and false for each element where the comparison returned False.

        """
        if not isinstance(right, Scalar | float):
            return NotImplemented
        if not isinstance(left, Scalar | float):
            return NotImplemented
        if isinstance(left, float) and isinstance(right, float):
            return NotImplemented

        arguments = [left, right, epsilon]
        node = AbstractSocket.add_linked_node(arguments, "FunctionNodeCompare")

        bl_node = node.get_bl_node()
        assert isinstance(bl_node, bpy.types.FunctionNodeCompare)
        bl_node.operation = operation
        bl_node.data_type = "FLOAT"
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

    def to_radians(self) -> "Scalar":
        """Returns the scalar field after conversion from degrees to radians."""
        return Scalar.math_operation_unary(self, operation="RADIANS")

    def to_degrees(self) -> "Scalar":
        """Returns the scalar field after conversion from radians to degrees."""
        return Scalar.math_operation_unary(self, operation="DEGREES")
