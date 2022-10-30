#!/usr/bin/python3

import pytest
import bpy
from .. import math as g
from ..nodetrees import GeometryNodeTree


test_unary_operations = [
    (g.sqrt, "SQRT"),
    (g.inverse_sqrt, "INVERSE_SQRT"),
    (g.exp, "EXPONENT"),
    (g.sign, "SIGN"),
    (g.fract, "FRACT"),
    (g.sin, "SINE"),
    (g.cos, "COSINE"),
    (g.tan, "TANGENT"),
    (g.asin, "ARCSINE"),
    (g.acos, "ARCCOSINE"),
    (g.atan, "ARCTANGENT"),
    (g.sinh, "SINH"),
    (g.cosh, "COSH"),
    (g.tanh, "TANH"),
]


test_binary_operations = [
    (g.log, "LOGARITHM"),
    (g.power, "POWER"),
    (g.minimum, "MINIMUM"),
    (g.maximum, "MAXIMUM"),
    (g.snap, "SNAP"),
    (g.pingpong, "PINGPONG"),
    (g.atan2, "ARCTAN2"),
]


test_swapped_operations = [
    (g.step, "LESS_THAN"),      # Swapped meaning: greater than or equal to.
    (g.drop, "GREATER_THAN"),   # Swapped meaning: smaller than or equal to.
]


test_tertiary_operations = [
    (g.multiply_add, "MULTIPLY_ADD"),
    (g.compare, "COMPARE"),
    (g.smooth_min, "SMOOTH_MIN"),
    (g.smooth_max, "SMOOTH_MAX"),
    (g.wrap, "WRAP"),
]


@pytest.mark.parametrize("test_function,test_operation_name", test_tertiary_operations)
def test_tertiary(test_function, test_operation_name: str):
    tree = GeometryNodeTree("test_add_input")
    input1 = tree.InputFloat()
    input2 = tree.InputFloat()
    input3 = tree.InputFloat()
    output = test_function(input1, input2, input3)
    # Check if the sockets are linked:
    bl_node = output.socket_reference.node
    assert isinstance(bl_node, bpy.types.ShaderNodeMath)
    assert bl_node.operation == test_operation_name
    assert bl_node.inputs[0].is_linked
    assert bl_node.inputs[1].is_linked
    assert bl_node.inputs[2].is_linked
    # Check if the sockets link correctly:
    group_inputs = tree.node_tree.nodes["Group Input"].outputs
    assert isinstance(bl_node.inputs[0].links, tuple)
    assert bl_node.inputs[0].links[0].from_socket == group_inputs[0]
    assert isinstance(bl_node.inputs[1].links, tuple)
    assert bl_node.inputs[1].links[0].from_socket == group_inputs[1]
    assert isinstance(bl_node.inputs[2].links, tuple)
    assert bl_node.inputs[2].links[0].from_socket == group_inputs[2]


@pytest.mark.parametrize("test_function,test_operation_name", test_binary_operations)
def test_binary(test_function, test_operation_name: str):
    tree = GeometryNodeTree("test_add_input")
    input1 = tree.InputFloat()
    input2 = tree.InputFloat()
    output = test_function(input1, input2)
    # Check if the sockets are linked:
    bl_node = output.socket_reference.node
    assert isinstance(bl_node, bpy.types.ShaderNodeMath)
    assert bl_node.operation == test_operation_name
    assert bl_node.inputs[0].is_linked
    assert bl_node.inputs[1].is_linked
    assert not bl_node.inputs[2].is_linked
    # Check if the sockets link correctly:
    group_inputs = tree.node_tree.nodes["Group Input"].outputs
    assert isinstance(bl_node.inputs[0].links, tuple)
    assert bl_node.inputs[0].links[0].from_socket == group_inputs[0]
    assert isinstance(bl_node.inputs[1].links, tuple)
    assert bl_node.inputs[1].links[0].from_socket == group_inputs[1]


@pytest.mark.parametrize("test_function,test_operation_name", test_swapped_operations)
def test_swapped_binary(test_function, test_operation_name: str):
    tree = GeometryNodeTree("test_add_input")
    input1 = tree.InputFloat()
    input2 = tree.InputFloat()
    output = test_function(input1, input2)
    # Check if the sockets are linked:
    bl_node = output.socket_reference.node
    assert isinstance(bl_node, bpy.types.ShaderNodeMath)
    assert bl_node.operation == test_operation_name
    assert bl_node.inputs[0].is_linked
    assert bl_node.inputs[1].is_linked
    assert not bl_node.inputs[2].is_linked
    # Check if the sockets link correctly:
    group_inputs = tree.node_tree.nodes["Group Input"].outputs
    assert isinstance(bl_node.inputs[0].links, tuple)
    assert bl_node.inputs[0].links[0].from_socket == group_inputs[1]
    assert isinstance(bl_node.inputs[1].links, tuple)
    assert bl_node.inputs[1].links[0].from_socket == group_inputs[0]


@pytest.mark.parametrize("test_function,test_operation_name", test_unary_operations)
def test_unary(test_function, test_operation_name: str):
    tree = GeometryNodeTree("test_add_input")
    input1 = tree.InputFloat()
    output = test_function(input1)
    # Check if the sockets are linked:
    bl_node = output.socket_reference.node
    assert isinstance(bl_node, bpy.types.ShaderNodeMath)
    assert bl_node.operation == test_operation_name
    assert bl_node.inputs[0].is_linked
    assert not bl_node.inputs[1].is_linked
    assert not bl_node.inputs[2].is_linked
    # Check if the sockets link correctly:
    group_inputs = tree.node_tree.nodes["Group Input"].outputs
    assert isinstance(bl_node.inputs[0].links, tuple)
    assert bl_node.inputs[0].links[0].from_socket == group_inputs[0]
