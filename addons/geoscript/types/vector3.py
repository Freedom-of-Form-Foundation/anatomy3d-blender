#!/usr/bin/python3

import bpy

from typing import Union
from ..exceptions import BlenderTypeError
from .abstract_socket import AbstractSocket
from .abstract_tensor import AbstractTensor
from .scalar import Scalar


class Vector3(AbstractTensor):
    """A 3D vector object in Geoscript."""

    @staticmethod
    def get_bl_idnames() -> list[str]:
        """Returns a list of Blender socket types that this class represents.

        Returns:
            List of strings corresponding to Blender Geometry Nodes socket
            types.
        """
        return ["VECTOR"]

    @staticmethod
    def math_operation_unary(
        vector: "Vector3", operation: str = "ADD", use_clamp: bool = False
    ) -> "Vector3":
        node = AbstractSocket.add_linked_node([vector], "ShaderNodeVectorMath")
        bl_node = node.get_bl_node()

        if not isinstance(bl_node, bpy.types.ShaderNodeVectorMath):
            raise BlenderTypeError(bl_node, "bpy.types.ShaderNodeVectorMath")
        bl_node.operation = operation

        return Vector3(node, 0)

    @staticmethod
    def math_operation_binary(
        left: Union["Vector3", Scalar, float],
        right: "Vector3",
        operation: str = "ADD",
        use_clamp: bool = False,
    ) -> "Vector3":
        if not isinstance(right, Vector3):
            return NotImplemented
        if not isinstance(left, Vector3 | Scalar | float):
            return NotImplemented

        node = AbstractSocket.new_node([left, right], "ShaderNodeVectorMath")
        node.connect_argument(1, right)

        bl_node = node.get_bl_node()
        if not isinstance(bl_node, bpy.types.ShaderNodeVectorMath):
            raise BlenderTypeError(bl_node, "bpy.types.ShaderNodeVectorMath")
        bl_node.operation = operation

        # Connect the left argument:
        if isinstance(left, Vector3):
            node.connect_argument(0, left)
        elif isinstance(left, Scalar | float):
            node.connect_argument(3, left)

        return Vector3(node, 0)

    # Multiply:
    def __mul__(self, other):
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, float | Scalar):
            return self.math_operation_binary(other, self, operation="SCALE")
        else:
            return NotImplemented

    # Component getters:
    def check_or_create_separation_node(self) -> None:
        if not hasattr(self, "separate_xyz_node"):
            node = self.new_node([self], "ShaderNodeSeparateXYZ")
            self.separate_xyz_node = node
            node.connect_argument(0, self)

    @property
    def x(self) -> Scalar:
        self.check_or_create_separation_node()
        return Scalar(self.separate_xyz_node, 0)

    @property
    def y(self) -> Scalar:
        self.check_or_create_separation_node()
        return Scalar(self.separate_xyz_node, 1)

    @property
    def z(self) -> Scalar:
        self.check_or_create_separation_node()
        return Scalar(self.separate_xyz_node, 2)
