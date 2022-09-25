#!/usr/bin/python3

"""Various standard scalar math functions."""

import bpy

import builtins
from .exceptions import BlenderTypeError
from .types import AbstractSocket
from .types import Scalar
from .types import Boolean
from .types import Vector3

# ================================
# ==== Scalar math functions: ====
# ================================


def multiply_add(
    value: Scalar | float, multiplier: Scalar | float, addend: Scalar | float
) -> Scalar:
    """Performs a multiplication and addition in one operation.

    Args:
        value (Scalar | float): Value to be multiplied and added to.
        multiplier (Scalar | float): Multiplication.
        addend (Scalar | float): Gets added to the function.

    Returns:
        Scalar: Result of the operator.

    """
    return Scalar.math_operation_ternary(
        value, multiplier, addend, operation="MULTIPLY_ADD"
    )


def compare(
    value1: Scalar | float, value2: Scalar | float, epsilon: Scalar | float
) -> Scalar:
    """Checks whether two values are within epsilon of each other.

    Produces 1.0 if value1 and value2 are within epsilon of each other, and
    0.0 otherwise.

    Args:
        value1 (Scalar | float):
            First value to compare.
        value2 (Scalar | float):
            Second value to compare.
        epsilon (Scalar | float):
            The maximal difference between the two values.

    Returns:
        Scalar: Result of the operator.

    """
    return Scalar.math_operation_ternary(value1, value2, epsilon, operation="COMPARE")


def smooth_min(
    value1: Scalar | float, value2: Scalar | float, distance: Scalar | float
) -> Scalar:
    return Scalar.math_operation_ternary(
        value1, value2, distance, operation="SMOOTH_MIN"
    )


def smooth_max(
    value1: Scalar | float, value2: Scalar | float, distance: Scalar | float
) -> Scalar:
    return Scalar.math_operation_ternary(
        value1, value2, distance, operation="SMOOTH_MAX"
    )


def wrap(
    value: Scalar | float, minimum: Scalar | float, maximum: Scalar | float
) -> Scalar:
    return Scalar.math_operation_ternary(value, minimum, maximum, operation="WRAP")


def clamp(scalar: Scalar) -> Scalar:
    if not isinstance(scalar, Scalar):
        raise TypeError(
            "Expected a Scalar, but received a {}.".format(scalar.__class__)
        )

    bl_node = scalar.socket_reference.node

    if isinstance(bl_node, bpy.types.ShaderNodeMath):
        bl_node.use_clamp = True
        return scalar

    node = AbstractSocket.new_node([scalar], "ShaderNodeMath")

    bl_node = node.get_bl_node()
    if not isinstance(bl_node, bpy.types.ShaderNodeMath):
        raise BlenderTypeError(bl_node, "bpy.types.ShaderNodeMath")

    bl_node.operation = "ADD"
    bl_node.use_clamp = True

    node.connect_argument(0, scalar)
    node.connect_argument(1, 0.0)

    return Scalar(node, 0)


def log(value: Scalar | float, base: Scalar | float) -> Scalar:
    return Scalar.math_operation_binary(value, base, operation="LOGARITHM")


def sqrt(value: Scalar | float) -> Scalar:
    return Scalar.math_operation_unary(value, operation="SQRT")


def inverse_sqrt(value: Scalar | float) -> Scalar:
    return Scalar.math_operation_unary(value, operation="INVERSE_SQRT")


def exp(value: Scalar | float) -> Scalar:
    return Scalar.math_operation_unary(value, operation="EXPONENT")


# This function unfortunately overrides min() even for non-Scalar types, so we
# must restore default behavior by calling builtins.min() if we are not dealing
# with GeoScript types:

# pylint: disable=redefined-builtin
def min(arg1, *args, key=None, default=None):
    if len(args) == 0:
        return builtins.min(arg1, key=key, default=default)

    if len(args) == 1:
        if isinstance(arg1, Scalar) or isinstance(args[0], Scalar):
            return Scalar.math_operation_binary(arg1, args[0], operation="MINIMUM")

    return builtins.min(arg1, *args, key=key)


# This function unfortunately overrides min() even for non-Scalar types, so we
# must restore default behavior by calling builtins.min() if we are not dealing
# with GeoScript types:

# pylint: disable=redefined-builtin
def max(arg1, *args, key=None, default=None):
    if len(args) == 0:
        return builtins.max(arg1, key=key, default=default)

    if len(args) == 1:
        if isinstance(arg1, Scalar) or isinstance(args[0], Scalar):
            return Scalar.math_operation_binary(arg1, args[0], operation="MAXIMUM")

    return builtins.max(arg1, *args, key=key)


def sign(value: Scalar | float) -> Scalar:
    return Scalar.math_operation_unary(value, operation="SIGN")


def frac(value: Scalar | float) -> Scalar:
    return Scalar.math_operation_unary(value, operation="FRACT")


def snap(value: Scalar | float, increment: Scalar | float) -> Scalar:
    return Scalar.math_operation_binary(value, increment, operation="SNAP")


def pingpong(value: Scalar | float, scale: Scalar | float) -> Scalar:
    return Scalar.math_operation_binary(value, scale, operation="PINGPONG")


def sin(value: Scalar | float) -> Scalar:
    return Scalar.math_operation_unary(value, operation="SINE")


def cos(value: Scalar | float) -> Scalar:
    return Scalar.math_operation_unary(value, operation="COSINE")


def tan(value: Scalar | float) -> Scalar:
    return Scalar.math_operation_unary(value, operation="TANGENT")


def asin(value: Scalar | float) -> Scalar:
    return Scalar.math_operation_unary(value, operation="ARCSINE")


def acos(value: Scalar | float) -> Scalar:
    return Scalar.math_operation_unary(value, operation="ARCCOSINE")


def atan(value: Scalar | float) -> Scalar:
    return Scalar.math_operation_unary(value, operation="ARCTANGENT")


# pylint: disable=invalid-name; standard atan2 has y and x as arguments
def atan2(y: Scalar | float, x: Scalar | float) -> Scalar:
    return Scalar.math_operation_binary(y, x, operation="ARCTAN2")


def sinh(value: Scalar | float) -> Scalar:
    return Scalar.math_operation_unary(value, operation="SINH")


def cosh(value: Scalar | float) -> Scalar:
    return Scalar.math_operation_unary(value, operation="COSH")


def tanh(value: Scalar | float) -> Scalar:
    return Scalar.math_operation_unary(value, operation="TANH")


# Heaviside step function, designed after the 'step()' function from OpenGL:
def step(edge: Scalar | float, x: Scalar | float) -> Scalar:
    return Scalar.math_operation_binary(x, edge, operation="LESS_THAN")


# Mirrored heaviside step function:
def drop(edge: Scalar | float, x: Scalar | float) -> Scalar:
    return Scalar.math_operation_binary(x, edge, operation="GREATER_THAN")


# Boolean comparison:


def is_equal(
    A: Scalar | float,
    B: Scalar | float,
    epsilon: Scalar | float,
    mode: str = "ELEMENTWISE",
) -> Boolean:
    return Scalar.math_comparison(A, B, epsilon, operation="EQUAL", mode=mode)


def is_not_equal(
    A: Scalar | float,
    B: Scalar | float,
    epsilon: Scalar | float,
    mode: str = "ELEMENTWISE",
) -> Boolean:
    return Scalar.math_comparison(A, B, epsilon, operation="NOT_EQUAL", mode=mode)


def map_range(
    value: Scalar | float,
    from_min: Scalar | float,
    from_max: Scalar | float,
    to_min: Scalar | float,
    to_max: Scalar | float,
    steps: Scalar | float = 4.0,
    interpolation_type: str = "LINEAR",
) -> Scalar:
    node = AbstractSocket.add_linked_node(
        [value, from_min, from_max, to_min, to_max, steps],
        "ShaderNodeMapRange",
    )

    bl_node = node.get_bl_node()
    if not isinstance(bl_node, bpy.types.ShaderNodeMapRange):
        raise BlenderTypeError(bl_node, "bpy.types.ShaderNodeMapRange")

    bl_node.clamp = False
    bl_node.interpolation_type = interpolation_type
    bl_node.data_type = "FLOAT"

    return Scalar(node, 0)


def map_range_vector(
    value: Vector3,
    from_min: Vector3,
    from_max: Vector3,
    to_min: Vector3,
    to_max: Vector3,
    steps: Vector3 | None = None,
    interpolation_type: str = "LINEAR",
) -> Vector3:
    node = AbstractSocket.add_linked_node(
        [
            None,
            None,
            None,
            None,
            None,
            None,
            value,
            from_min,
            from_max,
            to_min,
            to_max,
            steps,
        ],
        "ShaderNodeMapRange",
    )

    bl_node = node.get_bl_node()
    if not isinstance(bl_node, bpy.types.ShaderNodeMapRange):
        raise BlenderTypeError(bl_node, "bpy.types.ShaderNodeMapRange")

    bl_node.clamp = False
    bl_node.interpolation_type = interpolation_type
    bl_node.data_type = "FLOAT_VECTOR"

    return Vector3(node, 0)
