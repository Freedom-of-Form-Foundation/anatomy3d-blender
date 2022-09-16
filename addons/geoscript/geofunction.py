#!/usr/bin/python3

import bpy

from .geoscript import *
from .types import *
from .math import *
import math as constants

class GeometryNodeFunction(GeometryNodeTree):
    """A wrapper to create geometry node trees."""
    
    def __init__(self, name: str):
        super().__init__(name)
    
    def __call__(self, *args, **kwargs):
        # Add group node to node tree:
        node_tree, node, layer = AbstractSocket.new_node(
            [*args],
            'GeometryNodeGroup')
        
        # Set node group to the node tree defined in this object: 
        node.node_tree = bpy.data.node_groups[self.get_registered_name()]
        
        # Connect the arguments to the inputs of the new node:
        index = 0
        for socket in args:
            AbstractSocket.connect_argument(node_tree, socket, index, node)
            index = index + 1
        
        # Return a handle or tuple of handles of the node's outputs:
        #for output in node.outputs:
        return Scalar(node_tree, node.outputs[0], layer)


def geometry_function(f):
    """Function decorator that generates a geoscript."""
    
    def _geometry_function(*args, **kwargs):
        
        inputs = []
        
        # Register a new GeometryNodeTree with a unique name:
        unique_name = f.__module__ + "." + f.__qualname__
        script = GeometryNodeFunction(unique_name)
        
        #TODO: Detect if the node tree already is registered.
        
        # Detect the required node inputs from the function's arguments list:
        print(f.__annotations__)
        for name in f.__annotations__:
            annotation = f.__annotations__[name]
            
            print(name, annotation)
            
            if name == 'return':
                continue
            
            # Add the node input:
            if annotation == Scalar:
                inputs.append(script.InputFloat(name))
            elif annotation == Vector3:
                inputs.append(script.InputVector(name))
            elif annotation == Geometry:
                inputs.append(script.InputGeometry(name))
            else:
                raise TypeError("Geometry functions must have arguments"
                    " of type Scalar, Vector3, Geometry. Arguments of"
                    " type {} are not supported.".format(annotation))
        
        # TODO: Raise error when there is an argument that isn't annotated.
        
        # Generate the node tree:
        output = f(*inputs)
        
        # Add the node output:
        if isinstance(output, Scalar):
            script.OutputFloat(output, name)
        elif isinstance(output, Vector3):
            script.OutputVector(output, name)
        elif isinstance(output, Boolean):
            script.OutputBoolean(output, name)
        elif isinstance(output, Geometry):
            script.OutputGeometry(output, name)
        
        # Return a handle to the geometry script, which is callable. When the
        # script is called using __call__, it returns a handle to a newly
        # appended GeometryNodeGroup that refers to the node tree.
        return script(*args, **kwargs)
    
    return _geometry_function
