#!/usr/bin/python3

import bpy

from .types import *
from .math import *
import math as constants

class GeometryNodeTree():
    """Generate geometry node trees. Corresponds to a GeometryNodeTree."""
    
    def __init__(self, name: str):
        self.__registered_name = name
        
        # Get the node tree. If it doesn't yet exist, create a new tree:
        self.node_tree = bpy.data.node_groups.get(name)
        if not self.node_tree:
            self.node_tree = bpy.data.node_groups.new(name, 'GeometryNodeTree')

        # Remove all content from the existing node tree:
        for node in self.node_tree.nodes:
            self.node_tree.nodes.remove(node)

        for input in self.node_tree.inputs:
            self.node_tree.inputs.remove(input)
            
        for output in self.node_tree.outputs:
            self.node_tree.outputs.remove(output)
            
        # TODO: removing the inputs and outputs of the pre-existing tree will reset all
        # parameters. This should be fixed to prevent having to redo the parameters if
        # the user changed them.

        self.input_counter = 0
        self.output_counter = 0
        self.output_layer = 0
        
        self.group_input = self.node_tree.nodes.new('NodeGroupInput')
        self.group_output = self.node_tree.nodes.new('NodeGroupOutput')
    
    def get_registered_name(self):
        return self.__registered_name
    
    def __shift_output_node(self, layer):
        if layer > self.output_layer:
            self.group_output.location = (200.0 * layer, 0.0)
            self.output_layer = layer
    
    # Adding group inputs:
    def InputGeometry(self, name: str = 'Geometry'):
        input_geometry = self.node_tree.inputs.new('NodeSocketGeometry', name)
        
        socket = Geometry(self.node_tree, self.group_input.outputs[self.input_counter])
        
        self.input_counter += 1
        
        return socket
    
    def InputBoolean(self, name: str = 'Geometry'):
        input_boolean = self.node_tree.inputs.new('NodeSocketBool', name)
        
        socket = Boolean(self.node_tree, self.group_input.outputs[self.input_counter])
        
        self.input_counter += 1
        
        return socket
    
    def InputFloat(self, name: str):
        input_float = self.node_tree.inputs.new('NodeSocketFloat', name)
        
        socket = Scalar(self.node_tree, self.group_input.outputs[self.input_counter])
        
        self.input_counter += 1
        
        return socket
    
    def InputVector(self, name: str):
        input_vector = self.node_tree.inputs.new('NodeSocketVector', name)
        
        socket = Vector3(self.node_tree, self.group_input.outputs[self.input_counter])
        
        self.input_counter += 1
        
        return socket
    
    # Adding group outputs:
    def OutputGeometry(self):
        self.output_counter += 1
        return self.node_tree.outputs.new('NodeSocketGeometry', 'Geometry')
    
    def OutputGeometry(
            self,
            variable,
            name: str,
            tooltip: str = ''):
        
        output = self.node_tree.outputs.new('NodeSocketGeometry', name)
        output.description = tooltip
        
        self.node_tree.links.new(
            variable.socket_reference,
            self.group_output.inputs[self.output_counter])
        
        self.output_counter += 1
        
        self.__shift_output_node(variable.layer + 1)
        
        return output
    
    
    def OutputBoolean(
            self,
            variable,
            name: str,
            tooltip: str = '',
            attribute_domain: str = 'POINT',
            default_attribute_name: str = '',
            default_value: bool = False):
        
        output = self.node_tree.outputs.new('NodeSocketFloat', name)
        output.description = tooltip
        output.attribute_domain = attribute_domain
        output.default_attribute_name = default_attribute_name
        output.default_value = default_value
        
        self.node_tree.links.new(
            variable.socket_reference,
            self.group_output.inputs[self.output_counter])
        
        self.output_counter += 1
        
        self.__shift_output_node(variable.layer + 1)
        
        return output

    
    def OutputFloat(
            self,
            variable,
            name: str,
            tooltip: str = '',
            attribute_domain: str = 'POINT',
            default_attribute_name: str = '',
            default_value: float = 0.0,
            min_value: float = float('-inf'),
            max_value: float = float('inf')):
        
        output = self.node_tree.outputs.new('NodeSocketFloat', name)
        output.description = tooltip
        output.attribute_domain = attribute_domain
        output.default_attribute_name = default_attribute_name
        output.default_value = default_value
        output.min_value = min_value
        output.max_value = max_value
        
        self.node_tree.links.new(
            variable.socket_reference,
            self.group_output.inputs[self.output_counter])
        
        self.output_counter += 1
        
        self.__shift_output_node(variable.layer + 1)
        
        return output


    def OutputVector(
            self,
            variable,
            name: str,
            tooltip: str = '',
            attribute_domain: str = 'POINT',
            default_attribute_name: str = '',
            default_value = [0.0, 0.0, 0.0],
            min_value: float = float('-inf'),
            max_value: float = float('inf')):
        
        output = self.node_tree.outputs.new('NodeSocketVector', name)
        output.description = tooltip
        output.attribute_domain = attribute_domain
        output.default_attribute_name = default_attribute_name
        
        if len(default_value) != 3:
            raise ValueError("default_value is not an array of size 3.")
        
        for i in range(0, 2):
            output.default_value[i] = default_value[i]
        
        output.min_value = min_value
        output.max_value = max_value
        
        self.node_tree.links.new(
            variable.socket_reference,
            self.group_output.inputs[self.output_counter])
        
        self.output_counter += 1
        
        self.__shift_output_node(variable.layer + 1)
        
        return output
    
    # Built in attributes (menu 'Input'):
    def position(self):
        position = self.node_tree.nodes.new('GeometryNodeInputPosition')
        return Vector(self.node_tree, position.outputs[0])
    
    def normal(self):
        normal = self.node_tree.nodes.new('GeometryNodeInputNormal')
        return Vector(self.node_tree, normal.outputs[0])
    
    def radius(self):
        radius = self.node_tree.nodes.new('GeometryNodeInputRadius')
        return Scalar(self.node_tree, radius.outputs[0])
    
    def ID(self):
        ID = self.node_tree.nodes.new('GeometryNodeInputID')
        return Scalar(self.node_tree, ID.outputs[0])
    
    def named_attribute(self, attribute_name: str, data_type: str = 'FLOAT'):
        attribute = self.node_tree.nodes.new('GeometryNodeInputNamedAttribute')
        attribute.inputs[0].default_value = attribute_name
        attribute.data_type = data_type
        return Scalar(self.node_tree, attribute.outputs[0])
    
    def scene_time_seconds(self, attribute_name: str, data_type: str = 'FLOAT'):
        seconds = self.node_tree.nodes.new('GeometryNodeInputSceneTime')
        return Scalar(self.node_tree, seconds.outputs[0])
    
    def scene_time_frame(self, attribute_name: str, data_type: str = 'FLOAT'):
        frame = self.node_tree.nodes.new('GeometryNodeInputSceneTime')
        return Scalar(self.node_tree, frame.outputs[1])



        
        
        
        




