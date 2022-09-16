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
    def move_vertices(self, position = None, offset = None, selection = None):
        node, layer = self.new_node([self, position, offset, selection], 'GeometryNodeSetPosition')
        
        self.node_tree.links.new(self.socket_reference, node.inputs[0])
        
        self.add_link_with_typecheck(selection, node, 0, Boolean)
        self.add_link_with_typecheck(position, node, 1, Vector3)
        self.add_link_with_typecheck(offset, node, 2, Vector3)
        
        return Geometry(self.node_tree, node.outputs[0], layer)
    
    # "Geometry Proximity" in Blender:
    def __get_closest(self, target_element: str = 'POINTS', source_position: Vector3 = None):
        node, layer = self.new_node([self, source_position], 'GeometryProximityNode')
        node.target_element = target_element
        
        self.add_link_with_typecheck(self, node, 0, Geometry)
        self.add_link_with_typecheck(source_position, node, 1, Vector3)
        
        position = Vector3(self.node_tree, node.outputs[0], layer)
        distance = Scalar(self.node_tree, node.outputs[1], layer)
        
        return position, distance
    
    def get_closest_point(self, source_position: Vector3):
        return self.__get_closest('POINTS', source_position)
    
    def get_closest_edge(self, source_position: Vector3):
        return self.__get_closest('EDGES', source_position)
    
    def get_closest_face(self, source_position: Vector3):
        return self.__get_closest('FACES', source_position)
    
    
