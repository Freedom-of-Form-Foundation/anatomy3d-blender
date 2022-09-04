#!/usr/bin/python3
import bpy

class AbstractSocket():
    """Any type of output inside a node tree. This class handles the positioning and routing
    of new nodes in a node tree."""
    
    def __init__(self, node_tree: bpy.types.NodeTree = None, socket_reference: bpy.types.NodeSocket = None, layer: int = 0):
        if not node_tree:
            node_tree = bpy.types.GeometryNodeTree()
            
        self.node_tree = node_tree
        self.socket_reference = socket_reference
        self.layer = layer
    
    @staticmethod
    def new_node(input_list, node_type: str = ''):
        """Add a new node to the right of all input sockets."""
        
        # First calculate which is the rightmost layer of the input sockets:
        max_layer = 0
        for socket in input_list:
            if not isinstance(socket, AbstractSocket):
                raise TypeError("Socket inside socket list is not an instance of AbstractSocket, but of {}. This is a bug, please report to the developers.".format(socket.__class__))
            
            max_layer = max(max_layer, socket.layer)
        
        new_layer = max_layer + 1
        
        # Then create a new node to the right of that rightmost layer:
        new_node = input_list[0].node_tree.nodes.new(node_type)
        new_node.location = (200.0 * new_layer, 0.0)
        
        return (new_node, new_layer)
        

class AbstractTensor(AbstractSocket):
    """A mathematical object on which various operations can be performed, such as a Scalar or a Vector."""
    
    def __init__(self, node_tree: bpy.types.NodeTree = None, socket_reference: bpy.types.NodeSocket = None, layer: int = 0):
        super().__init__(node_tree, socket_reference, layer)
    
    @staticmethod
    def math_operation_unary(input, operation: str = 'ADD', use_clamp: bool = False):
        return NotImplemented
    
    @staticmethod
    def math_operation_binary(left, right, operation: str = 'ADD', use_clamp: bool = False):
        return NotImplemented
    
    # Add:
    def __add__(self, other):
        return self.math_operation_binary(self, other, operation = 'ADD', use_clamp = False);
    
    def __radd__(self, other):
        return self.math_operation_binary(other, self, operation = 'ADD', use_clamp = False);
    
    # Subtract:
    def __sub__(self, other):
        return self.math_operation_binary(self, other, operation = 'SUBTRACT', use_clamp = False);
    
    def __rsub__(self, other):
        return self.math_operation_binary(other, self, operation = 'SUBTRACT', use_clamp = False);
    
    # Multiply:
    def __mul__(self, other):
        return self.math_operation_binary(self, other, operation = 'MULTIPLY', use_clamp = False);
    
    def __rmul__(self, other):
        return self.math_operation_binary(other, self, operation = 'MULTIPLY', use_clamp = False);
    
    # Divide:
    def __div__(self, other):
        return self.math_operation_binary(self, other, operation = 'DIVIDE', use_clamp = False);
    
    def __rdiv__(self, other):
        return self.math_operation_binary(other, self, operation = 'DIVIDE', use_clamp = False);
    
    def __truediv__(self, other):
        return self.math_operation_binary(self, other, operation = 'DIVIDE', use_clamp = False);
    
    def __rtruediv__(self, other):
        return self.math_operation_binary(other, self, operation = 'DIVIDE', use_clamp = False);
    
    # Modulo:
    def __mod__(self, other):
        return self.math_operation_binary(self, other, operation = 'MODULO', use_clamp = False);
    
    def __rmod__(self, other):
        return self.math_operation_binary(other, self, operation = 'MODULO', use_clamp = False);
    
    # Power:
    def __pow__(self, other):
        return self.math_operation_binary(self, other, operation = 'POWER', use_clamp = False);
    
    def __rpow__(self, other):
        return self.math_operation_binary(other, self, operation = 'POWER', use_clamp = False);
    
    # Unary operations:
    def __abs__(self):
        return self.math_operation_unary(self, other, operation = 'ABSOLUTE', use_clamp = False);
    
    def __neg__(self):
        return self.math_operation_binary(-1.0, self, operation = 'MULTIPLY', use_clamp = False);
    
    def __round__(self):
        return self.math_operation_unary(self, operation = 'ROUND', use_clamp = False);
    
    def __trunc__(self):
        return self.math_operation_unary(self, operation = 'TRUNC', use_clamp = False);
    
    def __floor__(self):
        return self.math_operation_unary(self, operation = 'FLOOR', use_clamp = False);
    
    def __ceil__(self):
        return self.math_operation_unary(self, operation = 'CEIL', use_clamp = False);


class Vector(AbstractTensor):
    """A mathematics operation in a Geometry Node tree. Maps to a "Math" node."""
    
    def __init__(self, node_tree: bpy.types.NodeTree = None, socket_reference: bpy.types.NodeSocket = None, layer: int = 0):
        super().__init__(node_tree, socket_reference, layer)
    
    @staticmethod
    def math_operation_unary(input, operation: str = 'ADD', use_clamp: bool = False):
        #math_node = input.node_tree.nodes.new('ShaderNodeVectorMath')
        math_node, layer = input.new_node([input], 'ShaderNodeVectorMath')
        math_node.operation = operation
        
        input.node_tree.links.new(left.socket_reference, math_node.inputs[0])
        
        return Vector(input.node_tree, math_node.outputs[0], layer)
    
    @staticmethod
    def math_operation_binary(left, right, operation: str = 'ADD', use_clamp: bool = False):
        if isinstance(right, left.__class__):
            #math_node = left.node_tree.nodes.new('ShaderNodeVectorMath')
            math_node, layer = left.new_node([left, right], 'ShaderNodeVectorMath')
            math_node.operation = operation
            
            left.node_tree.links.new(left.socket_reference, math_node.inputs[0])
            left.node_tree.links.new(right.socket_reference, math_node.inputs[1])
            
            return Vector(left.node_tree, math_node.outputs[0], layer)
        
        elif isinstance(right, float):
            #math_node = left.node_tree.nodes.new('ShaderNodeVectorMath')
            math_node, layer = left.new_node([left], 'ShaderNodeVectorMath')
            math_node.operation = operation
            math_node.inputs[1].default_value = right
            
            left.node_tree.links.new(left.socket_reference, math_node.inputs[0])
            
            return Vector(left.node_tree, math_node.outputs[0], layer)
        
        elif isinstance(left, float):
            #math_node = right.node_tree.nodes.new('ShaderNodeVectorMath')
            math_node, layer = right.new_node([right], 'ShaderNodeVectorMath')
            math_node.operation = operation
            math_node.inputs[0].default_value = left
            
            right.node_tree.links.new(right.socket_reference, math_node.inputs[1])
            
            return Vector(right.node_tree, math_node.outputs[0], layer)
        
        else:
            return NotImplemented


class Scalar(AbstractTensor):
    """A mathematics operation in a Geometry Node tree. Maps to a "Math" node."""
    
    def __init__(self, node_tree: bpy.types.NodeTree = None, socket_reference: bpy.types.NodeSocket = None, layer: int = 0):
        super().__init__(node_tree, socket_reference, layer)
    
    @staticmethod
    def math_operation_unary(input, operation: str = 'ADD', use_clamp: bool = False):
        #math_node = input.node_tree.nodes.new('ShaderNodeMath')
        math_node, layer = input.new_node([input], 'ShaderNodeMath')
        math_node.operation = operation
        math_node.use_clamp = use_clamp
        
        input.node_tree.links.new(left.socket_reference, math_node.inputs[0], layer)
        
        return Scalar(input.node_tree, math_node.outputs[0], layer)
    
    @staticmethod
    def math_operation_binary(left, right, operation: str = 'ADD', use_clamp: bool = False):
        if isinstance(right, left.__class__):
            #math_node = left.node_tree.nodes.new('ShaderNodeMath')
            math_node, layer = left.new_node([left, right], 'ShaderNodeMath')
            math_node.operation = operation
            math_node.use_clamp = use_clamp
            
            left.node_tree.links.new(left.socket_reference, math_node.inputs[0])
            left.node_tree.links.new(right.socket_reference, math_node.inputs[1])
            
            return Scalar(left.node_tree, math_node.outputs[0], layer)
        
        elif isinstance(right, float):
            #math_node = left.node_tree.nodes.new('ShaderNodeMath')
            math_node, layer = left.new_node([left], 'ShaderNodeMath')
            math_node.operation = operation
            math_node.use_clamp = use_clamp
            math_node.inputs[1].default_value = right
            
            left.node_tree.links.new(left.socket_reference, math_node.inputs[0])
            
            return Scalar(left.node_tree, math_node.outputs[0], layer)
        
        elif isinstance(left, float):
            #math_node = right.node_tree.nodes.new('ShaderNodeMath')
            math_node, layer = right.new_node([right], 'ShaderNodeMath')
            math_node.operation = operation
            math_node.use_clamp = use_clamp
            math_node.inputs[0].default_value = left
            
            right.node_tree.links.new(right.socket_reference, math_node.inputs[1])
            
            return Scalar(right.node_tree, math_node.outputs[0], layer)
        
        else:
            return NotImplemented


class Scalar(AbstractTensor):
    """A mathematics operation in a Geometry Node tree. Maps to a "Math" node."""
    
    def __init__(self, node_tree: bpy.types.NodeTree = None, socket_reference: bpy.types.NodeSocket = None, layer: int = 0):
        super().__init__(node_tree, socket_reference, layer)
    
    @staticmethod
    def math_operation_unary(input, operation: str = 'ADD', use_clamp: bool = False):
        #math_node = input.node_tree.nodes.new('ShaderNodeMath')
        math_node, layer = input.new_node([input], 'ShaderNodeMath')
        math_node.operation = operation
        math_node.use_clamp = use_clamp
        
        input.node_tree.links.new(left.socket_reference, math_node.inputs[0], layer)
        
        return Scalar(input.node_tree, math_node.outputs[0], layer)
    
    @staticmethod
    def math_operation_binary(left, right, operation: str = 'ADD', use_clamp: bool = False):
        if isinstance(right, left.__class__):
            #math_node = left.node_tree.nodes.new('ShaderNodeMath')
            math_node, layer = left.new_node([left, right], 'ShaderNodeMath')
            math_node.operation = operation
            math_node.use_clamp = use_clamp
            
            left.node_tree.links.new(left.socket_reference, math_node.inputs[0])
            left.node_tree.links.new(right.socket_reference, math_node.inputs[1])
            
            return Scalar(left.node_tree, math_node.outputs[0], layer)
        
        elif isinstance(right, float):
            #math_node = left.node_tree.nodes.new('ShaderNodeMath')
            math_node, layer = left.new_node([left], 'ShaderNodeMath')
            math_node.operation = operation
            math_node.use_clamp = use_clamp
            math_node.inputs[1].default_value = right
            
            left.node_tree.links.new(left.socket_reference, math_node.inputs[0])
            
            return Scalar(left.node_tree, math_node.outputs[0], layer)
        
        elif isinstance(left, float):
            #math_node = right.node_tree.nodes.new('ShaderNodeMath')
            math_node, layer = right.new_node([right], 'ShaderNodeMath')
            math_node.operation = operation
            math_node.use_clamp = use_clamp
            math_node.inputs[0].default_value = left
            
            right.node_tree.links.new(right.socket_reference, math_node.inputs[1])
            
            return Scalar(right.node_tree, math_node.outputs[0], layer)
        
        else:
            return NotImplemented


class GeometryFunction():
    """Generate geometry node trees. Corresponds to a Geometry Nodes tree."""
    
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
        
        self.group_input = self.node_tree.nodes.new('NodeGroupInput')
        self.group_output = self.node_tree.nodes.new('NodeGroupOutput')
    
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
        
        socket = Vector(self.node_tree, self.group_input.outputs[self.input_counter])
        
        self.input_counter += 1
        
        return socket
    
    # Adding group outputs:
    def OutputGeometry(self):
        return self.node_tree.outputs.new('NodeSocketGeometry', 'Geometry')
    
    def OutputVector(self, variable, name: str):
        return
    
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

        vector2 = vector1 + vector1
        
        

