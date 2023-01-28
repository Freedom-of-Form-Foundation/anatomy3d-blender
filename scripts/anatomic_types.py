#!/usr/bin/python3

import math
import bpy
from ..modules.geoscript import nodetrees
from ..modules.geoscript.geofunction import geometry_function
from ..modules.geoscript import types as gtype


class BlenderObjectWrapper:
    def __init__(self, bl_object: bpy.types.Object):
        self.bl_object = bl_object

    def add_geometry_modifier(
        self, geometry_script: nodetrees.GeometryNodeTree
    ) -> bpy.types.NodesModifier:
        name = geometry_script.get_registered_name()
        bl_modifier = self.bl_object.modifiers.new(name, "NODES")
        assert isinstance(bl_modifier, bpy.types.NodesModifier)
        bl_modifier.node_group = geometry_script.get_bl_tree()
        return bl_modifier


class Joint(BlenderObjectWrapper):
    def __init__(self):
        pass

    pass


class HingeJoint(Joint):

    bl_collection_name = "HingeJoint"

    def __init__(self) -> None:
        self.position = [1.0, 1.0, 1.0]
        self.rotation_start = 1.0
        self.rotation_end = 2.0
        self.inner_surface = self.InnerSurface()
        self.outer_surface = self.OuterSurface()

        @geometry_function
        def hinge_joint_modifier(geometry: gtype.Geometry) -> gtype.Geometry:
            return geometry

        modifier_tree = hinge_joint_modifier()

        self.add_geometry_modifier(modifier_tree)

    class InnerSurface(BlenderObjectWrapper):
        def __init__(self):
            self.position = [1.0, 1.0, 1.0]
            self.rotation_start = 1.0
            self.rotation_end = 2.0

    class OuterSurface(BlenderObjectWrapper):
        def __init__(self):
            self.position = [1.0, 1.0, 1.0]
            self.rotation_start = 1.0
            self.rotation_end = 2.0


class BallAndSocketJoint(Joint):
    pass


class Tubercule(BlenderObjectWrapper):
    pass


ARF_Enum_AnatomicType = [
    ("NONE", "Not an ARF object", "", "X", 0),
    ("JOINT", "Joint", "", "RESTRICT_COLOR_ON", 1),
    ("TUBERCLE", "Tubercle", "", "SHARPCURVE", 2),
    ("BONE", "Bone", "", "BONE_DATA", 3),
    ("MUSCLE", "Muscle", "", "AUTOMERGE_OFF", 4),
    ("BLOOD_VESSEL", "Blood Vessel", "", "OUTLINER_OB_GREASEPENCIL", 5),
    ("NERVE", "Nerve", "", "GP_SELECT_POINTS", 6),
    ("SKIN", "Skin", "", "MESH_CAPSULE", 7),
]


ARF_Enum_BoneGeometryConstraintType = [
    ("JOINT", "Joint", "", "RESTRICT_COLOR_ON", 1),
    ("TUBERCLE", "Tubercle", "", "SHARPCURVE", 2),
]


ARF_Enum_JointType = [
    ("HINGE", "Hinge Joint", "", "MESH_CYLINDER", 1),
    ("BALL", "Ball and Socket Joint", "", "SPHERE", 2),
    ("CONDYLOID", "Condyloid Joint", "", "META_ELLIPSOID", 3),
    ("SADDLE", "Saddle Joint", "", "PIVOT_MEDIAN", 4),
    ("PLANE", "Plane Joint", "", "LIGHT_AREA", 5),
    ("PIVOT", "Pivot Joint", "", "LIGHT_POINT", 6),
]


class ARF_HingeJointProperties(bpy.types.PropertyGroup):
    """CollectionProperty"""

    angle1: bpy.props.FloatProperty(
        name="Angle 1",
        description="The starting angle of a hingejoint.",
        min=-math.pi,
        max=math.pi,
        step=0.1 * math.pi,
    )
    angle2: bpy.props.FloatProperty(
        name="Angle 2",
        description="The ending angle of a hingejoint.",
        min=-math.pi,
        max=math.pi,
        step=0.1 * math.pi,
    )
    smoothness_angle1: bpy.props.FloatProperty(
        name="Angle 1 Smoothness",
        description="The amount of blending between the hinge joint's articular surface and the surrounding bone at the wedge's start angle.",
        min=0.0,
        max=10.0,
        step=0.1,
    )
    smoothness_angle2: bpy.props.FloatProperty(
        name="Angle 2 Smoothness",
        description="The amount of blending between the hinge joint's articular surface and the surrounding bone at the wedge's end angle.",
        min=0.0,
        max=10.0,
        step=0.1,
    )
    smoothness_cap1: bpy.props.FloatProperty(
        name="Cap 1 Smoothness",
        description="The amount of blending between the hinge joint's articular surface and the surrounding bone at the cylinder's start cap.",
        min=0.0,
        max=10.0,
        step=0.1,
    )
    smoothness_cap2: bpy.props.FloatProperty(
        name="Cap 2 Smoothness",
        description="The amount of blending between the hinge joint's articular surface and the surrounding bone at the cylinder's end cap.",
        min=0.0,
        max=10.0,
        step=0.1,
    )
    resolution_arc: bpy.props.IntProperty(
        name="Arc Resolution",
        description="The amount of subdivisions over the arc of the cylinder. Higher is more precise, lower is faster.",
        min=1,
        soft_max=32,
    )
    resolution_length: bpy.props.IntProperty(
        name="Length Resolution",
        description="The amount of subdivisions over the length of the cylinder. Higher is more precise, lower is faster.",
        min=1,
        soft_max=32,
    )


class ARF_JointProperties(bpy.types.PropertyGroup):
    """PointerProperty"""

    joint_type: bpy.props.EnumProperty(items=ARF_Enum_JointType)
    hingejoint_properties: bpy.props.PointerProperty(type=ARF_HingeJointProperties)


ARF_Enum_InnerOuterSurface = [
    ("INNER", "Inner Surface", "", "LIGHT_HEMI", 1),
    ("OUTER", "Outer Surface", "", "GIZMO", 2),
]


class ARF_BoneGeometryConstraint(bpy.types.PropertyGroup):
    """CollectionProperty"""

    constraint_type: bpy.props.EnumProperty(items=ARF_Enum_BoneGeometryConstraintType)
    constraint_object: bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, obj: (
            obj.ARF.object_type == "JOINT" or obj.ARF.object_type == "TUBERCLE"
        )
        and obj.ARF.hide_from_user is False,
    )
    inner_outer_surface: bpy.props.EnumProperty(items=ARF_Enum_InnerOuterSurface)


class ARF_BoneProperties(bpy.types.PropertyGroup):
    """PointerProperty"""

    geometry_constraints: bpy.props.CollectionProperty(type=ARF_BoneGeometryConstraint)
    geometry_constraint_index: bpy.props.IntProperty()


class ARF_GeneralObjectProperties(bpy.types.PropertyGroup):
    """PointerProperty"""

    object_type: bpy.props.EnumProperty(items=ARF_Enum_AnatomicType)
    hide_from_user: bpy.props.BoolProperty()
    bone_properties: bpy.props.PointerProperty(type=ARF_BoneProperties)


class Bone(BlenderObjectWrapper):
    def __init__(self, bl_object: bpy.types.Object):
        super().__init__(bl_object)
        self.joints: list[Joint] = []

    def add_joint(self, joint: Joint) -> None:
        self.joints.append(joint)


class Muscle(BlenderObjectWrapper):
    pass


def register():
    bpy.utils.register_class(ARF_HingeJointProperties)
    bpy.utils.register_class(ARF_JointProperties)
    bpy.utils.register_class(ARF_BoneGeometryConstraint)
    bpy.utils.register_class(ARF_BoneProperties)
    bpy.utils.register_class(ARF_GeneralObjectProperties)
    bpy.types.Object.ARF = bpy.props.PointerProperty(type=ARF_GeneralObjectProperties)
    print("Registered anatomic_types.py")


def unregister():
    bpy.utils.unregister_class(ARF_BoneGeometryConstraint)
    bpy.utils.unregister_class(ARF_BoneProperties)
    bpy.utils.unregister_class(ARF_GeneralObjectProperties)
    bpy.utils.unregister_class(ARF_HingeJointProperties)
    bpy.utils.unregister_class(ARF_JointProperties)
    del bpy.types.Object.ARF
    print("Unregistered anatomic_types.py")
