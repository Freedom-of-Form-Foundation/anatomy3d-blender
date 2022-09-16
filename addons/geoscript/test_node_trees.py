#!/usr/bin/python3

import bpy

from .geoscript import *
from .types import *
from .math import *
import math as constants

class LERP(GeometryNodeTree):
    """Linear interpolation of vectors."""
    
    def __init__(self, name: str):
        super().__init__(name)
        
        # Inputs:
        vector1 = self.InputVector('Vector 1')
        vector2 = self.InputVector('Vector 2')
        mix = self.InputFloat('Mix')
        
        # Code:
        output = (1.0 - mix) * vector1 + mix * vector2
        
        # Outputs:
        self.OutputVector(output, 'Vector')


class NormalDistribution(GeometryNodeTree):
    """The normal distribution function, also known as a bell curve."""
    
    def __init__(self, name: str):
        super().__init__(name)
        
        # Inputs:
        x = self.InputFloat('x')
        mu = self.InputFloat('mu')
        sigma = self.InputFloat('sigma')
        
        # Code:
        exponent = (x-mu)/sigma
        output = 1.0/(sigma * constants.sqrt(2.0*constants.pi)) * exp(-0.5*(exponent*exponent))
        
        # Outputs:
        self.OutputFloat(output, 'Normal Distribution')


class ExampleFunction(GeometryNodeTree):
    """Add tubercules to bones"""
    
    def __init__(self, name: str):
        super().__init__(name)
        
        normal_distribution = NormalDistribution('common.normal_distribution')
        
        # Add new nodes to the tree:
        input = self.InputGeometry()
        variable = self.InputFloat('Float Input')
        vector1 = self.InputVector('Vector Input')
        
        variable2 = variable + 3.0
        variable3 = variable2 + variable
        variable4 = 4.0 + variable2
        variable5 = variable + (3.0 + 2.0) * variable

        vector2 = 2.0 * vector1
        
        variable6 = vector2.y + variable3
        variable7 = vector2.x + 2.0
        
        #normal_distribution(self.node_tree)
        
        variable9 = map_range(1.0, 2.0, variable2, 0.0, 1.0)
        
        vector3 = map_range_vector(vector2, vector2, vector1, vector2, vector2)
        
        variable8 = clamp(min(multiply_add(variable4, variable3, variable5), variable2))
        
        geometry2 = input.move_vertices(offset = vector2)
        
        self.OutputGeometry(geometry2, 'Output Geometry')
        self.OutputFloat(variable8, 'Float Output Name', attribute_domain = 'POINT', default_value = 0.5)
