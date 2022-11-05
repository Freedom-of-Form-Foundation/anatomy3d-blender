#!/usr/bin/python3

import bpy
from typing import Optional, Sequence


class NodeHandle:
    """A wrapper around a bpy.types.Node object."""

    def __init__(
        self,
        node_tree: bpy.types.NodeTree,
        blender_node: bpy.types.Node,
    ):
        self.__node_tree = node_tree
        self.__blender_node = blender_node

    def get_bl_tree(self) -> bpy.types.NodeTree:
        return self.__node_tree

    def get_bl_node(self) -> bpy.types.Node:
        return self.__blender_node

    def get_input(self, index: int) -> bpy.types.NodeSocket:
        return self.__blender_node.inputs[index]

    def get_output(self, index: int) -> bpy.types.NodeSocket:
        return self.__blender_node.outputs[index]

    def connect_argument(
        self,
        index: int,
        socket: object,
    ) -> None:
        """Connects a socket or constant to an input of this node with type checking.

        Args:
            index:
                The input index of node that is to be connected to. 0 refers
                to the first input of the node.
            socket:
                The AbstractSocket or constant value that is to be linked. Can
                be None, in which case it is skipped.

        Raises:
            TypeError:
                The object in input_list cannot connect to the node's socket,
                due to being of the wrong type.
        """
        node = self.get_bl_node()
        tree = self.get_bl_tree()

        socket_type = node.inputs[index].type
        current_input = node.inputs[index]

        if isinstance(socket, AbstractSocket):
            bl_idnames = socket.get_bl_idnames()
            if node.inputs[index].type in bl_idnames:
                tree.links.new(socket.socket_reference, node.inputs[index])
            else:
                raise TypeError(
                    "Argument {} of type {} doesn't support object"
                    " of type {}.".format(index, socket_type, socket.__class__)
                )
        elif isinstance(socket, float):
            if isinstance(
                current_input,
                bpy.types.NodeSocketFloat
                | bpy.types.NodeSocketFloatAngle
                | bpy.types.NodeSocketFloatDistance
                | bpy.types.NodeSocketFloatFactor
                | bpy.types.NodeSocketFloatPercentage
                | bpy.types.NodeSocketFloatTime
                | bpy.types.NodeSocketFloatTimeAbsolute
                | bpy.types.NodeSocketFloatUnsigned
            ):
                current_input.default_value = socket
        elif isinstance(socket, int):
            if isinstance(
                current_input,
                bpy.types.NodeSocketInt
                | bpy.types.NodeSocketIntFactor
                | bpy.types.NodeSocketIntPercentage
                | bpy.types.NodeSocketIntUnsigned,
            ):
                current_input.default_value = socket
        elif isinstance(socket, bool):
            if isinstance(current_input, bpy.types.NodeSocketBool):
                current_input.default_value = socket
        elif isinstance(socket, str):
            if isinstance(current_input, bpy.types.NodeSocketString):
                current_input.default_value = socket
        elif socket is not None:
            raise TypeError(
                "Argument {} of type {} doesn't support object"
                " of type {}.".format(index, socket_type, socket.__class__)
            )


class AbstractSocket:
    """Any type of output inside a node tree.

    This class handles the positioning and routing of new nodes in a node tree.
    This class is meant to be subclassed by socket types, such as Scalar,
    Vector3, Geometry, and so on."""

    def __init__(
        self,
        node_handle: NodeHandle,
        output_index: int,
    ) -> None:
        # if not node_tree:
        #    node_tree = bpy.types.GeometryNodeTree()

        self.node_tree = node_handle.get_bl_tree()
        self.bl_node_reference = node_handle.get_bl_node()
        self.socket_reference = node_handle.get_output(output_index)

    @staticmethod
    def get_bl_idnames() -> list[str]:
        """Returns a list of Blender socket types that this class represents.

        Returns:
            List of strings corresponding to Blender Geometry Nodes socket
            types.
        """
        return []

    @staticmethod
    def __get_node_tree(socket_list: Sequence[object]) -> bpy.types.NodeTree:
        """Extracts the Blender node tree from a list of AbstractSockets.

        Extracts the bpy.types.GeometryNodeTree from a list of AbstractSockets,
        and ensures that all AbstractSockets in the list belong to that
        GeometryNodeTree. This prevents errors related to connecting nodes
        belonging to different node trees, which is impossible.

        Args:
            socket_list:
                A list that contains at least one AbstractSocket. The other
                entries can be any object or value, including None, and will be
                ignored.

        Returns:
            The bpy.types.GeometryNodeTree that all AbstractSockets in
            socket_list belong to.

        Raises:
            ValueError:
                Two or more AbstractSockets in socket_list belong to different
                node trees.

            TypeError:
                socket_list contains no AbstractSockets.
        """
        node_tree: Optional[bpy.types.NodeTree] = None
        for i in socket_list:
            if isinstance(i, AbstractSocket):
                if node_tree is None:
                    node_tree = i.node_tree

                if node_tree != i.node_tree:
                    raise ValueError(
                        "Attempting to perform an operation on"
                        " nodes that belong to different node trees."
                    )

        if node_tree is None:
            raise TypeError(
                "Cannot add a new node to node tree without at"
                " least one input connection."
            )

        return node_tree

    @staticmethod
    def __get_outermost_x(socket_list: Sequence[object], default: float = 0) -> float:
        """Gets the visual x position of rightmost AbstractSocket.

        Finds the x position of the AbstractSocket in socket_list that is
        positioned the furthest to the right in Blender's visual node tree
        representation. This is purely cosmetic, and the layer index has no
        effect on the function of the nodes involved.

        Args:
            socket_list:
                A list that contains any amount of AbstractSocket. The other
                entries can be any object or value, including None, and will
                be ignored.
            default:
                The x position that this function should return if there are no
                AbstractSockets in socket_list.

        Returns:
            A float that represents the x position of the rightmost Blender
            node, or the default value if there are no AbstractSockets inside
            socket_list.
        """
        max_x = default
        for i in socket_list:
            if isinstance(i, AbstractSocket):
                current_x = i.bl_node_reference.location[0]
                max_x = max(max_x, current_x)

        return max_x

    @staticmethod
    def new_node(input_list, node_type: str = "") -> NodeHandle:
        """Add a new node to the right of all input sockets.

        Args:
            input_list:
                A list that contains at least one AbstractSocket. The other
                entries can be any object or value, including None, and will be
                ignored.
            node_type:
                The name of the node type to be added. Should be the string in
                bpy.types.Node.bl_idname, where Node is the type of node
                that you want to add.

        Returns:
            A tuple containing the new bpy.types.Node and the layer index of
            the added node.
        """
        # First calculate which is the rightmost layer of the input sockets:
        node_tree = AbstractSocket.__get_node_tree(input_list)
        max_x = AbstractSocket.__get_outermost_x(input_list)

        new_x = max_x + 200.0

        # Then create a new node to the right of that rightmost layer:
        new_node = node_tree.nodes.new(node_type)
        new_node.location = (new_x, 0.0)

        return NodeHandle(node_tree, new_node)

    @staticmethod
    def add_linked_node(
        input_list: Sequence[object | None], node_type: str = ""
    ) -> NodeHandle:
        """Appends a node and connects its inputs.

        Adds a node to the node tree, checks if the input_list entries are of
        the right type, and connects the input_list to the node.

        Args:
            input_list:
                A list of arguments that will be connected to the new node. It
                must contain at least one AbstractSocket. If an entry is
                derived from AbstractSocket, it will be connected to the
                corresponding node input. If an entry is a constant value, the
                node's input will be set to that constant value. If an entry is
                None, then the node input will be skipped.
            node_type:
                The name of the node type to be added. Should be the string in
                bpy.types.Node.bl_idname, where Node is the type of node
                that you want to add.

        Returns:
            A tuple containing the new bpy.types.Node and the layer index of
            the added node.

        Raises:
            TypeError:
                The object in input_list cannot connect to the node's socket,
                due to being of the wrong type.
        """
        node_handle = AbstractSocket.new_node(input_list, node_type)
        for index, socket in enumerate(input_list):
            node_handle.connect_argument(index, socket)
        return node_handle
