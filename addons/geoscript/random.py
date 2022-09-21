#!/usr/bin/python3

import bpy

from .types import AbstractSocket
from .types import Scalar
from .types import Boolean
from .types import Vector3

# ================================
# ==== Randomness functions: ====
# ================================


def rand_float(
    min: Scalar | float, max: Scalar | float, id: Scalar | int, seed: Scalar | int
) -> Scalar:
    node_tree, node, layer = AbstractSocket.add_linked_node(
        [None, None, min, max, None, None, None, id, seed], "FunctionNodeRandomValue"
    )

    node.data_type = "FLOAT"

    return Scalar(node_tree, node.outputs[0], layer)


def rand_int(
    min: Scalar | int, max: Scalar | int, id: Scalar | int, seed: Scalar | int
) -> Scalar:
    node_tree, node, layer = AbstractSocket.add_linked_node(
        [None, None, None, None, min, max, None, id, seed], "FunctionNodeRandomValue"
    )

    node.data_type = "INT"

    return Scalar(node_tree, node.outputs[0], layer)


def rand_vector(
    min: Vector3, max: Vector3, id: Scalar | int, seed: Scalar | int
) -> Vector3:
    node_tree, node, layer = AbstractSocket.add_linked_node(
        [min, max, None, None, None, None, None, id, seed], "FunctionNodeRandomValue"
    )

    node.data_type = "FLOAT_VECTOR"

    return Vector3(node_tree, node.outputs[0], layer)


def rand_bool(
    probability: Scalar | float, id: Scalar | int, seed: Scalar | int
) -> Boolean:
    node_tree, node, layer = AbstractSocket.add_linked_node(
        [None, None, None, None, None, None, probability, id, seed],
        "FunctionNodeRandomValue",
    )

    node.data_type = "BOOLEAN"

    return Boolean(node_tree, node.outputs[0], layer)
