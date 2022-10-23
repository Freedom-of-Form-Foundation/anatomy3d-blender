#!/usr/bin/python3

import bpy

from .types import NodeHandle, Geometry, Vector3, Scalar, Boolean, Object


def check_overlap(
    bl_node1: bpy.types.Node, bl_node2: bpy.types.Node, padding: float = 20.0
) -> bool:
    return (
        bl_node1.location[0] + bl_node1.width + padding >= bl_node2.location[0]
        and bl_node1.location[0] <= bl_node2.location[0] + bl_node2.width + padding
        and bl_node1.location[1] + bl_node2.height + padding >= bl_node2.location[1]
        and bl_node1.location[1] <= bl_node2.location[1] + bl_node2.height + padding
    )


class GeometryNodeTree:
    """Geoscript-specific wrapper for bpy.types.GeometryNodeTree."""

    def __init__(self, name: str):
        self.__registered_name = name

        # Get the node tree. If it doesn't yet exist, create a new tree:
        self.node_tree = bpy.data.node_groups.get(name)
        if not self.node_tree:
            self.node_tree = bpy.data.node_groups.new(name, "GeometryNodeTree")

        # Remove all content from the existing node tree:
        for node in self.node_tree.nodes:
            self.node_tree.nodes.remove(node)

        for input in self.node_tree.inputs:
            self.node_tree.inputs.remove(input)

        for output in self.node_tree.outputs:
            self.node_tree.outputs.remove(output)

        # TODO: removing the inputs and outputs of the pre-existing tree will reset all
        # parameters. This should be fixed to prevent having to redo the parameters if
        # the user changed them.

        self.input_counter = 0
        self.output_counter = 0
        self.output_layer = 0

        self.group_input = self.node_tree.nodes.new("NodeGroupInput")
        self.group_output = self.node_tree.nodes.new("NodeGroupOutput")

        self.attributes = self.GeometryNodeAttributes(self.node_tree)

        self.function()

        self.beautify_node_tree()

    def function(self) -> None:
        """The Geoscript code that represents the node tree."""
        pass

    def get_registered_name(self):
        return self.__registered_name

    def get_bl_tree(self):
        return self.node_tree

    def __shift_output_node(self, layer: int):
        """Visually shifts the "Output Node" to the right for better readability."""
        if layer > self.output_layer:
            self.group_output.location = (200.0 * layer, 0.0)
            self.output_layer = layer

    def beautify_node_tree(self) -> None:
        """Visually moves the nodes around in the node tree for better readability."""
        bl_tree = self.node_tree

        # Shift down all nodes that overlap:
        for bl_node in bl_tree.nodes:
            for other_node in bl_tree.nodes:
                if bl_node == other_node:
                    continue
                if check_overlap(bl_node, other_node) is True:
                    other_node.location[1] -= bl_node.height + 140.0

    # Adding group inputs:
    def InputGeometry(self, name: str = "Geometry") -> Geometry:
        self.node_tree.inputs.new("NodeSocketGeometry", name)

        node_handle = NodeHandle(self.node_tree, self.group_input)
        socket = Geometry(node_handle, self.input_counter)

        self.input_counter += 1

        return socket

    def InputBoolean(self, name: str = "Boolean") -> Boolean:
        self.node_tree.inputs.new("NodeSocketBool", name)

        node_handle = NodeHandle(self.node_tree, self.group_input)
        socket = Boolean(node_handle, self.input_counter)

        self.input_counter += 1

        return socket

    def InputFloat(self, name: str = "Float") -> Scalar:
        self.node_tree.inputs.new("NodeSocketFloat", name)

        node_handle = NodeHandle(self.node_tree, self.group_input)
        socket = Scalar(node_handle, self.input_counter)

        self.input_counter += 1

        return socket

    def InputVector(self, name: str = "Vector") -> Vector3:
        self.node_tree.inputs.new("NodeSocketVector", name)

        node_handle = NodeHandle(self.node_tree, self.group_input)
        socket = Vector3(node_handle, self.input_counter)

        self.input_counter += 1

        return socket

    def InputObject(self, name: str = "Object") -> Object:
        self.node_tree.inputs.new("NodeSocketObject", name)

        node_handle = NodeHandle(self.node_tree, self.group_input)
        socket = Object(node_handle, self.input_counter)

        self.input_counter += 1

        return socket

    # Adding group outputs:
    def OutputGeometry(self, variable, name: str, tooltip: str = ""):

        output = self.node_tree.outputs.new("NodeSocketGeometry", name)
        output.description = tooltip

        self.node_tree.links.new(
            variable.socket_reference, self.group_output.inputs[self.output_counter]
        )

        self.output_counter += 1

        self.__shift_output_node(variable.layer + 1)

        return output

    def OutputBoolean(
        self,
        variable,
        name: str,
        tooltip: str = "",
        attribute_domain: str = "POINT",
        default_attribute_name: str = "",
        default_value: bool = False,
    ):

        output = self.node_tree.outputs.new("NodeSocketFloat", name)
        output.description = tooltip
        output.attribute_domain = attribute_domain
        output.default_attribute_name = default_attribute_name
        output.default_value = default_value

        self.node_tree.links.new(
            variable.socket_reference, self.group_output.inputs[self.output_counter]
        )

        self.output_counter += 1

        self.__shift_output_node(variable.layer + 1)

        return output

    def OutputFloat(
        self,
        variable,
        name: str,
        tooltip: str = "",
        attribute_domain: str = "POINT",
        default_attribute_name: str = "",
        default_value: float = 0.0,
        min_value: float = float("-inf"),
        max_value: float = float("inf"),
    ):

        output = self.node_tree.outputs.new("NodeSocketFloat", name)
        output.description = tooltip
        output.attribute_domain = attribute_domain
        output.default_attribute_name = default_attribute_name
        output.default_value = default_value
        output.min_value = min_value
        output.max_value = max_value

        self.node_tree.links.new(
            variable.socket_reference, self.group_output.inputs[self.output_counter]
        )

        self.output_counter += 1

        self.__shift_output_node(variable.layer + 1)

        return output

    def OutputVector(
        self,
        variable,
        name: str,
        tooltip: str = "",
        attribute_domain: str = "POINT",
        default_attribute_name: str = "",
        default_value=[0.0, 0.0, 0.0],
        min_value: float = float("-inf"),
        max_value: float = float("inf"),
    ):

        output = self.node_tree.outputs.new("NodeSocketVector", name)
        output.description = tooltip
        output.attribute_domain = attribute_domain
        output.default_attribute_name = default_attribute_name

        if len(default_value) != 3:
            raise ValueError("default_value is not an array of size 3.")

        for i in range(0, 2):
            output.default_value[i] = default_value[i]

        output.min_value = min_value
        output.max_value = max_value

        self.node_tree.links.new(
            variable.socket_reference, self.group_output.inputs[self.output_counter]
        )

        self.output_counter += 1

        self.__shift_output_node(variable.layer + 1)

        return output

    class GeometryNodeAttributes:
        """Standard input attributes for GeometryNodeTree"""

        def __init__(self, bl_node_tree: bpy.types.GeometryNodeTree):
            self.bl_node_tree = bl_node_tree

        def add_node(self, node_type_name: str, layer: int = 0) -> NodeHandle:
            bl_node = self.bl_node_tree.nodes.new(node_type_name)
            return NodeHandle(self.bl_node_tree, bl_node, layer)

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
