#!/usr/bin/python3

import bpy

from .types import AbstractSocket
from .types import Scalar
from .types import Boolean
from .types import Vector3
import builtins

# ================================
# ==== Scalar math functions: ====
# ================================

def multiply_add(value, multiplier, addend):
    return Scalar.math_operation_ternary(value, multiplier, addend, operation = 'MULTIPLY_ADD')

def compare(value1, value2, epsilon):
    return Scalar.math_operation_ternary(value1, value2, epsilon, operation = 'COMPARE')

def smooth_min(value1, value2, distance):
    return Scalar.math_operation_ternary(value1, value2, distance, operation = 'SMOOTH_MIN')

def smooth_max(value1, value2, distance):
    return Scalar.math_operation_ternary(value1, value2, distance, operation = 'SMOOTH_MAX')

def wrap(value, min, max):
    return Scalar.math_operation_ternary(value, min, max, operation = 'WRAP')

def clamp(scalar):
    if not isinstance(scalar, Scalar):
        return TypeError("Expected a Scalar, but received a {}.".format(scalar.__class__))
    
    node = scalar.socket_reference.node
    
    if hasattr(node, 'use_clamp'):
        node.use_clamp = True
        return scalar
    elif hasattr(node, 'clamp'):
        node.clamp = True
        return scalar
    else:
        math_node, layer = scalar.new_node([scalar], 'ShaderNodeMath')
        math_node.operation = 'ADD'
        math_node.use_clamp = True
        math_node.inputs[1].default_value = 0.0
        
        scalar.node_tree.links.new(scalar.socket_reference, math_node.inputs[0])
        
        return Scalar(scalar.node_tree, math_node.outputs[0], layer)


def log(value, base):
    return Scalar.math_operation_binary(value, base, operation = 'LOGARITHM')

def sqrt(value):
    return Scalar.math_operation_unary(value, operation = 'SQRT')

def inverse_sqrt(value):
    return Scalar.math_operation_unary(value, operation = 'INVERSE_SQRT')

def exp(value):
    return Scalar.math_operation_unary(value, operation = 'EXPONENT')

# This function unfortunately overrides min() even for non-Scalar types, so we must restore
# default behavior by calling builtins.min() if we are not dealing with GeoScript types:
def min(arg1, *args, key=None, default=None):
    if len(args) == 0:
        return builtins.min(arg1, key=key, default=default)
    
    if len(args) == 1:
        if isinstance(arg1, Scalar) or isinstance(args[0], Scalar):
            return Scalar.math_operation_binary(arg1, args[0], operation = 'MINIMUM')
    
    return builtins.min(arg1, *args, key=key)

# This function unfortunately overrides max() even for non-Scalar types, so we must restore
# default behavior by calling builtins.max() if we are not dealing with GeoScript types:
def max(arg1, *args, key=None, default=None):
    if len(args) == 0:
        return builtins.max(arg1, key=key, default=default)
    
    if len(args) == 1:
        if isinstance(arg1, Scalar) or isinstance(args[0], Scalar):
            return Scalar.math_operation_binary(arg1, args[0], operation = 'MAXIMUM')
    
    return builtins.max(arg1, *args, key=key)

def sign(value):
    return Scalar.math_operation_unary(value, operation = 'SIGN')

def frac(value):
    return Scalar.math_operation_unary(value, operation = 'FRACT')

def snap(value, increment):
    return Scalar.math_operation_binary(value, increment, operation = 'SNAP')

def pingpong(value, scale):
    return Scalar.math_operation_binary(value, scale, operation = 'PINGPONG')

def sin(value):
    return Scalar.math_operation_unary(value, operation = 'SINE')

def cos(value):
    return Scalar.math_operation_unary(value, operation = 'COSINE')

def tan(value):
    return Scalar.math_operation_unary(value, operation = 'TANGENT')

def asin(value):
    return Scalar.math_operation_unary(value, operation = 'ARCSINE')

def acos(value):
    return Scalar.math_operation_unary(value, operation = 'ARCCOSINE')

def atan(value):
    return Scalar.math_operation_unary(value, operation = 'ARCTANGENT')

def atan2(y, x):
    return Scalar.math_operation_binary(y, x, operation = 'ARCTAN2')

def sinh(value):
    return Scalar.math_operation_unary(value, operation = 'SINH')

def cosh(value):
    return Scalar.math_operation_unary(value, operation = 'COSH')

def tanh(value):
    return Scalar.math_operation_unary(value, operation = 'TANH')
    
# Heaviside step function, designed after the 'step()' function from OpenGL:
def step(edge, x):
    return self.math_operation_binary(x, edge, operation = 'LESS_THAN')

# Mirrored heaviside step function:
def drop(edge, x):
    return self.math_operation_binary(x, edge, operation = 'GREATER_THAN')

# Boolean comparison:
def is_equal(A, B, epsilon, mode: str = 'ELEMENTWISE') -> Boolean:
    if isinstance(A, float):
        return B.math_comparison(A, B, epsilon, operation = 'EQUAL', mode = mode)
    else:
        return A.math_comparison(A, B, epsilon, operation = 'EQUAL', mode = mode)

def is_not_equal(A, B, epsilon, mode: str = 'ELEMENTWISE') -> Boolean:
    if isinstance(A, float):
        return B.math_comparison(A, B, epsilon, operation = 'NOT_EQUAL', mode = mode)
    else:
        return A.math_comparison(A, B, epsilon, operation = 'NOT_EQUAL', mode = mode)

def map_range(
        value: Scalar | float,
        from_min: Scalar | float,
        from_max: Scalar | float,
        to_min: Scalar | float,
        to_max: Scalar | float,
        steps: Scalar | float = 4.0,
        interpolation_type: str = 'LINEAR') -> Scalar:
    node_tree, node, layer = AbstractSocket.add_linked_node(
        [value, from_min, from_max, to_min, to_max, steps],
        'ShaderNodeMapRange')
    
    node.clamp = False
    node.interpolation_type = interpolation_type
    node.data_type = 'FLOAT'
    
    return Scalar(node_tree, node.outputs[0], layer)

def map_range_vector(
        value: Vector3,
        from_min: Vector3,
        from_max: Vector3,
        to_min: Vector3,
        to_max: Vector3,
        steps: Vector3 | None = None,
        interpolation_type: str = 'LINEAR') -> Scalar:
    node_tree, node, layer = AbstractSocket.add_linked_node(
        [None, None, None, None, None, None,
            value, from_min, from_max, to_min, to_max, steps],
        'ShaderNodeMapRange')
    
    node.clamp = False
    node.interpolation_type = interpolation_type
    node.data_type = 'FLOAT_VECTOR'
    
    return Scalar(node_tree, node.outputs[0], layer)



