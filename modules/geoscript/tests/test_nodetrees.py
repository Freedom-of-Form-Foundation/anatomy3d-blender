#!/usr/bin/python3

import pytest
import bpy
from ..nodetrees import GeometryNodeTree


def test_geometry_node_tree_class() -> None:
    """Tests whether a simple GeometryNodeTree class can correctly add an input."""
    class ExampleTree(GeometryNodeTree):
        def function(self):
            # Add new nodes to the tree:
            input1 = self.InputGeometry()

    example_tree = ExampleTree("test_function")
    bl_tree = example_tree.get_bl_tree()
    assert isinstance(bl_tree, bpy.types.GeometryNodeTree)
    inputs = bl_tree.inputs
    assert len(inputs) == 1
    first_input = inputs[0]
    assert isinstance(first_input, bpy.types.NodeSocketInterfaceStandard)
    assert first_input.type == "GEOMETRY"
    assert isinstance(first_input, bpy.types.NodeSocketInterfaceGeometry)


def add_input(example_tree: GeometryNodeTree, bpy_type: str) -> None:
    if bpy_type == "VALUE":
        example_tree.InputFloat()
    elif bpy_type == "BOOLEAN":
        example_tree.InputBoolean()
    elif bpy_type == "VECTOR":
        example_tree.InputVector()
    elif bpy_type == "OBJECT":
        example_tree.InputObject()
    elif bpy_type == "GEOMETRY":
        example_tree.InputGeometry()


test_input_types = [
    ("VALUE", bpy.types.NodeSocketInterfaceFloat),
    ("BOOLEAN", bpy.types.NodeSocketInterfaceBool),
    ("VECTOR", bpy.types.NodeSocketInterfaceVector),
    ("OBJECT", bpy.types.NodeSocketInterfaceObject),
    ("GEOMETRY", bpy.types.NodeSocketInterfaceGeometry),
]


@pytest.mark.parametrize("test_bpy_typename,test_bpy_type", test_input_types)
def test_add_input(test_bpy_typename: str, test_bpy_type: type) -> None:
    """Tests whether the input generation functions work correctly."""
    example_tree = GeometryNodeTree("test_add_input")
    add_input(example_tree, test_bpy_typename)
    bl_tree = example_tree.get_bl_tree()
    assert isinstance(bl_tree, bpy.types.GeometryNodeTree)
    inputs = bl_tree.inputs
    assert len(inputs) == 1
    first_input = inputs[0]
    assert isinstance(first_input, bpy.types.NodeSocketInterfaceStandard)
    assert first_input.type == test_bpy_typename
    assert isinstance(first_input, test_bpy_type)
