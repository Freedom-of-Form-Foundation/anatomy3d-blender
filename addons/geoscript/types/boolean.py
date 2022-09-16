#!/usr/bin/python3

import bpy

from .abstract_socket import AbstractSocket

class Boolean(AbstractSocket):
    """A mathematics operation in a Geometry Node tree. Maps to a "Math" node."""
    
    def __init__(
            self,
            node_tree: bpy.types.NodeTree = None,
            socket_reference: bpy.types.NodeSocket = None,
            layer: int = 0):
        super().__init__(node_tree, socket_reference, layer)
    
    @staticmethod
    def get_bl_idnames():
        """Returns a list of Blender socket types that this class represents.
        
        Returns:
            List of strings corresponding to Blender Geometry Nodes socket
            types.
        """
        return ['BOOLEAN']
    
    @staticmethod
    def math_operation_unary(input, operation: str = 'ADD'):
        #math_node = input.node_tree.nodes.new('ShaderNodeMath')
        math_node, layer = input.new_node([input], 'FunctionNodeBooleanMath')
        math_node.operation = operation
        
        input.node_tree.links.new(left.socket_reference, math_node.inputs[0])
        
        return Boolean(input.node_tree, math_node.outputs[0], layer)
    
    @staticmethod
    def math_operation_binary(left, right, operation: str = 'ADD'):
        if isinstance(right, left.__class__):
            #math_node = left.node_tree.nodes.new('ShaderNodeMath')
            math_node, layer = left.new_node([left, right], 'FunctionNodeBooleanMath')
            math_node.operation = operation
            
            left.node_tree.links.new(left.socket_reference, math_node.inputs[0])
            left.node_tree.links.new(right.socket_reference, math_node.inputs[1])
            
            return Boolean(left.node_tree, math_node.outputs[0], layer)
        
        elif isinstance(right, bool):
            #math_node = left.node_tree.nodes.new('ShaderNodeMath')
            math_node, layer = left.new_node([left], 'FunctionNodeBooleanMath')
            math_node.operation = operation
            math_node.inputs[1].default_value = right
            
            left.node_tree.links.new(left.socket_reference, math_node.inputs[0])
            
            return Boolean(left.node_tree, math_node.outputs[0], layer)
        
        elif isinstance(left, bool):
            #math_node = right.node_tree.nodes.new('ShaderNodeMath')
            math_node, layer = right.new_node([right], 'FunctionNodeBooleanMath')
            math_node.operation = operation
            math_node.inputs[0].default_value = left
            
            right.node_tree.links.new(right.socket_reference, math_node.inputs[1])
            
            return Boolean(right.node_tree, math_node.outputs[0], layer)
        
        else:
            return NotImplemented
    
    # And:
    def __and__(self, other):
        return self.math_operation_binary(self, other, operation = 'AND')
    
    def __rand__(self, other):
        return self.math_operation_binary(other, self, operation = 'AND')
    
    # Or:
    def __or__(self, other):
        return self.math_operation_binary(self, other, operation = 'OR')
    
    def __ror__(self, other):
        return self.math_operation_binary(other, self, operation = 'OR')
    
    # Xor:
    def __xor__(self, other):
        return self.math_operation_binary(self, other, operation = 'XOR')
    
    def __rxor__(self, other):
        return self.math_operation_binary(other, self, operation = 'XOR')
    
    def __ne__(self, other):
        return self.math_operation_binary(self, other, operation = 'XOR')
    
    # Not:
    def __invert__(self, other):
        return self.math_operation_binary(self, other, operation = 'NOT')
    
    def __rinvert__(self, other):
        return self.math_operation_binary(other, self, operation = 'NOT')
    
    # Equal:
    def __eq__(self, other):
        return self.math_operation_binary(self, other, operation = 'XNOR')
    
    # Subtract:
    def __sub__(self, other):
        return self.math_operation_binary(self, other, operation = 'NIMPLY')

