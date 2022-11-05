#!/usr/bin/python3

import bpy

from typing import Tuple
from .abstract_socket import AbstractSocket, NodeHandle
from .vector3 import Vector3
from .scalar import Scalar
from .boolean import Boolean


class Geometry(AbstractSocket):
    """Corresponds to a Geometry socket type in Blender's Geometry Nodes"""

    @staticmethod
    def get_bl_idnames():
        """Returns a list of Blender socket types that this class represents.

        Returns:
            List of strings corresponding to Blender Geometry Nodes socket
            types.
        """
        return ["GEOMETRY"]

    # "Set Position" in Blender:
    def move_vertices(
        self,
        position: Vector3 = None,
        offset: Vector3 = None,
        selection: Boolean = None,
    ):
        """Moves vertices in the geometry to a different position.

        Args:
            position:
                The absolute position that the vertices will be moved to. If
                None, the vertices will only be moved relative to the position
                it already has.
            offset:
                The relative position that the vertices will be shifted towards.
                This is added to the position of the vertices.
            selection:
                The selection of vertices that will be moved. If selection is
                False for a certain vertex, then that vertex will not be moved.

        Raises:
            TypeError:
                One of the arguments is of the wrong type.

        Returns:
            The geometry after the transformation.
        """
        arguments = [self, selection, position, offset]
        node = AbstractSocket.add_linked_node(arguments, "GeometryNodeSetPosition")
        return Geometry(node, 0)

    # "Set ID":
    def set_id(self, id: Scalar | int, selection: Boolean = None):
        """Sets the ID of the vertices in the geometry.

        Args:
            id:
                The ID that will be assigned to the appropriate vertex.
            selection:
                The selection of vertices that will be changed by this
                operation. If selection is False for a certain vertex, then
                that vertex will not have its ID changed.

        Raises:
            TypeError:
                One of the arguments is of the wrong type.

        Returns:
            The geometry after the assignment of the IDs.
        """
        arguments = [self, selection, id]
        node = AbstractSocket.add_linked_node(arguments, "GeometryNodeSetID")
        return Geometry(node, 0)

    # "Geometry Proximity" in Blender:
    def __get_closest(
        self, target_element: str, source_position: Vector3 = None
    ) -> Tuple[Vector3, Scalar]:
        node = self.add_linked_node([self, source_position], "GeometryNodeProximity")

        bl_node = node.get_bl_node()
        assert isinstance(bl_node, bpy.types.GeometryNodeProximity)
        bl_node.target_element = target_element

        position = Vector3(node, 0)
        distance = Scalar(node, 1)

        return position, distance

    def get_closest_point(self, source_position: Vector3) -> Tuple[Vector3, Scalar]:
        """Gets the vertex and distance closest to source_position.

        Args:
            source_position:
                The position from which to find the closest distance to the
                geometry.

        Raises:
            TypeError:
                One of the arguments is of the wrong type.

        Returns:
            A tuple containing (position, distance):
                position:
                    The position of the vertex in the geometry that is the
                    closest to source_position.
                distance:
                    The distance between that vertex and source_position.
        """
        return self.__get_closest("POINTS", source_position)

    def get_closest_edge(self, source_position: Vector3) -> Tuple[Vector3, Scalar]:
        """Gets the edge position and distance closest to source_position.

        Args:
            source_position:
                The position from which to find the closest distance to the
                geometry.

        Raises:
            TypeError:
                One of the arguments is of the wrong type.

        Returns:
            A tuple containing (position, distance):
                position:
                    The position of the edge in the geometry that is the
                    closest to source_position.
                distance:
                    The distance between that edge and source_position.
        """
        return self.__get_closest("EDGES", source_position)

    def get_closest_face(self, source_position: Vector3) -> Tuple[Vector3, Scalar]:
        """Gets the face position and distance closest to source_position.

        Args:
            source_position:
                The position from which to find the closest distance to the
                geometry.

        Raises:
            TypeError:
                One of the arguments is of the wrong type.

        Returns:
            A tuple containing (position, distance):
                position:
                    The position of the face in the geometry that is the
                    closest to source_position.
                distance:
                    The distance between that face and source_position.
        """
        return self.__get_closest("FACES", source_position)

    # "Transform" in Blender:
    def transform(
        self, translation: Vector3, rotation: Vector3, scale: Vector3
    ) -> "Geometry":
        """Transforms the entire geometry.

        Args:
            translation:
                The change in position.
            rotation:
                The Euler rotation to transform the geometry with.
            scale:
                Vector3 containing the x, y, z scale.

        Raises:
            TypeError:
                One of the arguments is of the wrong type.

        Returns:
            The geometry after the transformation.
        """
        arguments = [self, translation, rotation, scale]
        node = AbstractSocket.add_linked_node(arguments, "GeometryNodeTransform")
        return Geometry(node, 0)

    # "Separate Geometry" in Blender:
    def separate_geometry(
        self, selection: Boolean, domain: str = "POINT"
    ) -> Tuple["Geometry", "Geometry"]:
        """Separates the geometry into two parts using selection.

        Args:
            selection:
                Elements where selection is True will be assigned to the first
                output, and elements where selection is False will be assigned
                to the second output.
            domain:
                The type of elements that are separated. Must be one of
                ['POINT', 'EDGE', 'FACE', 'CURVE', 'INSTANCE'].

        Raises:
            TypeError:
                One of the arguments is of the wrong type.

        Returns:
            The geometry after the transformation.
        """
        arguments = [self, selection]
        node = AbstractSocket.add_linked_node(arguments, "GeometryNodeSeparateGeometry")

        selected = Geometry(node, 0)
        inverted = Geometry(node, 1)

        return (selected, inverted)

    # "Separate Component" in Blender:
    def __get_component(self, index: int):
        if not hasattr(self, "_components_node"):
            self._components_node = AbstractSocket.add_linked_node(
                [self], "GeometryNodeSeparateComponents"
            )
        return Geometry(self._components_node, index)

    def get_mesh_component(self):
        """Isolate the mesh inside this geometry, if any."""
        return self.__get_component(0)

    def get_point_cloud_component(self):
        """Isolate the point cloud inside this geometry, if any."""
        return self.__get_component(1)

    def get_curve_component(self):
        """Isolate the curve component inside this geometry, if any."""
        return self.__get_component(2)

    def get_volume_component(self):
        """Isolate the volume component inside this geometry, if any."""
        return self.__get_component(3)

    def get_instances_component(self):
        """Isolate the instances inside this geometry, if any."""
        return self.__get_component(4)

    # "Merge by Distance" in Blender:
    def merge_all_by_distance(
        self, merge_distance: Scalar, selection: Boolean | bool = True
    ):
        """Merges all vertices that are close together.

        Args:
            merge_distance:
                The maximum proximity between two elements in which they are
                merged.
            selection:
                Which vertices to merge. If true, all elements will be merged by
                distance.

        Raises:
            TypeError:
                One of the arguments is of the wrong type.

        Returns:
            The geometry after the merging.
        """
        arguments = [self, selection, merge_distance]
        node = AbstractSocket.add_linked_node(arguments, "GeometryNodeMergeByDistance")
        bl_node = node.get_bl_node()
        assert isinstance(bl_node, bpy.types.GeometryNodeMergeByDistance)
        bl_node.mode = "ALL"
        return Geometry(node, 0)

    def merge_connected_by_distance(
        self, merge_distance: Scalar, selection: Boolean | bool = True
    ) -> "Geometry":
        """Merges only vertices connected by an edge that are close together.

        Args:
            merge_distance:
                The maximum proximity between two elements in which they are
                merged.
            selection:
                Which vertices to merge. If true, all elements will be merged by
                distance.

        Raises:
            TypeError:
                One of the arguments is of the wrong type.

        Returns:
            The geometry after the merging.
        """
        arguments = [self, selection, merge_distance]
        node = AbstractSocket.add_linked_node(arguments, "GeometryNodeMergeByDistance")
        bl_node = node.get_bl_node()
        assert isinstance(bl_node, bpy.types.GeometryNodeMergeByDistance)
        bl_node.mode = "CONNECTED"
        return Geometry(node, 0)

    # "Geometry to Instance" in Blender:
    def to_instances(self) -> "Geometry":
        """Converts the geometry to an instance.

        Converts the geometry to an instance for use with nodes that manipulate
        instances.

        Returns:
            A new Geometry that has internally been converted to instances.
        """
        node = AbstractSocket.add_linked_node([self], "GeometryNodeGeometryToInstance")
        return Geometry(node, 0)

    # "Bounding Box" in Blender:
    def __get_bounding_box_node(self) -> NodeHandle:
        previous_node = self.socket_reference.node
        if previous_node.bl_idname == "GeometryNodeBoundBox":
            return NodeHandle(self.node_tree, previous_node)
        else:
            return AbstractSocket.add_linked_node([self], "GeometryNodeBoundBox")

    def get_bounding_box_geometry(self) -> "Geometry":
        """Gets the geometry of the bounding box.

        Returns:
            A new Geometry that contains the bounding box.
        """
        node = self.__get_bounding_box_node()
        return Geometry(node, 0)

    def get_bounding_box_points(self) -> Tuple[Vector3, Vector3]:
        """Gets the positions of the corners of the bounding box.

        Returns:
            A tuple containing the two opposite Vector3 points of the bounding
            box.
        """
        node = self.__get_bounding_box_node()
        minimum = Vector3(node, 1)
        maximum = Vector3(node, 2)
        return (minimum, maximum)

    # "Convex Hull" in Blender:
    def get_convex_hull(self) -> "Geometry":
        """Returns the convex hull mesh.

        Returns:
            A new Geometry containing the convex hull mesh of this geometry.
        """
        node = AbstractSocket.add_linked_node([self], "GeometryNodeConvexHull")
        return Geometry(node, 0)

    # "Raycast" in Blender:
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
            if self.get_output(4).type == "VALUE":  # "VALUE" means float in Blender.
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

    def raycast(
        self,
        source_position: Vector3,
        ray_direction: Vector3,
        ray_length: Scalar | float,
        attribute=None,
        attribute_data_type: str = "FLOAT",
        attribute_mapping: str = "INTERPOLATED",
    ) -> RayHit:
        """Raycasts and samples an attribute at the ray intersection.

        Casts a rat from source_position onto self, and get the attribute
        at the ray hit point.

        Args:
            source_position:
                The starting point of the ray.
            ray_direction:
                Direction of the ray.
            ray_length:
                The maximum distance of the ray.
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
            self,
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

        return self.RayHit(node.get_bl_tree(), node.get_bl_node())
