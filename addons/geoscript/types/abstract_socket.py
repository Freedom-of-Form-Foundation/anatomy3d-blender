#!/usr/bin/python3

import bpy
from typing import Type, Optional


class AbstractSocket:
    """Any type of output inside a node tree.

    This class handles the positioning and routing of new nodes in a node tree.
    This class is meant to be subclassed by socket types, such as Scalar,
    Vector3, Geometry, and so on."""

    def __init__(
        self,
        node_tree: bpy.types.NodeTree,
        socket_reference: bpy.types.NodeSocket,
        layer: int = 0,
    ):
        if not node_tree:
            node_tree = bpy.types.GeometryNodeTree()

        self.node_tree = node_tree
        self.socket_reference = socket_reference
        self.layer = layer

    @staticmethod
    def get_bl_idnames() -> list[str]:
        """Returns a list of Blender socket types that this class represents.

        Returns:
            List of strings corresponding to Blender Geometry Nodes socket
            types.
        """
        return []

    @staticmethod
    def allowed_const_types(name: str) -> None | Type[object]:
        allowed_const_types = {
            "CUSTOM": None,
            "VALUE": float,
            "INT": int,
            "BOOLEAN": bool,
            "VECTOR": None,
            "STRING": str,
            "RGBA": None,
            "SHADER": None,
            "OBJECT": None,
            "IMAGE": None,
            "GEOMETRY": None,
            "COLLECTION": None,
            "TEXTURE": None,
            "MATERIAL": None,
        }

        return allowed_const_types[name]

    @staticmethod
    def __get_node_tree(socket_list) -> bpy.types.NodeTree:
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
    def __get_outermost_layer(socket_list, default: int = 0):
        """Gets the visual layer position of rightmost AbstractSocket.

        Finds the layer index of the AbstractSocket in socket_list that is
        positioned the furthest to the right in Blender's visual node tree
        representation. The layer index helps to position the node for display
        purposes. This is purely cosmetic, and the layer index has no effect on
        the function of the nodes involved.

        Args:
            socket_list:
                A list that contains any amount of AbstractSocket. The other
                entries can be any object or value, including None, and will
                be ignored.
            default:
                The layer that this function should return if there are no
                AbstractSockets in socket_list.

        Returns:
            An int that represents the rightmost layer that an AbstractSocket
            inside socket_list is in, or the default value if there are no
            AbstractSockets inside socket_list.
        """
        max_layer = default
        for i in socket_list:
            if isinstance(i, AbstractSocket):
                max_layer = max(max_layer, i.layer)

        return max_layer

    @staticmethod
    def new_node(input_list, node_type: str = ""):
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
        max_layer = AbstractSocket.__get_outermost_layer(input_list)

        new_layer = max_layer + 1

        # Then create a new node to the right of that rightmost layer:
        new_node = node_tree.nodes.new(node_type)
        new_node.location = (200.0 * new_layer, 0.0)

        return (node_tree, new_node, new_layer)

    # DEPRECATED:
    @staticmethod
    def add_link_with_typecheck(
        socket, node: bpy.types.Node, input_index: int, type_check
    ) -> None:
        """Connect two node sockets if the type of socket matches type_check.

        Args:
            socket:
                The AbstractSocket that is to be linked.
            node:
                The Blender node that is to be linked to.
            input_index:
                The input index of node that is to be connected to. 0 refers
                to the first input of the node.
        """
        if isinstance(socket, type_check):
            input_socket = node.inputs[input_index]
            socket.node_tree.links.new(socket.socket_reference, input_socket)
        elif socket is not None:
            raise TypeError(
                "Argument 'position' (of type Vector3) doesn't"
                " support object of type {}.".format(socket.__class__)
            )

    @staticmethod
    def connect_argument(node_tree, socket, index: int, node: bpy.types.Node):
        """Connect a socket or constant to a node input.

        Args:
            socket:
                The AbstractSocket or constant value that is to be linked. Can
                be None, in which case it is skipped.
            node:
                The Blender node that is to be linked to.
            input_index:
                The input index of node that is to be connected to. 0 refers
                to the first input of the node.

        Raises:
            TypeError:
                The object in input_list cannot connect to the node's socket,
                due to being of the wrong type.
        """
        socket_type: str = node.inputs[index].type
        const_types = AbstractSocket.allowed_const_types(socket_type)

        # If the argument is an AbstractSocket, then the allowed types can be
        # found using get_allowed_link_types().
        if isinstance(socket, AbstractSocket):
            bl_idnames = socket.get_bl_idnames()

            if node.inputs[index].type in bl_idnames:
                node_tree.links.new(socket.socket_reference, node.inputs[index])
            else:
                raise TypeError(
                    "Argument {} of type {} doesn't support object"
                    " of type {}.".format(index, socket_type, socket.__class__)
                )

        # If the argument is constant, then look up whether this is allowed in
        # the global lookup table get_allowed_constant_types().
        elif const_types is not None and isinstance(socket, const_types):
            current_input = node.inputs[index]
            if isinstance(current_input, bpy.types.NodeSocketFloat):
                current_input.default_value = socket

        elif socket is not None:
            raise TypeError(
                "Argument {} of type {} doesn't support object"
                " of type {}.".format(index, socket_type, socket.__class__)
            )

    @staticmethod
    def add_linked_node(input_list, node_type: str = ""):
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
        # Create a new node:
        node_tree, node, layer = AbstractSocket.new_node(input_list, node_type)

        # Connect the arguments to the node's inputs:
        index: int = 0
        for socket in input_list:
            AbstractSocket.connect_argument(node_tree, socket, index, node)

            index = index + 1

        # The node is now complete and linked, so return:
        return (node_tree, node, layer)
