#!/usr/bin/python3

import bpy

from .geoscript import GeometryNodeTree
from .geofunction import geometry_function
from .types import Vector3, Scalar
from .raytracing import raycast_with_attribute
import math as m
from . import math as g


@geometry_function
def normal_distribution(x: Scalar, mu: Scalar, sigma: Scalar | float) -> Scalar:
    ex = (x - mu) / sigma
    return 1.0 / (sigma * m.sqrt(2.0 * m.pi)) * g.exp(-0.5 * (ex * ex))


@geometry_function
def lerp(vector1: Vector3, vector2: Vector3, mix: Scalar) -> Vector3:
    return (1.0 - mix) * vector1 + mix * vector2


class LERP(GeometryNodeTree):
    """Linear interpolation of vectors."""

    def __init__(self, name: str):
        super().__init__(name)

        # Inputs:
        vector1 = self.InputVector("Vector 1")
        vector2 = self.InputVector("Vector 2")
        mix = self.InputFloat("Mix")

        # Code:
        output = (1.0 - mix) * vector1 + mix * vector2

        # Outputs:
        self.OutputVector(output, "Vector")


class NormalDistribution(GeometryNodeTree):
    """The normal distribution function, also known as a bell curve."""

    def __init__(self, name: str):
        super().__init__(name)

        # Inputs:
        x = self.InputFloat("x")
        mu = self.InputFloat("mu")
        sigma = self.InputFloat("sigma")

        # Code:
        ex = (x - mu) / sigma
        output = 1.0 / (sigma * m.sqrt(2.0 * m.pi)) * g.exp(-0.5 * (ex * ex))

        # Outputs:
        self.OutputFloat(output, "Normal Distribution")


class ExampleFunction(GeometryNodeTree):
    """Add tubercules to bones"""

    def __init__(self, name: str):
        super().__init__(name)

        # Add new nodes to the tree:
        input = self.InputGeometry()
        variable = self.InputFloat("Float Input")
        vector1 = self.InputVector("Vector Input")
        boolean = self.InputBoolean("Boolean Input")

        # geometry.py tests:
        geo1 = input.move_vertices(vector1, vector1, boolean)
        geo2 = geo1.set_id(variable, boolean)
        position, distance = geo1.get_closest_point(vector1)
        position, distance = geo1.get_closest_edge(vector1)
        position, distance = geo1.get_closest_face(vector1)
        geo3 = geo1.transform(vector1, vector1, vector1)
        geo4, geo5 = geo3.separate_geometry(boolean)
        geo6 = geo3.get_mesh_component()
        geo7 = geo3.get_point_cloud_component()
        geo8 = geo3.get_curve_component()
        geo9 = geo8.get_volume_component()
        geo10 = geo9.get_instances_component()
        geo11 = geo10.merge_all_by_distance(variable, boolean)
        geo12 = geo11.merge_connected_by_distance(variable, boolean)
        geo13 = geo12.to_instances()
        geo14 = geo13.get_bounding_box_geometry()
        geo15 = geo14.get_convex_hull()
        vec1, vec2 = geo15.get_bounding_box_points()

        rayhit = raycast_with_attribute(vec1, vec2, variable, geo15, variable, "FLOAT")
        rayhit = raycast_with_attribute(vec1, vec2, variable, geo15, variable, "INT")
        rayhit = raycast_with_attribute(vec1, vec2, variable, geo15, boolean, "BOOLEAN")
        rayhit = raycast_with_attribute(
            vec1, vec2, variable, geo15, vector1, "FLOAT_VECTOR"
        )
        # rayhit = raycast(vec1, vec2, variable, geo15, None, 'FLOAT_COLOR')

        is_hit = rayhit.is_hit()
        hit_position = rayhit.hit_position()
        hit_normal = rayhit.hit_normal()
        hit_distance = rayhit.hit_distance()
        attribute = rayhit.attribute()

        variable2 = variable + 3.0
        variable3 = variable2 + variable
        variable4 = 4.0 + variable2
        variable5 = variable + (3.0 + 2.0) * variable

        vector2 = 2.0 * vector1

        variable6 = vector2.y + variable3
        variable7 = vector2.x + 2.0

        # normal_distribution(self.node_tree)

        variable9 = g.map_range(1.0, 2.0, variable2, 0.0, 1.0)

        vector3 = g.map_range_vector(vector2, vector2, vector1, vector2, vector2)

        variable8 = g.clamp(
            g.min(g.multiply_add(variable4, variable3, variable5), variable2)
        )

        geometry2 = input.move_vertices(offset=vector2)

        abc1 = normal_distribution(variable2, variable3, variable4)
        abc2 = lerp(vector1, vector2, 1.0)

        self.OutputGeometry(geometry2, "Output Geometry")
        self.OutputFloat(hit_distance, "Output Float")
        self.OutputFloat(
            variable8, "Float Output Name", attribute_domain="POINT", default_value=0.5
        )
