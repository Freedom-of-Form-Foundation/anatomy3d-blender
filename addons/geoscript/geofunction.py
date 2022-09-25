#!/usr/bin/python3

import bpy

from typing import List
from .exceptions import BlenderTypeError
from .geoscript import GeometryNodeTree
from .types import AbstractSocket, Scalar, Vector3, Boolean, Geometry


class GeometryNodeFunction(GeometryNodeTree):
    """A wrapper to create geometry node trees."""

    def __init__(self, name: str):
        super().__init__(name)

    def __call__(self, *args, **kwargs) -> None | object | List[object]:
        # Add group node to node tree:
        node = AbstractSocket.new_node([*args], "GeometryNodeGroup")

        # Set node group to the node tree defined in this object:
        bl_node = node.get_bl_node()
        if not isinstance(bl_node, bpy.types.GeometryNodeGroup):
            raise BlenderTypeError(bl_node, "bpy.types.GeometryNodeGroup")
        bl_node.node_tree = bpy.data.node_groups[self.get_registered_name()]

        # Connect the arguments to the inputs of the new node:
        for index, socket in enumerate(args):
            node.connect_argument(index, socket)

        # Return a handle or tuple of handles of the node's outputs:
        # for output in node.outputs:
        output_list: List[object] = []
        for index, output in enumerate(bl_node.outputs):
            if output.type == "VALUE":
                output_list.append(Scalar(node, index))
            elif output.type == "INT":
                output_list.append(Scalar(node, index))
            elif output.type == "BOOLEAN":
                output_list.append(Boolean(node, index))
            elif output.type == "VECTOR":
                output_list.append(Vector3(node, index))
            elif output.type == "GEOMETRY":
                output_list.append(Geometry(node, index))
            else:
                raise ValueError(
                    "Unknown output type detected while adding"
                    " node group. This is likely a bug, please report to"
                    " the developers."
                )

        if len(output_list) == 0:
            return None
        elif len(output_list) == 1:
            return output_list[0]
        else:
            return output_list


def geometry_function(f):
    """Function decorator that generates a geoscript."""

    def _geometry_function(*args, **kwargs):

        inputs = []

        # Register a new GeometryNodeTree with a unique name:
        unique_name = f.__module__ + "." + f.__qualname__
        script = GeometryNodeFunction(unique_name)

        # TODO: Detect if the node tree already is registered.

        # Detect the required node inputs from the function's arguments list:
        for name in f.__annotations__:
            annotation = f.__annotations__[name]

            if name == "return":
                continue

            # Add the node input:
            if annotation == Scalar or annotation == Scalar | float:
                inputs.append(script.InputFloat(name))
            elif annotation == Vector3:
                inputs.append(script.InputVector(name))
            elif annotation == Geometry:
                inputs.append(script.InputGeometry(name))
            else:
                raise TypeError(
                    "Geometry functions must have arguments"
                    " of type Scalar, Vector3, Geometry. Arguments of"
                    " type {} are not supported.".format(annotation)
                )

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
