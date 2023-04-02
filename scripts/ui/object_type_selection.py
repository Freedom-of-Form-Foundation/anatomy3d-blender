#!/usr/bin/python3

from typing import Any
import bpy


class OPERATOR_(bpy.types.Operator):
    """Move items up and down, add and remove"""

    bl_idname = "ARF_edit_bones"
    bl_label = "Bone Edit Mode"
    bl_description = "Change the view to edit bones."
    bl_options = {"REGISTER"}

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        self.report({"INFO"}, "Enabling Bone Edit Mode.")
        for key, obj in enumerate(context.scene.objects):
            if obj.type == 'MESH':
                obj.hide_select = False
        return {"FINISHED"}


class VIEW_3D_PT_ARF_Properties(bpy.types.Panel):
    """Creates a Panel in the 3d view window"""

    bl_label = "ARF: Properties"
    bl_space_type = "VIEW_3D"
    bl_category = "Bone Properties"
    bl_region_type = "UI"

    def draw(self, context: bpy.types.Context):
        layout = self.layout

        scene = context.scene
        obj = context.object

        row = layout.row()
        row.label(text="Bone geometry constraints", icon="CONSTRAINT_BONE")

        row = layout.row()
        row.operator("geoscript.run_tests")

        # Create bone length slider:
        row = layout.row()
        armature: bpy.types.Armature = bpy.data.armatures["Armature"]
        for key, data in enumerate(armature.edit_bones):
            print(key, data)
        selected_bl_bone: bpy.types.EditBone = armature.edit_bones[obj.ARF_linked_bone]
        row.prop(selected_bl_bone, "length", text="Bone length")

        row = layout.row()
        row.template_list(
            "UI_UL_BoneModifiers",
            "Object Modifiers",
            obj,  # type: ignore
            "custom",
            obj,  # type: ignore
            "custom_index",
            rows=1,
        )

        col = row.column(align=True)
        add = col.operator("custom.list_action", icon="ADD", text="")
        add.action = "ADD"
        col.operator("custom.list_action", icon="REMOVE", text="").action = "REMOVE"
        col.separator()
        col.operator("custom.list_action", icon="TRIA_UP", text="").action = "UP"
        col.operator("custom.list_action", icon="TRIA_DOWN", text="").action = "DOWN"

        row = layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator("geoscript.run_tests", icon="LINENUMBERS_ON")
        row = col.row(align=True)
        row.operator("geoscript.run_tests", icon="VIEW3D", text="Select Item")
        row.operator("geoscript.run_tests", icon="GROUP", text="Select all Items")
        row = col.row(align=True)
        row.operator("geoscript.run_tests", icon="X")
        row.operator("geoscript.run_tests", icon="GHOST_ENABLED")


class CUSTOM_colorCollection(bpy.types.PropertyGroup):
    # name: StringProperty() -> Instantiated by default
    id = bpy.props.IntProperty()


def register():
    bpy.utils.register_class(UI_UL_BoneModifiers)
    bpy.utils.register_class(VIEW_3D_PT_ARF_Properties)
    bpy.utils.register_class(CUSTOM_colorCollection)
    bpy.utils.register_class(CUSTOM_OT_list_action)
    print("Registered scripts.ui.bone_properties")

    # Custom scene properties
    bpy.types.Object.custom = bpy.props.CollectionProperty(type=CUSTOM_colorCollection)
    bpy.types.Object.custom_index = bpy.props.IntProperty()
    bpy.types.Object.ARF_linked_bone = bpy.props.StringProperty()

    #bpy.types.Bone.length_property = bpy.props.FloatProperty()


def unregister():
    bpy.utils.unregister_class(UI_UL_BoneModifiers)
    bpy.utils.unregister_class(VIEW_3D_PT_ARF_Properties)
    bpy.utils.unregister_class(CUSTOM_colorCollection)
    bpy.utils.unregister_class(CUSTOM_OT_list_action)
    print("Unregistered scripts.ui.bone_properties")

    del bpy.types.Object.custom
    del bpy.types.Object.custom_index
    del bpy.types.Object.ARF_linked_bone

    #del bpy.types.Bone.length_property
