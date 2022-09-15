#!/usr/bin/python3

import bpy

class AbstractSocket():
    """Any type of output inside a node tree.
    
    This class handles the positioning and routing of new nodes in a node tree.
    This class is meant to be subclassed by socket types, such as Scalar,
    Vector3, Geometry, and so on."""
    
    def __init__(self,
                 node_tree: bpy.types.NodeTree = None,
                 socket_reference: bpy.types.NodeSocket = None,
                 layer: int = 0):
        if not node_tree:
            node_tree = bpy.types.GeometryNodeTree()
            
        self.node_tree = node_tree
        self.socket_reference = socket_reference
        self.layer = layer
    
    @staticmethod
    def __get_node_tree(socket_list) -> bpy.types.GeometryNodeTree:
        """Extracts the Blender node tree from a list of AbstractSockets.
        
        Extracts the bpy.types.GeometryNodeTree from a list of AbstractSockets,
        and ensures that all AbstractSockets in the list belong to
        that GeometryNodeTree. This prevents errors related to connecting nodes
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
        node_tree: bpy.types.GeometryNodeTree = None
        for i in socket_list:
            if isinstance(i, AbstractSocket):
                if node_tree == None:
                    node_tree = i.node_tree
                
                if node_tree != i.node_tree:
                    raise ValueError("Attempting to perform an operation on"
                        " nodes that belong to different node trees.")

        if node_tree is None:
            raise TypeError("Cannot add a new node to node tree without at"
                " least one input connection.")
        
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
    def new_node(input_list, node_type: str = ''):
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
        
        return (new_node, new_layer)
    
    @staticmethod
    def add_link_with_typecheck(
            socket,
            node: bpy.types.Node,
            input_index: int,
            type_check) -> None:
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
            raise TypeError("Argument 'position' (of type Vector3) doesn't"
                " support object of type {}.".format(socket.__class__))

