#!/usr/bin/python3

import bpy

from .abstract_socket import AbstractSocket

class AbstractTensor(AbstractSocket):
    """A mathematical object on which various operations can be performed, such as a Scalar or a Vector."""
    
    def __init__(self, node_tree: bpy.types.NodeTree = None, socket_reference: bpy.types.NodeSocket = None, layer: int = 0):
        super().__init__(node_tree, socket_reference, layer)
    
    @staticmethod
    def math_operation_unary(input, operation: str = 'ADD', use_clamp: bool = False):
        return NotImplemented
    
    @staticmethod
    def math_operation_binary(left, right, operation: str = 'ADD', use_clamp: bool = False):
        return NotImplemented
    
    # Add:
    def __add__(self, other):
        return self.math_operation_binary(self, other, operation = 'ADD', use_clamp = False);
    
    def __radd__(self, other):
        return self.math_operation_binary(other, self, operation = 'ADD', use_clamp = False);
    
    # Subtract:
    def __sub__(self, other):
        return self.math_operation_binary(self, other, operation = 'SUBTRACT', use_clamp = False);
    
    def __rsub__(self, other):
        return self.math_operation_binary(other, self, operation = 'SUBTRACT', use_clamp = False);
    
    # Multiply:
    def __mul__(self, other):
        return self.math_operation_binary(self, other, operation = 'MULTIPLY', use_clamp = False);
    
    def __rmul__(self, other):
        return self.math_operation_binary(other, self, operation = 'MULTIPLY', use_clamp = False);
    
    # Divide:
    def __div__(self, other):
        return self.math_operation_binary(self, other, operation = 'DIVIDE', use_clamp = False);
    
    def __rdiv__(self, other):
        return self.math_operation_binary(other, self, operation = 'DIVIDE', use_clamp = False);
    
    def __truediv__(self, other):
        return self.math_operation_binary(self, other, operation = 'DIVIDE', use_clamp = False);
    
    def __rtruediv__(self, other):
        return self.math_operation_binary(other, self, operation = 'DIVIDE', use_clamp = False);
    
    # Modulo:
    def __mod__(self, other):
        return self.math_operation_binary(self, other, operation = 'MODULO', use_clamp = False);
    
    def __rmod__(self, other):
        return self.math_operation_binary(other, self, operation = 'MODULO', use_clamp = False);
    
    # Power:
    def __pow__(self, other):
        return self.math_operation_binary(self, other, operation = 'POWER', use_clamp = False);
    
    def __rpow__(self, other):
        return self.math_operation_binary(other, self, operation = 'POWER', use_clamp = False);
    
    # Unary operations:
    def __abs__(self):
        return self.math_operation_unary(self, other, operation = 'ABSOLUTE', use_clamp = False);
    
    def __neg__(self):
        return self.math_operation_binary(-1.0, self, operation = 'MULTIPLY', use_clamp = False);
    
    def __round__(self):
        return self.math_operation_unary(self, operation = 'ROUND', use_clamp = False);
    
    def __trunc__(self):
        return self.math_operation_unary(self, operation = 'TRUNC', use_clamp = False);
    
    def __floor__(self):
        return self.math_operation_unary(self, operation = 'FLOOR', use_clamp = False);
    
    def __ceil__(self):
        return self.math_operation_unary(self, operation = 'CEIL', use_clamp = False);


