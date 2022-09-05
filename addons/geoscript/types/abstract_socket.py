#!/usr/bin/python3

import bpy

class AbstractSocket():
    """Any type of output inside a node tree. This class handles the positioning and routing
    of new nodes in a node tree."""
    
    def __init__(self, node_tree: bpy.types.NodeTree = None, socket_reference: bpy.types.NodeSocket = None, layer: int = 0):
        if not node_tree:
            node_tree = bpy.types.GeometryNodeTree()
            
        self.node_tree = node_tree
        self.socket_reference = socket_reference
        self.layer = layer
    
    @staticmethod
    def new_node(input_list, node_type: str = ''):
        """Add a new node to the right of all input sockets."""
        
        # First calculate which is the rightmost layer of the input sockets:
        max_layer = 0
        for socket in input_list:
            if socket is None:
                continue
            
            if not isinstance(socket, AbstractSocket):
                raise TypeError("Socket inside socket list is not an instance of AbstractSocket, but of {}. This is a bug, please report to the developers.".format(socket.__class__))
            
            max_layer = max(max_layer, socket.layer)
        
        new_layer = max_layer + 1
        
        # Then create a new node to the right of that rightmost layer:
        new_node = input_list[0].node_tree.nodes.new(node_type)
        new_node.location = (200.0 * new_layer, 0.0)
        
        return (new_node, new_layer)
    
    @staticmethod
    def add_link_with_typecheck(socket, node: bpy.types.Node, input_index: int, type_check):
        if isinstance(socket, type_check):
            socket.node_tree.links.new(socket.socket_reference, node.inputs[input_index])
        elif socket is not None:
            raise TypeError("Argument 'position' (of type Vector3) doesn't support object of type {}.".format(socket.__class__))
