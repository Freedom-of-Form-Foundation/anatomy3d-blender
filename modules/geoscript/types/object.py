#!/usr/bin/python3

import bpy

from .abstract_socket import AbstractSocket
from .vector3 import Vector3
from .boolean import Boolean
from .geometry import Geometry


class Object(AbstractSocket):
    """Corresponds to an Object socket type in Blender's Geometry Nodes"""

    @staticmethod
    def get_bl_idnames():
        """Returns a list of Blender socket types that this class represents.

        Returns:
            List of strings corresponding to Blender Geometry Nodes socket
            types.
        """
        return ["OBJECT"]

    # "Object Info" in Blender:
    def get_geometry(
        self,
        as_instance: Boolean = None,
        relative: bool = False,
    ):
        """Get the geometry contained within this object.

        Args:
            as_instance:
                Whether to treat the object as an instanced object.
            relative:
                Whether to get the geometry in local space relative to the
                geometry that the geometry node tree acts on. Note that this
                is not (necessarily) the same geometry as what is contained in
                this object. If False, this function will retrieve the
                geometry in global space.

        Raises:
            TypeError:
                One of the arguments is of the wrong type.

        Returns:
            The geometry contained within this object.
        """
        arguments = [self, as_instance]
        node = AbstractSocket.add_linked_node(arguments, "GeometryNodeObjectInfo")
        bl_node = node.get_bl_node()
        assert isinstance(bl_node, bpy.types.GeometryNodeObjectInfo)
        bl_node.transform_space = "RELATIVE" if relative else "ORIGINAL"
        return Geometry(node, 3)

    def get_location(
        self,
        as_instance: Boolean = None,
        relative: bool = False,
    ):
        """Get the location of this object.

        Args:
            as_instance:
                Whether to treat the object as an instanced object.
            relative:
                Whether to get the geometry in local space relative to the
                geometry that the geometry node tree acts on. Note that this
                is not (necessarily) the same geometry as what is contained in
                this object. If False, this function will retrieve the
                geometry in global space.

        Raises:
            TypeError:
                One of the arguments is of the wrong type.

        Returns:
            The position vector of the object.
        """
        arguments = [self, as_instance]
        node = AbstractSocket.add_linked_node(arguments, "GeometryNodeObjectInfo")
        bl_node = node.get_bl_node()
        assert isinstance(bl_node, bpy.types.GeometryNodeObjectInfo)
        bl_node.transform_space = "RELATIVE" if relative else "ORIGINAL"
        return Vector3(node, 0)

    def get_rotation(
        self,
        as_instance: Boolean = None,
        relative: bool = False,
    ):
        """Get the Euler rotation of this object.

        Args:
            as_instance:
                Whether to treat the object as an instanced object.
            relative:
                Whether to get the geometry in local space relative to the
                geometry that the geometry node tree acts on. Note that this
                is not (necessarily) the same geometry as what is contained in
                this object. If False, this function will retrieve the
                geometry in global space.

        Raises:
            TypeError:
                One of the arguments is of the wrong type.

        Returns:
            The Euler rotation vector of the object.
        """
        arguments = [self, as_instance]
        node = AbstractSocket.add_linked_node(arguments, "GeometryNodeObjectInfo")
        bl_node = node.get_bl_node()
        assert isinstance(bl_node, bpy.types.GeometryNodeObjectInfo)
        bl_node.transform_space = "RELATIVE" if relative else "ORIGINAL"
        return Vector3(node, 1)

    def get_scale(
        self,
        as_instance: Boolean = None,
        relative: bool = False,
    ):
        """Get the scaling vector of this object.

        Args:
            as_instance:
                Whether to treat the object as an instanced object.
            relative:
                Whether to get the geometry in local space relative to the
                geometry that the geometry node tree acts on. Note that this
                is not (necessarily) the same geometry as what is contained in
                this object. If False, this function will retrieve the
                geometry in global space.

        Raises:
            TypeError:
                One of the arguments is of the wrong type.

        Returns:
            The scale vector of the object.
        """
        arguments = [self, as_instance]
        node = AbstractSocket.add_linked_node(arguments, "GeometryNodeObjectInfo")
        bl_node = node.get_bl_node()
        assert isinstance(bl_node, bpy.types.GeometryNodeObjectInfo)
        bl_node.transform_space = "RELATIVE" if relative else "ORIGINAL"
        return Vector3(node, 2)
