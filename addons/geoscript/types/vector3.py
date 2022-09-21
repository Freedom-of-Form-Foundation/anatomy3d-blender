#!/usr/bin/python3

import bpy

from .abstract_tensor import AbstractTensor
from .scalar import Scalar


class Vector3(AbstractTensor):
    """A 3D vector object in Geoscript."""

    def __init__(
        self,
        node_tree: bpy.types.NodeTree = None,
        socket_reference: bpy.types.NodeSocket = None,
        layer: int = 0,
    ):
        super().__init__(node_tree, socket_reference, layer)

    @staticmethod
    def get_bl_idnames() -> list[str]:
        """Returns a list of Blender socket types that this class represents.

        Returns:
            List of strings corresponding to Blender Geometry Nodes socket
            types.
        """
        return ["VECTOR"]

    @staticmethod
    def math_operation_unary(vector, operation: str = "ADD", use_clamp: bool = False):
        tree, math_node, layer = vector.new_node([vector], "ShaderNodeVectorMath")
        math_node.operation = operation

        tree.links.new(vector.socket_reference, math_node.inputs[0])

        return Vector3(tree, math_node.outputs[0], layer)

    @staticmethod
    def math_operation_binary(
        left, right, operation: str = "ADD", use_clamp: bool = False
    ):
        if isinstance(right, left.__class__ | Scalar):
            tree, math_node, layer = left.new_node(
                [left, right], "ShaderNodeVectorMath"
            )
            math_node.operation = operation

            tree.links.new(left.socket_reference, math_node.inputs[0])
            tree.links.new(right.socket_reference, math_node.inputs[1])

            return Vector3(tree, math_node.outputs[0], layer)

        elif isinstance(right, float):
            tree, math_node, layer = left.new_node([left], "ShaderNodeVectorMath")
            math_node.operation = operation
            math_node.inputs[3].default_value = right

            tree.links.new(left.socket_reference, math_node.inputs[0])

            return Vector3(tree, math_node.outputs[0], layer)

        elif isinstance(left, float):
            tree, math_node, layer = right.new_node([right], "ShaderNodeVectorMath")
            math_node.operation = operation
            math_node.inputs[3].default_value = left

            tree.links.new(right.socket_reference, math_node.inputs[1])

            return Vector3(tree, math_node.outputs[0], layer)

        else:
            return NotImplemented

    # Multiply:
    def __mul__(self, other):
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, float | Scalar):
            return self.math_operation_binary(self, other, operation="SCALE")
        else:
            return NotImplemented

    # Component getters:
    def check_or_create_separation_node(self):
        if not hasattr(self, "separate_xyz_node"):
            tree, node, layer = self.new_node([self], "ShaderNodeSeparateXYZ")
            self.separate_xyz_node = node
            self.separate_xyz_layer = layer

            tree.links.new(self.socket_reference, node.inputs[0])

    @property
    def x(self):
        self.check_or_create_separation_node()
        return Scalar(
            self.node_tree,
            self.separate_xyz_node.outputs[0],
            self.separate_xyz_layer,
        )

    @property
    def y(self):
        self.check_or_create_separation_node()
        return Scalar(
            self.node_tree,
            self.separate_xyz_node.outputs[1],
            self.separate_xyz_layer,
        )

    @property
    def z(self):
        self.check_or_create_separation_node()
        return Scalar(
            self.node_tree,
            self.separate_xyz_node.outputs[2],
            self.separate_xyz_layer,
        )
