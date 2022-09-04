#!/usr/bin/python3

import bpy

from .abstract_socket import AbstractSocket
from .abstract_tensor import AbstractTensor
from .boolean import Boolean

class Scalar(AbstractTensor):
    """A scalar type within a Geoscript, which acts like float."""
    
    def __init__(self, node_tree: bpy.types.NodeTree = None, socket_reference: bpy.types.NodeSocket = None, layer: int = 0):
        super().__init__(node_tree, socket_reference, layer)
    
    @staticmethod
    def math_operation_unary(input, operation: str = 'ADD', use_clamp: bool = False):
        math_node, layer = input.new_node([input], 'ShaderNodeMath')
        math_node.operation = operation
        math_node.use_clamp = use_clamp
        
        input.node_tree.links.new(left.socket_reference, math_node.inputs[0])
        
        return Scalar(input.node_tree, math_node.outputs[0], layer)
    
    @staticmethod
    def math_operation_binary(left, right, operation: str = 'ADD', use_clamp: bool = False):
        if isinstance(right, left.__class__):
            math_node, layer = left.new_node([left, right], 'ShaderNodeMath')
            math_node.operation = operation
            math_node.use_clamp = use_clamp
            
            left.node_tree.links.new(left.socket_reference, math_node.inputs[0])
            left.node_tree.links.new(right.socket_reference, math_node.inputs[1])
            
            return Scalar(left.node_tree, math_node.outputs[0], layer)
        
        elif isinstance(right, float):
            math_node, layer = left.new_node([left], 'ShaderNodeMath')
            math_node.operation = operation
            math_node.use_clamp = use_clamp
            math_node.inputs[1].default_value = right
            
            left.node_tree.links.new(left.socket_reference, math_node.inputs[0])
            
            return Scalar(left.node_tree, math_node.outputs[0], layer)
        
        elif isinstance(left, float):
            math_node, layer = right.new_node([right], 'ShaderNodeMath')
            math_node.operation = operation
            math_node.use_clamp = use_clamp
            math_node.inputs[0].default_value = left
            
            right.node_tree.links.new(right.socket_reference, math_node.inputs[1])
            
            return Scalar(right.node_tree, math_node.outputs[0], layer)
        
        else:
            return NotImplemented
    
    @staticmethod
    def math_operation_ternary(left, middle, right, operation: str = 'MULTIPLY_ADD', use_clamp: bool = False):
        socket_list = []
        if isinstance(left, Scalar):
            socket_list.append(left)
        
        if isinstance(middle, Scalar):
            socket_list.append(middle)
        
        if isinstance(right, Scalar):
            socket_list.append(right)
        
        if len(socket_list) == 0:
            raise ValueError("Ternary operator applied on non-Scalar types {}, {} and {}.".format(left.__class__, middle.__class__, right.__class__))
        
        math_node, layer = left.new_node(socket_list, 'ShaderNodeMath')
        math_node.operation = operation
        math_node.use_clamp = use_clamp
        
        if isinstance(left, Scalar):
            left.node_tree.links.new(left.socket_reference, math_node.inputs[0])
        elif isinstance(left, float):
            math_node.inputs[0].default_value = left
        
        if isinstance(middle, Scalar):
            middle.node_tree.links.new(middle.socket_reference, math_node.inputs[1])
        elif isinstance(middle, float):
            math_node.inputs[1].default_value = middle
        
        if isinstance(right, Scalar):
            right.node_tree.links.new(right.socket_reference, math_node.inputs[2])
        elif isinstance(right, float):
            math_node.inputs[2].default_value = right
        
        return Scalar(socket_list[0].node_tree, math_node.outputs[0], layer)
    
    @staticmethod
    def math_comparison(left, right, epsilon, operation: str = 'LESS_THAN', mode = 'ELEMENT'):
        socket_list = []
        if isinstance(left, Scalar):
            socket_list.append(left)
        
        if isinstance(right, Scalar):
            socket_list.append(right)
        
        if isinstance(epsilon, Scalar):
            socket_list.append(epsilon)
        
        if len(socket_list) == 0:
            raise ValueError("Ternary operator applied on non-Scalar types {}, {} and {}.".format(left.__class__, right.__class__, epsilon.__class__))
        
        math_node, layer = left.new_node(socket_list, 'FunctionNodeCompare')
        math_node.operation = operation
        math_node.data_type = 'FLOAT'
        if hasattr(math_node, 'mode'):
            math_node.mode = mode
        
        if isinstance(left, Scalar):
            left.node_tree.links.new(left.socket_reference, math_node.inputs[0])
        elif isinstance(left, float):
            math_node.inputs[0].default_value = left
        
        if isinstance(right, Scalar):
            right.node_tree.links.new(right.socket_reference, math_node.inputs[1])
        elif isinstance(right, float):
            math_node.inputs[1].default_value = right
        
        if isinstance(epsilon, Scalar):
            epsilon.node_tree.links.new(epsilon.socket_reference, math_node.inputs[2])
        elif isinstance(epsilon, float):
            math_node.inputs[2].default_value = epsilon
        
        return Boolean(socket_list[0].node_tree, math_node.outputs[0], layer)
    
    
    def __lt__(self, other):
        return self.math_comparison(self, other, None, operation = 'LESS_THAN')
    
    def __gt__(self, other):
        return self.math_comparison(self, other, None, operation = 'GREATER_THAN')
    
    def __le__(self, other):
        return self.math_comparison(self, other, None, operation = 'LESS_EQUAL')
    
    def __ge__(self, other):
        return self.math_comparison(self, other, None, operation = 'GREATER_EQUAL')
    
    def to_radians(self, value):
        return Scalar.math_operation_unary(value, operation = 'RADIANS')
    
    def to_degrees(self, value):
        return Scalar.math_operation_unary(value, operation = 'DEGREES')
    

    
