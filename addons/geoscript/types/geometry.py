#!/usr/bin/python3

import bpy

from .abstract_socket import AbstractSocket
from .vector3 import Vector3
from .scalar import Scalar
from .boolean import Boolean

class Geometry(AbstractSocket):
    """Corresponds to a Geometry socket type in Blender's Geometry Nodes"""
    
    def __init__(
            self,
            node_tree: bpy.types.NodeTree = None,
            socket_reference: bpy.types.NodeSocket = None,
            layer: int = 0):
        super().__init__(node_tree, socket_reference, layer)
    
    @staticmethod
    def get_bl_idnames():
        """Returns a list of Blender socket types that this class represents.
        
        Returns:
            List of strings corresponding to Blender Geometry Nodes socket
            types.
        """
        return ['GEOMETRY']
    
    # "Set Position" in Blender:
    def move_vertices(self,
            position: Vector3 = None,
            offset: Vector3 = None,
            selection: Boolean = None):
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
        tree, node, layer = AbstractSocket.add_linked_node(arguments, 'GeometryNodeSetPosition')
        return Geometry(tree, node.outputs[0], layer)
    
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
        tree, node, layer = AbstractSocket.add_linked_node(arguments, 'GeometryNodeSetID')
        return Geometry(tree, node.outputs[0], layer)
    
    # "Geometry Proximity" in Blender:
    def __get_closest(self, target_element: str = 'POINTS', source_position: Vector3 = None):
        tree, node, layer = self.new_node([self, source_position], 'GeometryNodeProximity')
        node.target_element = target_element
        
        self.add_link_with_typecheck(self, node, 0, Geometry)
        self.add_link_with_typecheck(source_position, node, 1, Vector3)
        
        position = Vector3(tree, node.outputs[0], layer)
        distance = Scalar(tree, node.outputs[1], layer)
        
        return position, distance
    
    def get_closest_point(self, source_position: Vector3):
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
        return self.__get_closest('POINTS', source_position)
    
    def get_closest_edge(self, source_position: Vector3):
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
        return self.__get_closest('EDGES', source_position)
    
    def get_closest_face(self, source_position: Vector3):
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
        return self.__get_closest('FACES', source_position)
    
    # "Transform" in Blender:
    def transform(self, translation: Vector3, rotation: Vector3, scale: Vector3):
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
        tree, node, layer = AbstractSocket.add_linked_node(arguments, 'GeometryNodeTransform')
        return Geometry(tree, node.outputs[0], layer)
    
    # "Separate Geometry" in Blender:
    def separate_geometry(self, selection: Boolean, domain: str = 'POINT'):
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
        tree, node, layer = AbstractSocket.add_linked_node(arguments, 'GeometryNodeSeparateGeometry')
        
        selection = Geometry(tree, node.outputs[0], layer)
        inverted = Geometry(tree, node.outputs[1], layer)
        
        return (selection, inverted)
    
    # "Separate Component" in Blender:
    def __get_component(self, index: int):
        if not hasattr(self, '_components_node'):
            t, node, l = AbstractSocket.add_linked_node([self], 'GeometryNodeSeparateComponents')
            self._components_node = node
        
        node = self._components_node
        
        return Geometry(self.node_tree, node.outputs[index], self.layer + 1)
    
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
    def merge_all_by_distance(self, selection: Boolean, merge_distance: Scalar):
        """Merges all vertices that are close together.
        
        Args:
            selection:
                Which vertices to merge.
            merge_distance:
                The maximum proximity between two elements in which they are
                merged.
        
        Raises:
            TypeError:
                One of the arguments is of the wrong type.
        
        Returns:
            The geometry after the merging.
        """
        arguments = [self, selection, merge_distance]
        tree, node, layer = AbstractSocket.add_linked_node(arguments, 'GeometryNodeMergeByDistance')
        node.mode = 'ALL'
        
        return Geometry(tree, node.outputs[0], layer)
    
    def merge_connected_by_distance(self, selection: Boolean, merge_distance: Scalar):
        """Merges only vertices connected by an edge that are close together.
        
        Args:
            selection:
                Which vertices to merge.
            merge_distance:
                The maximum proximity between two elements in which they are
                merged.
        
        Raises:
            TypeError:
                One of the arguments is of the wrong type.
        
        Returns:
            The geometry after the merging.
        """
        arguments = [self, selection, merge_distance]
        tree, node, layer = AbstractSocket.add_linked_node(arguments, 'GeometryNodeMergeByDistance')
        node.mode = 'CONNECTED'
        
        return Geometry(tree, node.outputs[0], layer)
    
    # "Geometry to Instance" in Blender:
    def to_instances(self):
        """Converts the geometry to an instance.
        
        Converts the geometry to an instance for use with nodes that manipulate
        instances.
        
        Returns:
            A new Geometry that has internally been converted to instances.
        """
        tree, node, layer = AbstractSocket.add_linked_node([self], 'GeometryNodeGeometryToInstance')
        
        return Geometry(tree, node.outputs[0], layer)
    
    # "Bounding Box" in Blender:
    def __get_bounding_box_node(self):
        previous_node = self.socket_reference.node
        
        if previous_node.bl_idname == 'GeometryNodeBoundBox':
            return (self.node_tree, previous_node, self.layer)
        else:
            tree, node, layer = AbstractSocket.add_linked_node([self], 'GeometryNodeBoundBox')
            return (tree, node, layer)
    
    def get_bounding_box_geometry(self):
        """Gets the geometry of the bounding box.
        
        Returns:
            A new Geometry that contains the bounding box.
        """
        tree, node, layer = self.__get_bounding_box_node()
        return Geometry(tree, node.outputs[0], layer)
    
    def get_bounding_box_points(self):
        """Gets the positions of the corners of the bounding box.
        
        Returns:
            A tuple containing the two opposite Vector3 points of the bounding
            box.
        """
        tree, node, layer = self.__get_bounding_box_node()
        minimum = Vector3(tree, node.outputs[1], layer)
        maximum = Vector3(tree, node.outputs[2], layer)
        return (minimum, maximum)
        
    # "Convex Hull" in Blender:
    def get_convex_hull(self):
        """Returns the convex hull mesh.
        
        Returns:
            A new Geometry containing the convex hull mesh of this geometry.
        """
        tree, node, layer = AbstractSocket.add_linked_node([self], 'GeometryNodeConvexHull')
        return Geometry(tree, node.outputs[0], layer)


