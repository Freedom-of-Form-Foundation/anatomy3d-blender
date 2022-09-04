#!/usr/bin/python3

import bpy

from .abstract_socket import AbstractSocket
from .abstract_tensor import AbstractTensor
from .scalar import Scalar

class Vector(AbstractTensor):
    """A 3D vector object in Geoscript."""
    
    def __init__(self, node_tree: bpy.types.NodeTree = None, socket_reference: bpy.types.NodeSocket = None, layer: int = 0):
        super().__init__(node_tree, socket_reference, layer)
    
    @staticmethod
    def math_operation_unary(input, operation: str = 'ADD', use_clamp: bool = False):
        #math_node = input.node_tree.nodes.new('ShaderNodeVectorMath')
        math_node, layer = input.new_node([input], 'ShaderNodeVectorMath')
        math_node.operation = operation
        
        input.node_tree.links.new(left.socket_reference, math_node.inputs[0])
        
        return Vector(input.node_tree, math_node.outputs[0], layer)
    
    @staticmethod
    def math_operation_binary(left, right, operation: str = 'ADD', use_clamp: bool = False):
        if isinstance(right, left.__class__):
            #math_node = left.node_tree.nodes.new('ShaderNodeVectorMath')
            math_node, layer = left.new_node([left, right], 'ShaderNodeVectorMath')
            math_node.operation = operation
            
            left.node_tree.links.new(left.socket_reference, math_node.inputs[0])
            left.node_tree.links.new(right.socket_reference, math_node.inputs[1])
            
            return Vector(left.node_tree, math_node.outputs[0], layer)
        
        elif isinstance(right, float):
            #math_node = left.node_tree.nodes.new('ShaderNodeVectorMath')
            math_node, layer = left.new_node([left], 'ShaderNodeVectorMath')
            math_node.operation = operation
            math_node.inputs[1].default_value = right
            
            left.node_tree.links.new(left.socket_reference, math_node.inputs[0])
            
            return Vector(left.node_tree, math_node.outputs[0], layer)
        
        elif isinstance(left, float):
            #math_node = right.node_tree.nodes.new('ShaderNodeVectorMath')
            math_node, layer = right.new_node([right], 'ShaderNodeVectorMath')
            math_node.operation = operation
            math_node.inputs[0].default_value = left
            
            right.node_tree.links.new(right.socket_reference, math_node.inputs[1])
            
            return Vector(right.node_tree, math_node.outputs[0], layer)
        
        else:
            return NotImplemented
