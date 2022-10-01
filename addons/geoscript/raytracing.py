#!/usr/bin/python3

"""Functions and classes for calculating ray-mesh intersections in GeoScript."""

import bpy

from .types import AbstractSocket, NodeHandle, Scalar, Boolean, Vector3, Geometry


class RayHit(NodeHandle):
    """The intersection point between a ray and a mesh, if hit."""

    def is_hit(self) -> Boolean:
        """True only if the ray intersects the mesh it was casted to."""
        return Boolean(self, 0)

    def hit_position(self) -> Vector3:
        """The 3D location where the ray intersects the mesh."""
        return Vector3(self, 1)

    def hit_normal(self) -> Vector3:
        """The normal vector of the point on the mesh where the ray intersects."""
        return Vector3(self, 2)

    def hit_distance(self) -> Scalar:
        """The distance between the ray start point and the intersection point."""
        return Scalar(self, 3)

    def attribute(self) -> Scalar | Boolean | Vector3 | None:
        """The value of the selected attribute stored on the mesh at the ray hit."""
        if self.get_output(4).type == "VALUE":  # "VALUE" stands for float in Blender.
            return Scalar(self, 4)
        elif self.get_output(4).type == "INT":
            return Scalar(self, 4)
        elif self.get_output(4).type == "BOOLEAN":
            return Boolean(self, 4)
        elif self.get_output(4).type == "VECTOR":
            return Vector3(self, 4)
        elif self.get_output(4).type == "COLOR":
            return None
        return None


def raycast_with_attribute(
    source_position: Vector3,
    ray_direction: Vector3,
    ray_length: Scalar | float,
    target_geometry: Geometry,
    attribute=None,
    attribute_data_type: str = "FLOAT",
    attribute_mapping: str = "INTERPOLATED",
) -> RayHit:
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
    # Blender uses a different argument index for the input attribute
    # depending on `attribute_data_type`. Hence we need to fill
    # part of the `arguments` list with empty sockets, and then
    # connect the attribute input to the correct socket based on
    # `attribute_data_type`.
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
    node = AbstractSocket.add_linked_node(
        arguments, "GeometryNodeRaycast"
    )

    # Set the Blender node's properties:
    bl_node = node.get_bl_node()
    assert isinstance(bl_node, bpy.types.GeometryNodeRaycast)
    bl_node.data_type = attribute_data_type
    bl_node.mapping = attribute_mapping

    return RayHit(node.get_bl_tree(), node.get_bl_node(), node.get_layer())


def raycast(
    source_position: Vector3,
    ray_direction: Vector3,
    ray_length: Scalar | float,
    target_geometry: Geometry,
) -> RayHit:
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
