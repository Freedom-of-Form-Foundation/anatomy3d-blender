#!/usr/bin/python3

import bpy

from .types import *
from .math import *

class GeometryFunction():
    """Generate geometry node trees. Corresponds to a GeometryNodeTree."""
    
    def __init__(self, name: str):
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
    
    def __shift_output_node(self, layer):
        if layer > self.output_layer:
            self.group_output.location = (200.0 * layer, 0.0)
    
    # Adding group inputs:
    def InputGeometry(self):
        self.input_counter += 1
        return self.node_tree.inputs.new('NodeSocketGeometry', 'Geometry')
    
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
    
    
    def OutputBoolean(
            self,
            variable,
            name: str,
            tooltip: str = '',
            attribute_domain: str = '',
            default_attribute_name: str = '',
            default_value: bool = False,
            min_value: float = float('-inf'),
            max_value: float = float('inf')):
        
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
            attribute_domain: str = '',
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
            attribute_domain: str = '',
            default_attribute_name: str = '',
            default_value = [0.0, 0.0, 0.0],
            min_value: float = float('-inf'),
            max_value: float = float('inf')):
        
        output = self.node_tree.outputs.new('NodeSocketVector', name)
        output.description = tooltip
        output.attribute_domain = attribute_domain
        output.default_attribute_name = default_attribute_name
        
        if len(default_value) != 3:
            raise ValueError("default_value is not a vector3.")
        
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
        

class ExampleFunction(GeometryFunction):
    """Add tubercules to bones"""
    
    def __init__(self, name: str):
        super().__init__(name)
        
        # Add new nodes to the tree:
        input = self.InputGeometry()
        output = self.OutputGeometry()
        variable = self.InputFloat('Float Input')
        vector1 = self.InputVector('Vector Input')
        
        variable2 = variable + 3.0
        variable3 = variable2 + variable
        variable4 = 4.0 + variable2
        variable5 = variable + (3.0 + 2.0) * variable

        vector2 = 2.0 * vector1
        
        variable6 = vector2.y + variable3
        variable7 = vector2.x + 2.0
        
        variable8 = clamp(min(multiply_add(variable4, variable3, variable5), variable2))
        
        self.OutputFloat(variable8, 'Float Output Name', attribute_domain = 'POINT', default_value = 0.5)
        
        
        
        




