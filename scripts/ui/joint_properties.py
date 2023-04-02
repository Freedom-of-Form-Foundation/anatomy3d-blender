#!/usr/bin/python3

from typing import Any
import bpy


class VIEW_3D_PT_ARF_JointProperties(bpy.types.Panel):
    """Creates a Panel in the 3d view window"""

    bl_label = "ARF: Joint Properties"
    bl_space_type = "VIEW_3D"
    bl_category = "Bone Properties"
    bl_region_type = "UI"

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        obj = context.object

        obj_ARF_data = obj.ARF  # type: ignore

        layout.row().label(text="Joint properties", icon="RESTRICT_COLOR_ON")
        layout.row().label(text=obj.name)
        layout.row().prop(obj_ARF_data, "object_type", text="Object Type")

        self.draw_modifier_list(obj)

        index = obj_ARF_data.bone_properties.geometry_constraint_index
        geometry_constraints = obj_ARF_data.bone_properties.geometry_constraints

        # Don't display info if no entry is selected, i.e. index is out of bounds:
        if len(geometry_constraints) <= index:
            return

        row = layout.row()
        row.prop(geometry_constraints[index], "constraint_type", text="Type")

        row = layout.row()
        row.prop(geometry_constraints[index], "name", text="Name")

        # row = layout.row()
        # col = row.column(align=True)
        # row = col.row(align=True)
        # row.operator("geoscript.run_tests", icon="LINENUMBERS_ON")
        # row = col.row(align=True)
        # row.operator("geoscript.run_tests", icon="VIEW3D", text="Select Item")
        # row.operator("geoscript.run_tests", icon="GROUP", text="Select all Items")
        # row = col.row(align=True)
        # row.operator("geoscript.run_tests", icon="X")
        # row.operator("geoscript.run_tests", icon="GHOST_ENABLED")

    def draw_modifier_list(self, obj: bpy.types.Object) -> None:
        row = self.layout.row()
        self.draw_modifier_list_selector(row, obj)
        self.draw_modifier_list_buttons(row)

    def draw_modifier_list_selector(self, row, obj: bpy.types.Object) -> None:
        row.template_list(
            "UI_UL_BoneModifiers",
            "Object Modifiers",
            obj.ARF.bone_properties,  # type: ignore
            "geometry_constraints",
            obj.ARF.bone_properties,  # type: ignore
            "geometry_constraint_index",
            rows=1,
        )

    def draw_modifier_list_buttons(self, row) -> None:
        col = row.column(align=True)
        col.operator("custom.list_action", icon="ADD", text="").action = "ADD"
        col.operator("custom.list_action", icon="REMOVE", text="").action = "REMOVE"
        col.separator()
        col.operator("custom.list_action", icon="TRIA_UP", text="").action = "UP"
        col.operator("custom.list_action", icon="TRIA_DOWN", text="").action = "DOWN"


def register():
    bpy.utils.register_class(VIEW_3D_PT_ARF_JointProperties)
    print("Registered scripts.ui.joint_properties")


def unregister():
    bpy.utils.unregister_class(VIEW_3D_PT_ARF_JointProperties)
    print("Unregistered scripts.ui.joint_properties")
