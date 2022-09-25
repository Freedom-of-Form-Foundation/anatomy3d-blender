#!/usr/bin/python3

import bpy

from .exceptions import BlenderTypeError
from .types import AbstractSocket
from .types import Scalar
from .types import Boolean
from .types import Vector3

# ================================
# ==== Randomness functions: ====
# ================================


def rand_float(
    min_value: Scalar | float,
    max_value: Scalar | float,
    id_value: Scalar | int,
    seed: Scalar | int,
) -> Scalar:
    arguments = [min_value, max_value, id_value, seed]
    node = AbstractSocket.new_node(arguments, "FunctionNodeRandomValue")

    bl_node = node.get_bl_node()
    if not isinstance(bl_node, bpy.types.FunctionNodeRandomValue):
        raise BlenderTypeError(bl_node, "bpy.types.FunctionNodeRandomValue")
    bl_node.data_type = "FLOAT"

    node.connect_argument(2, min_value)
    node.connect_argument(3, max_value)
    node.connect_argument(7, id_value)
    node.connect_argument(8, seed)

    return Scalar(node, 0)


def rand_int(
    min_value: Scalar | int,
    max_value: Scalar | int,
    id_value: Scalar | int,
    seed: Scalar | int,
) -> Scalar:
    arguments = [min_value, max_value, id_value, seed]
    node = AbstractSocket.new_node(arguments, "FunctionNodeRandomValue")

    bl_node = node.get_bl_node()
    if not isinstance(bl_node, bpy.types.FunctionNodeRandomValue):
        raise BlenderTypeError(bl_node, "bpy.types.FunctionNodeRandomValue")
    bl_node.data_type = "INT"

    node.connect_argument(4, min_value)
    node.connect_argument(5, max_value)
    node.connect_argument(7, id_value)
    node.connect_argument(8, seed)

    return Scalar(node, 0)


def rand_vector(
    min_value: Vector3, max_value: Vector3, id_value: Scalar | int, seed: Scalar | int
) -> Vector3:
    arguments = [min_value, max_value, id_value, seed]
    node = AbstractSocket.new_node(arguments, "FunctionNodeRandomValue")

    bl_node = node.get_bl_node()
    if not isinstance(bl_node, bpy.types.FunctionNodeRandomValue):
        raise BlenderTypeError(bl_node, "bpy.types.FunctionNodeRandomValue")
    bl_node.data_type = "FLOAT_VECTOR"

    node.connect_argument(0, min_value)
    node.connect_argument(1, max_value)
    node.connect_argument(7, id_value)
    node.connect_argument(8, seed)

    return Vector3(node, 0)


def rand_bool(
    probability: Scalar | float, id_value: Scalar | int, seed: Scalar | int
) -> Boolean:
    arguments = [probability, id_value, seed]
    node = AbstractSocket.new_node(arguments, "FunctionNodeRandomValue")

    bl_node = node.get_bl_node()
    if not isinstance(bl_node, bpy.types.FunctionNodeRandomValue):
        raise BlenderTypeError(bl_node, "bpy.types.FunctionNodeRandomValue")
    bl_node.data_type = "BOOLEAN"

    node.connect_argument(6, probability)
    node.connect_argument(7, id_value)
    node.connect_argument(8, seed)

    return Boolean(node, 0)
