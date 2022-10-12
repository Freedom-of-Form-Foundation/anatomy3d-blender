#!/usr/bin/python3

"""Various standard scalar math functions."""

import bpy

from .types import AbstractSocket, Scalar, Boolean, Vector3


def multiply_add(
    value: Scalar | float, multiplier: Scalar | float, addend: Scalar | float
) -> Scalar:
    """Performs a multiplication and addition in one operation.

    Args:
        value: Value to be multiplied and added to.
        multiplier: Multiplication.
        addend: Gets added to the function.

    Returns:
        Result of the operator.

    """
    return Scalar.math_operation_ternary(
        value, multiplier, addend, operation="MULTIPLY_ADD"
    )


def compare(
    value1: Scalar | float, value2: Scalar | float, epsilon: Scalar | float
) -> Scalar:
    """Checks whether two values are within `epsilon` of each other.

    Outputs 1.0 if the difference between the two input values is less than
    or equal to `epsilon`.

    Args:
        value1: First value to compare.
        value2: Second value to compare.
        epsilon: The maximal difference between the two values.

    Returns:
        0.0 if the difference between the two input values is larger than
        `epsilon`, 1.0 if the difference between the two input values is
        less than or equal to `epsilon`.

    """
    return Scalar.math_operation_ternary(value1, value2, epsilon, operation="COMPARE")


def smooth_min(
    value1: Scalar | float, value2: Scalar | float, distance: Scalar | float
) -> Scalar:
    """Smooth and differentiable approximation to the `min()` function.

    Blender references https://en.wikipedia.org/wiki/Smooth_maximum for
    additional explanation.

    Args:
        value1: First value to compare.
        value2: Second value to compare.
        distance: Modulates the smoothness of the approximation.

    Returns:
        The approximated minimum.

    """
    return Scalar.math_operation_ternary(
        value1, value2, distance, operation="SMOOTH_MIN"
    )


def smooth_max(
    value1: Scalar | float, value2: Scalar | float, distance: Scalar | float
) -> Scalar:
    """Smooth and differentiable approximation to the `max()` function.

    Blender references https://en.wikipedia.org/wiki/Smooth_maximum for
    additional explanation.

    Args:
        value1: First value to compare.
        value2: Second value to compare.
        distance: Modulates the smoothness of the approximation.

    Returns:
        The approximated maximum.

    """
    return Scalar.math_operation_ternary(
        value1, value2, distance, operation="SMOOTH_MAX"
    )


def wrap(
    value: Scalar | float, min_value: Scalar | float, max_value: Scalar | float
) -> Scalar:
    """Wraps `value` to be within `min_value` and `max_value`.

    Outputs a value between `min_value` and `max_value` based on the absolute
    difference between the input value and the nearest integer multiple of
    `max_value` less than the value.

    Args:
        value: The input value.
        min_value: The left boundary of the domain of the output.
        max_value: The right boundary of the domain of the output.

    Returns:
        A value between `min_value` and `max_value`.

    """
    return Scalar.math_operation_ternary(value, min_value, max_value, operation="WRAP")


def clamp(scalar: Scalar) -> Scalar:
    """Clamps `scalar` between 0.0 and 1.0.

    Any values higher than 1.0 will be rounded down to 1.0, and any values
    lower than 0.0 will be rounded up to 0.0.

    Args:
        scalar: The input value to be clamped.

    Returns:
        A value between 0.0 and 1.0.

    """
    assert isinstance(scalar, Scalar)

    bl_node = scalar.socket_reference.node

    if isinstance(bl_node, bpy.types.ShaderNodeMath):
        bl_node.use_clamp = True
        return scalar
    elif isinstance(bl_node, bpy.types.ShaderNodeMapRange):
        bl_node.clamp = True
        return scalar

    node = AbstractSocket.new_node([scalar], "ShaderNodeMath")

    bl_node = node.get_bl_node()
    assert isinstance(bl_node, bpy.types.ShaderNodeMath)
    bl_node.operation = "ADD"
    bl_node.use_clamp = True

    node.connect_argument(0, scalar)
    node.connect_argument(1, 0.0)

    return Scalar(node, 0)


def log(value: Scalar | float, base: Scalar | float) -> Scalar:
    """Takes the logarithm of `value` with base `base`.

    Args:
        value: The input value.
        base: The base of the logarithm.

    Returns:
        The result of the operation.

    """
    return Scalar.math_operation_binary(value, base, operation="LOGARITHM")


def sqrt(value: Scalar) -> Scalar:
    """Takes the square root of `value`.

    Args:
        value: The input value.

    Returns:
        The result of the operation.

    """
    return Scalar.math_operation_unary(value, operation="SQRT")


def inverse_sqrt(value: Scalar) -> Scalar:
    """Returns `1/sqrt(value)`.

    Args:
        value: The input value.

    Returns:
        The result of the operation.

    """
    return Scalar.math_operation_unary(value, operation="INVERSE_SQRT")


def exp(value: Scalar) -> Scalar:
    """Takes the exponent of `value` with base `e` (Euler's number).

    Args:
        value: The input value.

    Returns:
        The result of the operation.

    """
    return Scalar.math_operation_unary(value, operation="EXPONENT")


def power(base: Scalar | float, exp: Scalar | float) -> Scalar:
    """Takes the exponent of `value` with base `e` (Euler's number).

    Args:
        value: The input value.

    Returns:
        The result of the operation.

    """
    return Scalar.math_operation_binary(base, exp, operation="POWER")


def minimum(arg1: Scalar, arg2: Scalar | float) -> Scalar:
    """Returns the minimum of the two input arguments.

    Args:
        arg1: The first value to compare.
        arg2: The second value to compare.

    Note:
        At least one of the two arguments should be a `Scalar` in order
        to use Blender's node tree. If both arguments are `float`, consider
        using the builtin `min` function instead.

    Returns:
        The minimum of the two input arguments.

    """
    return Scalar.math_operation_binary(arg1, arg2, operation="MINIMUM")


def maximum(arg1: Scalar, arg2: Scalar | float) -> Scalar:
    """Returns the maximum of the two input arguments.

    Args:
        arg1: The first value to compare.
        arg2: The second value to compare.

    Note:
        At least one of the two arguments should be a `Scalar` in order
        to use Blender's node tree. If both arguments are `float`, consider
        using the builtin `max` function instead.

    Returns:
        The maximum of the two input arguments.

    """
    return Scalar.math_operation_binary(arg1, arg2, operation="MAXIMUM")


def sign(value: Scalar) -> Scalar:
    """Extracts the sign of the input value.

    All positive numbers will output 1.0. All negative numbers will
    output -1.0. And 0.0 will output 0.0.

    Args:
        value: The input value.

    Returns:
        The sign of the input.

    """
    return Scalar.math_operation_unary(value, operation="SIGN")


def fract(value: Scalar) -> Scalar:
    """Extracts the distance between `value` and the nearest integer below `value`.

    Example:
        If the input field has a value of `16.53` at a certain point,
        this function will return a field with `0.53` at that point instead.

        An input field of `-4.30` will give `0.70`.

    Args:
        value: The input value.

    Returns:
        The fractional part of the input.

    """
    return Scalar.math_operation_unary(value, operation="FRACT")


def snap(value: Scalar | float, increment: Scalar | float) -> Scalar:
    """Rounds `value` down to an integer multiple of `increment`.

    Args:
        value: The input value.
        increment: The spacing between the values to snap to.

    Returns:
        The integer multiple of `increment` directly below `value`.

    """
    return Scalar.math_operation_binary(value, increment, operation="SNAP")


def pingpong(value: Scalar | float, scale: Scalar | float) -> Scalar:
    """The output value is moved between 0.0 and `scale` based on the input value.

    Args:
        value: The input value.
        scale: The maximum value that the output can take.

    Returns:
        A value between 0.0 and `scale`.

    """
    return Scalar.math_operation_binary(value, scale, operation="PINGPONG")


def sin(value: Scalar) -> Scalar:
    """Returns the sine of the input value."""
    return Scalar.math_operation_unary(value, operation="SINE")


def cos(value: Scalar) -> Scalar:
    """Returns the cosine of the input value."""
    return Scalar.math_operation_unary(value, operation="COSINE")


def tan(value: Scalar) -> Scalar:
    """Returns the tangent of the input value."""
    return Scalar.math_operation_unary(value, operation="TANGENT")


def asin(value: Scalar) -> Scalar:
    """Returns the arcsine of the input value."""
    return Scalar.math_operation_unary(value, operation="ARCSINE")


def acos(value: Scalar) -> Scalar:
    """Returns the arccosine of the input value."""
    return Scalar.math_operation_unary(value, operation="ARCCOSINE")


def atan(value: Scalar) -> Scalar:
    """Returns the arctangent of the input value."""
    return Scalar.math_operation_unary(value, operation="ARCTANGENT")


# pylint: disable=invalid-name; standard atan2 has y and x as arguments
def atan2(y: Scalar | float, x: Scalar | float) -> Scalar:
    """Returns the angle of the vector (x, y) in radians.

    Note:
        The arguments of `atan2` are reversed compared to how you
        would write it as a vector. This is standard for the `atan2`
        implementations, since this makes it mimic the closely
        related function `arctan(y/x)`.

    Returns:
        The angle in radians between the positive x-axis and the
        ray from the origin of the point(x, y)."""
    return Scalar.math_operation_binary(y, x, operation="ARCTAN2")


def sinh(value: Scalar) -> Scalar:
    """Returns the hyperbolic sine of the input value."""
    return Scalar.math_operation_unary(value, operation="SINH")


def cosh(value: Scalar) -> Scalar:
    """Returns the hyperbolic cosine of the input value."""
    return Scalar.math_operation_unary(value, operation="COSH")


def tanh(value: Scalar) -> Scalar:
    """Returns the hyperbolic tangent of the input value."""
    return Scalar.math_operation_unary(value, operation="TANH")


def step(edge: Scalar | float, x: Scalar | float) -> Scalar:
    """The Heaviside step function.

    Args:
        edge: The edge point of the unit step function.
        x: The input value.

    Returns:
        The field where values are 1.0 if `x < edge`, and 0.0 otherwise.

    Note:
        The behavior of this function should be equivalent to the
        `step()` function of OpenGL.

    """
    return Scalar.math_operation_binary(x, edge, operation="LESS_THAN")


def drop(edge: Scalar | float, x: Scalar | float) -> Scalar:
    """The mirrored version of the Heaviside step function.

    Args:
        edge: The edge point of the unit step function.
        x: The input value.

    Returns:
        The field where values are 1.0 if `x > edge`, and 0.0 otherwise.

    """
    return Scalar.math_operation_binary(x, edge, operation="GREATER_THAN")


# Boolean comparison:


def is_equal(
    A: Scalar | float,
    B: Scalar | float,
    epsilon: Scalar | float,
    mode: str = "ELEMENTWISE",
) -> Boolean:
    """Returns True if A and B are approximately equal.

    Computes a field which is True for all elements where the difference
    between `A` and `B` is less than `epsilon`, and False otherwise.

    Args:
        A: The first value to compare.
        B: The second value to compare.
        epsilon:
            The maximum difference between the compared inputs for them
            to be considered equal.
        mode:
            How to handle `Vector3` inputs. Unused if only `Scalar`s are
            compared. Defaults to "ELEMENTWISE".

    Returns:
        A boolean field that is the output of the operation.

    """
    return Scalar.math_comparison(A, B, epsilon, operation="EQUAL", mode=mode)


def is_not_equal(
    A: Scalar | float,
    B: Scalar | float,
    epsilon: Scalar | float,
    mode: str = "ELEMENTWISE",
) -> Boolean:
    """Returns False if A and B are approximately equal.

    Computes a field which is True for all elements where the difference
    between `A` and `B` is more than `epsilon`, and False otherwise.

    Args:
        A: The first value to compare.
        B: The second value to compare.
        epsilon:
            The maximum difference between the compared inputs for them
            to be considered equal.
        mode:
            How to handle `Vector3` inputs. Unused if only `Scalar`s are
            compared. Defaults to "ELEMENTWISE".

    Returns:
        A boolean field that is the output of the operation.

    """
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
    """Maps the input value from a range to a target range.

    Args:
        value: The input value or vector to be remapped.
        from_min: The lower bound of the range to remap from.
        from_max: The higher bound of the range to remap from.
        to_min: The lower bound of the target range.
        to_max: The higher bound of the target range.
        steps:
            The number of values allowed between To Min and To Max when
            using Stepped Linear interpolation. A higher value will give a
            smoother interpolation while lower values will progressively
            quantize the input.
        interpolation_type:
            The mathematical method used to transition between gaps in
            the numerical inputs.

            "LINEAR":
                Linear interpolation between `from_min` and `from_max` values.
            "STEPPED":
                Stepped linear interpolation between `from_min` and
                `from_max` values.
            "SMOOTHSTEP":
                Smooth Hermite edge interpolation between `from_min` and
                `from_max` values.
            "SMOOTHERSTEP":
                Smoother Hermite edge interpolation between `from_min`
                and `from_max` values.

            Defaults to "LINEAR".

    Returns:
        The input value after remapping.

    """
    node = AbstractSocket.add_linked_node(
        [value, from_min, from_max, to_min, to_max, steps],
        "ShaderNodeMapRange",
    )

    bl_node = node.get_bl_node()
    assert isinstance(bl_node, bpy.types.ShaderNodeMapRange)
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
    """Maps the input vector elementwise from a range to a target range.

    Args:
        value: The input value or vector to be remapped.
        from_min: The lower bound of the range to remap from.
        from_max: The higher bound of the range to remap from.
        to_min: The lower bound of the target range.
        to_max: The higher bound of the target range.
        steps:
            The number of values allowed between To Min and To Max when
            using Stepped Linear interpolation. A higher value will give a
            smoother interpolation while lower values will progressively
            quantize the input.
        interpolation_type:
            The mathematical method used to transition between gaps in
            the numerical inputs.

            "LINEAR":
                Linear interpolation between `from_min` and `from_max` values.
            "STEPPED":
                Stepped linear interpolation between `from_min` and
                `from_max` values.
            "SMOOTHSTEP":
                Smooth Hermite edge interpolation between `from_min` and
                `from_max` values.
            "SMOOTHERSTEP":
                Smoother Hermite edge interpolation between `from_min`
                and `from_max` values.

            Defaults to "LINEAR".

    Returns:
        The input value after remapping.

    """
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
    assert isinstance(bl_node, bpy.types.ShaderNodeMapRange)
    bl_node.clamp = False
    bl_node.interpolation_type = interpolation_type
    bl_node.data_type = "FLOAT_VECTOR"

    return Vector3(node, 0)
