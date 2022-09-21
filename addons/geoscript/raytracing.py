#!/usr/bin/python3

import bpy

from .types import AbstractSocket
from .types import Scalar
from .types import Boolean
from .types import Vector3
from .types import Geometry


class RayHit:
    def __init__(self, node_tree, node, layer):
        self.__node_tree = node_tree
        self.__node = node
        self.__layer = layer

    def is_hit(self):
        return Boolean(self.__node_tree, self.__node.outputs[0], self.__layer)

    def hit_position(self):
        return Vector3(self.__node_tree, self.__node.outputs[1], self.__layer)

    def hit_normal(self):
        return Vector3(self.__node_tree, self.__node.outputs[2], self.__layer)

    def hit_distance(self):
        return Scalar(self.__node_tree, self.__node.outputs[3], self.__layer)

    def attribute(self):
        if self.__node.outputs[4].type == "VALUE":
            return Scalar(self.__node_tree, self.__node.outputs[3], self.__layer)
        elif self.__node.outputs[4].type == "INT":
            return Scalar(self.__node_tree, self.__node.outputs[3], self.__layer)
        elif self.__node.outputs[4].type == "BOOLEAN":
            return Boolean(self.__node_tree, self.__node.outputs[3], self.__layer)
        elif self.__node.outputs[4].type == "VECTOR":
            return Vector3(self.__node_tree, self.__node.outputs[3], self.__layer)
        elif self.__node.outputs[4].type == "COLOR":
            return None


def raycast_with_attribute(
    source_position: Vector3,
    ray_direction: Vector3,
    ray_length: Scalar | float,
    target_geometry: Geometry,
    attribute=None,
    attribute_data_type: str = "FLOAT",
    attribute_mapping: str = "INTERPOLATED",
):
    """Raycasts and samples an attribute at the ray intersection.

    Casts a rat from source_position onto target_geometry, and get the attribute
    at the ray hit point.

    Args:
        source_position:
            The starting point of the ray.
        ray_direction:
            Direction of the ray.
        ray_length:
            The maximum distance of the ray.
        target_geometry:
            The geometry that the ray can intersect.
        attribute:
            The geometry attribute to sample at the point of intersection.
        attribute_data_type:
            The data type of the attribute to sample.
        attribute_mapping:
            Whether to sample the attribute from the nearest element where the
            attribute is stored (such as a vertex), or whether to interpolate
            the attribute at the exact position of intersection (in the middle
            of a plane in the geometry).

    Raises:
        TypeError:
            One of the arguments is of the wrong type.

    Returns:
        A RayHit instance that contains the outputs of the ray cast.
    """
    arguments = [
        target_geometry,
        None,
        None,
        None,
        None,
        None,
        source_position,
        ray_direction,
        ray_length,
    ]

    # Connect attribute nodes:
    if attribute_data_type == "FLOAT":
        arguments[2] = attribute
    elif attribute_data_type == "INT":
        arguments[5] = attribute
    elif attribute_data_type == "FLOAT_VECTOR":
        arguments[1] = attribute
    elif attribute_data_type == "FLOAT_COLOR":
        arguments[3] = attribute
    elif attribute_data_type == "BOOLEAN":
        arguments[4] = attribute

    # Create node:
    node_tree, node, layer = AbstractSocket.add_linked_node(
        arguments, "GeometryNodeRaycast"
    )

    node.data_type = attribute_data_type
    node.mapping = attribute_mapping

    return RayHit(node_tree, node, layer)


def raycast(
    source_position: Vector3,
    ray_direction: Vector3,
    ray_length: Scalar | float,
    target_geometry: Geometry,
):
    """Casts a ray from source_position onto target_geometry.

    Args:
        source_position:
            The starting point of the ray.
        ray_direction:
            Direction of the ray.
        ray_length:
            The maximum distance of the ray.
        target_geometry:
            The geometry that the ray can intersect.
        attribute:
            The geometry attribute to sample at the point of intersection.
        attribute_data_type:
            The data type of the attribute to sample.
        attribute_mapping:
            Whether to sample the attribute from the nearest element where the
            attribute is stored (such as a vertex), or whether to interpolate
            the attribute at the exact position of intersection (in the middle
            of a plane in the geometry).

    Raises:
        TypeError:
            One of the arguments is of the wrong type.

    Returns:
        A RayHit instance that contains the outputs of the ray cast.
    """
    return raycast_with_attribute(
        source_position, ray_direction, ray_length, target_geometry
    )
