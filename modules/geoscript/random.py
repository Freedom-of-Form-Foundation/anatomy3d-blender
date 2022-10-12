#!/usr/bin/python3

"""Functions for generating Uniform and Bernoulli distributions in GeoScript."""

import bpy

from .types import AbstractSocket, Scalar, Boolean, Vector3


def rand_float(
    min_value: Scalar | float,
    max_value: Scalar | float,
    id_value: Scalar | int,
    seed: Scalar | int,
) -> Scalar:
    """Uniform floating point random distribution between min_value and max_value.

    Returns a field with random values uniformly distributed in
    the domain [min_value, max_value].

    Args:
        min_value: The smallest value it can randomly output.
        max_value: The largest value it can randomly output.
        id_value: The index of the elements in a field.
        seed: The randomness seed.

    Returns:
        A scalar field randomly distributed on [min_value, max_value].

    """
    arguments = [min_value, max_value, id_value, seed]
    node = AbstractSocket.new_node(arguments, "FunctionNodeRandomValue")

    bl_node = node.get_bl_node()
    assert isinstance(bl_node, bpy.types.FunctionNodeRandomValue)
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
    """Uniform integer random distribution between min_value and max_value.

    Returns a field with random values uniformly distributed in
    the domain [min_value, max_value].

    Args:
        min_value: The smallest value it can randomly output.
        max_value: The largest value it can randomly output.
        id_value: The index of the elements in a field.
        seed: The randomness seed.

    Returns:
        An integer field randomly distributed on [min_value, max_value].

    """
    arguments = [min_value, max_value, id_value, seed]
    node = AbstractSocket.new_node(arguments, "FunctionNodeRandomValue")

    bl_node = node.get_bl_node()
    assert isinstance(bl_node, bpy.types.FunctionNodeRandomValue)
    bl_node.data_type = "INT"

    node.connect_argument(4, min_value)
    node.connect_argument(5, max_value)
    node.connect_argument(7, id_value)
    node.connect_argument(8, seed)

    return Scalar(node, 0)


def rand_vector(
    min_value: Vector3, max_value: Vector3, id_value: Scalar | int, seed: Scalar | int
) -> Vector3:
    """Elementwise uniform random distribution between min_value and max_value.

    Returns a field with random values uniformly distributed in
    the domain [min_value, max_value], also randomizing the elements in the 3D
    vector. It is therefore equivalent to generating three random scalar fields
    at the same time.

    Args:
        min_value: The smallest value it can randomly output.
        max_value: The largest value it can randomly output.
        id_value: The index of the elements in a field.
        seed: The randomness seed.

    Returns:
        A vector field where the vector is uniformly distributed on the 3D
        domain cube [min_value, max_value].

    """
    arguments = [min_value, max_value, id_value, seed]
    node = AbstractSocket.new_node(arguments, "FunctionNodeRandomValue")

    bl_node = node.get_bl_node()
    assert isinstance(bl_node, bpy.types.FunctionNodeRandomValue)
    bl_node.data_type = "FLOAT_VECTOR"

    node.connect_argument(0, min_value)
    node.connect_argument(1, max_value)
    node.connect_argument(7, id_value)
    node.connect_argument(8, seed)

    return Vector3(node, 0)


def rand_bool(
    probability: Scalar | float, id_value: Scalar | int, seed: Scalar | int
) -> Boolean:
    """Bernoulli distribution, returning a Boolean field.

    Returns a field that has elements that are True with probability `probability`
    and False with probability `(1 - probability)`.

    Args:
        probability: The chance of randomly generating a 'True' value.
        id_value: The index of the elements in a field.
        seed: The randomness seed.

    Returns:
        A boolean field that is randomly True or False.

    """
    arguments = [probability, id_value, seed]
    node = AbstractSocket.new_node(arguments, "FunctionNodeRandomValue")

    bl_node = node.get_bl_node()
    assert isinstance(bl_node, bpy.types.FunctionNodeRandomValue)
    bl_node.data_type = "BOOLEAN"

    node.connect_argument(6, probability)
    node.connect_argument(7, id_value)
    node.connect_argument(8, seed)

    return Boolean(node, 0)
