#!/usr/bin/python3

from typing import Any, Tuple, Optional
import bpy

from .types import (
    NodeHandle,
    AbstractSocket,
    Geometry,
    Vector3,
    Scalar,
    Boolean,
    Object,
)


class GeometryNodeTree:
    """Geoscript-specific wrapper for bpy.types.GeometryNodeTree."""

    def __init__(self, name: str):
        self.__create_or_overwrite_bl_tree(name)

        # TODO: removing the inputs and outputs of the pre-existing tree will reset all
        # parameters. This should be fixed to prevent having to redo the parameters if
        # the user changed them.

        self.inputs = self.Inputs(self.node_tree)
        self.outputs = self.Outputs(self.node_tree)
        self.attributes = self.Attributes(self.node_tree)

        self.function()

        self.beautify_node_tree()

    def function(self) -> Any:
        """The Geoscript code that represents the node tree.

        This should be completed in a subclass and should contain Geoscript code.
        """
        pass

    def __create_or_overwrite_bl_tree(self, name: str):
        """Retrieves and erases the Blender node tree that has the name `name`.

        Note:
            If the tree doesn't yet exist, this function creates a new tree. If it
            does exist, it erases the tree's contents."""
        self.__registered_name = name
        self.node_tree = bpy.data.node_groups.get(name)
        if not self.node_tree:
            self.node_tree = bpy.data.node_groups.new(name, "GeometryNodeTree")
        self.__clean()

    def __clean(self):
        """Remove all content from the existing node tree."""
        for node in self.node_tree.nodes:
            self.node_tree.nodes.remove(node)

        for i in self.node_tree.inputs:
            self.node_tree.inputs.remove(i)

        for o in self.node_tree.outputs:
            self.node_tree.outputs.remove(o)

    def get_registered_name(self):
        return self.__registered_name

    def get_bl_tree(self):
        return self.node_tree

    @staticmethod
    def __does_node_overlap(
        bl_node1: bpy.types.Node, bl_node2: bpy.types.Node, padding: float = 20.0
    ) -> bool:
        """Returns True if two Blender nodes visually overlap."""
        return (
            bl_node1.location[0] + bl_node1.width + padding >= bl_node2.location[0]
            and bl_node1.location[0] <= bl_node2.location[0] + bl_node2.width + padding
            and bl_node1.location[1] + bl_node2.height + padding >= bl_node2.location[1]
            and bl_node1.location[1] <= bl_node2.location[1] + bl_node2.height + padding
        )

    def beautify_node_tree(self) -> None:
        """Visually moves the nodes around in the node tree for better readability."""
        bl_tree = self.node_tree

        # Shift down all nodes that overlap:
        for bl_node in bl_tree.nodes:
            for other_node in bl_tree.nodes:
                if bl_node == other_node:
                    continue
                if self.__does_node_overlap(bl_node, other_node) is True:
                    other_node.location[1] -= bl_node.height + 140.0

    class Inputs:
        """Handles adding new tree inputs to the node tree."""

        def __init__(self, bl_node_tree: bpy.types.GeometryNodeTree):
            self.bl_node_tree = bl_node_tree
            self.input_counter = 0
            self.group_input = self.bl_node_tree.nodes.new("NodeGroupInput")

        def _add_input(
            self, input_name: str, socket_class: type, socket_typename: str
        ) -> Tuple[AbstractSocket, bpy.types.NodeSocketInterface]:
            bl_socket = self.bl_node_tree.inputs.new(socket_typename, input_name)
            node_handle = NodeHandle(self.bl_node_tree, self.group_input)
            socket = socket_class(node_handle, self.input_counter)
            self.input_counter += 1
            return socket, bl_socket

        def add_geometry(self, name: str = "Geometry", tooltip: str = "") -> Geometry:
            socket, bl_socket = self._add_input(name, Geometry, "NodeSocketGeometry")
            assert isinstance(socket, Geometry)
            bl_socket.description = tooltip
            return socket

        def add_object(
            self,
            name: str = "Object",
            tooltip: str = "",
            default_value: Optional[bpy.types.Object] = None,
        ) -> Object:
            socket, bl_socket = self._add_input(name, Object, "NodeSocketObject")
            assert isinstance(bl_socket, bpy.types.NodeSocketInterfaceObject)
            assert isinstance(socket, Object)
            bl_socket.description = tooltip
            if isinstance(default_value, bpy.types.Object):
                bl_socket.default_value = default_value
            return socket

        def add_boolean(
            self,
            name: str = "Boolean",
            tooltip: str = "",
            attribute_domain: str = "POINT",
            default_attribute_name: str = "",
            default_value: bool = False,
        ) -> Boolean:
            socket, bl_socket = self._add_input(name, Boolean, "NodeSocketBool")
            assert isinstance(bl_socket, bpy.types.NodeSocketInterfaceBool)
            assert isinstance(socket, Boolean)
            bl_socket.description = tooltip
            bl_socket.attribute_domain = attribute_domain
            bl_socket.default_attribute_name = default_attribute_name
            bl_socket.default_value = default_value
            return socket

        def add_float(
            self,
            name: str = "Float",
            tooltip: str = "",
            attribute_domain: str = "POINT",
            default_attribute_name: str = "",
            default_value: float = 0.0,
            min_value: float = float("-inf"),
            max_value: float = float("inf"),
        ) -> Scalar:
            socket, bl_socket = self._add_input(name, Scalar, "NodeSocketFloat")
            assert isinstance(bl_socket, bpy.types.NodeSocketInterfaceFloat)
            assert isinstance(socket, Scalar)
            bl_socket.description = tooltip
            bl_socket.attribute_domain = attribute_domain
            bl_socket.default_attribute_name = default_attribute_name
            bl_socket.default_value = default_value
            bl_socket.min_value = min_value
            bl_socket.max_value = max_value
            return socket

        def add_integer(
            self,
            name: str = "Integer",
            tooltip: str = "",
            attribute_domain: str = "POINT",
            default_attribute_name: str = "",
            default_value: int = 0,
            min_value: int = 0,
            max_value: int = 0,
        ) -> Scalar:
            socket, bl_socket = self._add_input(name, Scalar, "NodeSocketInt")
            assert isinstance(bl_socket, bpy.types.NodeSocketInterfaceInt)
            assert isinstance(socket, Scalar)
            bl_socket.description = tooltip
            bl_socket.attribute_domain = attribute_domain
            bl_socket.default_attribute_name = default_attribute_name
            bl_socket.default_value = default_value
            bl_socket.min_value = min_value
            bl_socket.max_value = max_value
            return socket

        def add_vector(
            self,
            name: str = "Vector",
            tooltip: str = "",
            attribute_domain: str = "POINT",
            default_attribute_name: str = "",
            default_value=[0.0, 0.0, 0.0],
            min_value: float = float("-inf"),
            max_value: float = float("inf"),
        ) -> Vector3:
            socket, bl_socket = self._add_input(name, Vector3, "NodeSocketVector")
            assert isinstance(bl_socket, bpy.types.NodeSocketInterfaceVector)
            assert isinstance(socket, Vector3)
            bl_socket.description = tooltip
            bl_socket.attribute_domain = attribute_domain
            bl_socket.default_attribute_name = default_attribute_name
            if len(default_value) != 3:
                raise ValueError("default_value is not an array of size 3.")
            bl_socket.default_value = default_value
            bl_socket.min_value = min_value
            bl_socket.max_value = max_value
            return socket

    class Outputs:
        """Handles adding new tree outputs to the node tree."""

        def __init__(self, bl_node_tree: bpy.types.GeometryNodeTree):
            self.bl_node_tree = bl_node_tree
            self.output_counter = 0
            self.output_node_x_position = 0.0
            self.group_output = self.bl_node_tree.nodes.new("NodeGroupOutput")

        def __shift_output_node(self, x: float) -> None:
            """Visually shifts the "Output Node" to the right for better readability."""
            if x > self.output_node_x_position:
                self.group_output.location = (x, 0.0)
                self.output_node_x_position = x

        def _add_output(self, variable: AbstractSocket) -> None:
            self.bl_node_tree.links.new(
                variable.socket_reference, self.group_output.inputs[self.output_counter]
            )
            self.output_counter += 1
            self.__shift_output_node(variable.bl_node_reference.location[0] + 200.0)

        def add_geometry(self, variable: Geometry, name: str, tooltip: str = ""):
            output = self.bl_node_tree.outputs.new("NodeSocketGeometry", name)
            output.description = tooltip
            self._add_output(variable)
            return output

        def add_boolean(
            self,
            variable: Boolean,
            name: str,
            tooltip: str = "",
            attribute_domain: str = "POINT",
            default_attribute_name: str = "",
            default_value: bool = False,
        ):
            output = self.bl_node_tree.outputs.new("NodeSocketBool", name)
            assert isinstance(output, bpy.types.NodeSocketInterfaceBool)
            output.description = tooltip
            output.attribute_domain = attribute_domain
            output.default_attribute_name = default_attribute_name
            output.default_value = default_value
            self._add_output(variable)
            return output

        def add_float(
            self,
            variable: Scalar,
            name: str,
            tooltip: str = "",
            attribute_domain: str = "POINT",
            default_attribute_name: str = "",
            default_value: float = 0.0,
            min_value: float = float("-inf"),
            max_value: float = float("inf"),
        ):
            output = self.bl_node_tree.outputs.new("NodeSocketFloat", name)
            assert isinstance(output, bpy.types.NodeSocketInterfaceFloat)
            output.description = tooltip
            output.attribute_domain = attribute_domain
            output.default_attribute_name = default_attribute_name
            output.default_value = default_value
            output.min_value = min_value
            output.max_value = max_value
            self._add_output(variable)
            return output

        def add_integer(
            self,
            variable: Scalar,
            name: str,
            tooltip: str = "",
            attribute_domain: str = "POINT",
            default_attribute_name: str = "",
            default_value: int = 0,
            min_value: int = 0,
            max_value: int = 0,
        ):
            output = self.bl_node_tree.outputs.new("NodeSocketFloat", name)
            assert isinstance(output, bpy.types.NodeSocketInterfaceFloat)
            output.description = tooltip
            output.attribute_domain = attribute_domain
            output.default_attribute_name = default_attribute_name
            output.default_value = default_value
            output.min_value = min_value
            output.max_value = max_value
            self._add_output(variable)
            return output

        def add_vector(
            self,
            variable: Vector3,
            name: str,
            tooltip: str = "",
            attribute_domain: str = "POINT",
            default_attribute_name: str = "",
            default_value=[0.0, 0.0, 0.0],
            min_value: float = float("-inf"),
            max_value: float = float("inf"),
        ):

            output = self.bl_node_tree.outputs.new("NodeSocketVector", name)
            assert isinstance(output, bpy.types.NodeSocketInterfaceVector)
            output.description = tooltip
            output.attribute_domain = attribute_domain
            output.default_attribute_name = default_attribute_name

            if len(default_value) != 3:
                raise ValueError("default_value is not an array of size 3.")

            for i in range(0, 2):
                output.default_value[i] = default_value[i]

            output.min_value = min_value
            output.max_value = max_value

            self._add_output(variable)

            return output

    class Attributes:
        """Standard input attributes for GeometryNodeTree."""

        def __init__(self, bl_node_tree: bpy.types.GeometryNodeTree):
            self.bl_node_tree = bl_node_tree

        def add_node(self, node_type_name: str) -> NodeHandle:
            bl_node = self.bl_node_tree.nodes.new(node_type_name)
            return NodeHandle(self.bl_node_tree, bl_node)

        # Built in attributes (menu 'Input'):
        @property
        def position(self) -> Vector3:
            position = self.add_node("GeometryNodeInputPosition")
            return Vector3(position, 0)

        @property
        def normal(self) -> Vector3:
            normal = self.add_node("GeometryNodeInputNormal")
            return Vector3(normal, 0)

        @property
        def radius(self) -> Scalar:
            radius = self.add_node("GeometryNodeInputRadius")
            return Scalar(radius, 0)

        @property
        def element_id(self) -> Scalar:
            element_id = self.add_node("GeometryNodeInputID")
            return Scalar(element_id, 0)

        def get_named_attribute(
            self, attribute_name: str, data_type: str = "FLOAT"
        ) -> Scalar:
            node_handle = self.add_node("GeometryNodeInputNamedAttribute")

            bl_node = node_handle.get_bl_node()
            assert isinstance(bl_node, bpy.types.GeometryNodeInputNamedAttribute)
            bl_node.data_type = data_type

            node_handle.connect_argument(0, attribute_name)

            return Scalar(node_handle, 0)

        def is_viewport(self) -> Boolean:
            is_viewport = self.add_node("GeometryNodeIsViewport")
            return Boolean(is_viewport, 0)

        @property
        def scene_time_seconds(self) -> Scalar:
            seconds_and_frames = self.add_node("GeometryNodeInputSceneTime")
            return Scalar(seconds_and_frames, 0)

        @property
        def scene_time_frame(self) -> Scalar:
            seconds_and_frames = self.add_node("GeometryNodeInputSceneTime")
            return Scalar(seconds_and_frames, 1)
