#!/usr/bin/python3

from typing import Sequence
from ..types import AbstractSocket, Geometry, Vector3, Scalar
import bpy


class Primitive(Geometry):
    bl_node_name = ""

    def __init__(self, inputs: Sequence[object | None]):
        self.node = AbstractSocket.add_linked_node(inputs, self.bl_node_name)


class CurveLineSegment(Primitive):
    bl_node_name = "GeometryNodeCurvePrimitiveLine"

    def __init__(self, start: Vector3, end: Vector3):
        super().__init__([start, end])
        bl_node = self.node.get_bl_node()
        assert isinstance(bl_node, bpy.types.GeometryNodeCurvePrimitiveLine)
        bl_node.mode = "POINTS"


class CurveLineDirection(Primitive):
    bl_node_name = "GeometryNodeCurvePrimitiveLine"

    def __init__(self, start: Vector3, direction: Vector3, length: Scalar | float):
        super().__init__([start, None, direction, length])
        bl_node = self.node.get_bl_node()
        assert isinstance(bl_node, bpy.types.GeometryNodeCurvePrimitiveLine)
        bl_node.mode = "DIRECTION"


class CurveCircle(Primitive):
    pass


class CurveSpiral(Primitive):
    pass


class Arc(Primitive):
    pass


class BezierSegment(Primitive):
    pass


class QuadraticBezier(Primitive):
    pass


class Quadrilateral(Primitive):
    pass


class Star(Primitive):
    pass
