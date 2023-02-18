#!/usr/bin/python3

from typing import Any, Optional, TYPE_CHECKING
import bpy

from ..anatomic_types import ARF_GeneralObjectProperties


class UI_UL_BoneModifiers(bpy.types.UIList):
    def draw_item(
        self,
        context: Optional[bpy.types.Context],
        layout: bpy.types.UILayout,
        data: Optional[bpy.types.AnyType],
        item: Optional[bpy.types.AnyType],
        icon: Optional[int],
        active_data: bpy.types.AnyType,
        active_propname: str,
        index: Optional[int] = 0,
        flt_flag: Optional[int] = 0,
    ) -> Any:
        """Draws an item in a collection.

        The draw_item function is called for each item of the collection that is
        visible in the list.

        Args:
            data: the RNA object containing the collection,
            item: the current drawn item of the collection,
            icon: the "computed" icon for the item (as an integer, because some objects
                like materials or textures have custom icons ID, which are not available
                as enum items).
            active_data: the RNA object containing the active property for the
                collection (i.e. integer pointing to the active item of the collection).
            active_propname: the name of the active property
                (use 'getattr(active_data, active_propname)').
            index: the index of the current item in the collection.
            flt_flag: the result of the filtering process for this item.

        Note:
            as index and flt_flag are optional arguments, you do not have to use/declare
            them here if you don't need them.
        """
        icon_name = "X"
        # if item and item.constraint_object:
        if item and hasattr(item, "constraint_object"):
            if item.constraint_object.ARF.object_type == "JOINT":
                icon_name = "RESTRICT_COLOR_ON"
            elif item.constraint_object.ARF.object_type == "TUBERCLE":
                icon_name = "SHARPCURVE"

        if self.layout_type in {"DEFAULT", "COMPACT"}:
            if item:
                layout.prop(item, "name", text="", emboss=False, icon=icon_name)
            else:
                layout.label(text="", translate=False, icon=icon_name)
        elif self.layout_type in {"GRID"}:
            layout.alignment = "CENTER"
            layout.label(text="", icon=icon_name)


class CUSTOM_OT_list_action(bpy.types.Operator):
    """Move items up and down, add and remove"""

    bl_idname = "custom.list_action"
    bl_label = "List Actions"
    bl_description = "Move items up and down, add and remove"
    bl_options = {"REGISTER"}

    enumitems = (
        ("UP", "Up", ""),
        ("DOWN", "Down", ""),
        ("REMOVE", "Remove", ""),
        ("ADD", "Add", ""),
    )

    # Hacky workaround to silence mypy false flag when using props.EnumProperty():
    if TYPE_CHECKING:
        action: bpy.types.EnumProperty
    else:
        action: bpy.props.EnumProperty(items=enumitems)

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        obj = context.object

        if not hasattr(obj, "ARF"):
            return
        assert isinstance(obj.ARF, ARF_GeneralObjectProperties)

        bone_properties = obj.ARF.bone_properties
        idx = bone_properties.geometry_constraint_index

        try:
            item = bone_properties.geometry_constraints[idx]
        except IndexError:
            pass
        else:
            if (
                self.action == "DOWN"
                and idx < len(bone_properties.geometry_constraints) - 1
            ):
                bone_properties.geometry_constraints.move(idx, idx + 1)
                bone_properties.geometry_constraint_index += 1
                info = 'Item "%s" moved to position %d' % (
                    item.name,
                    bone_properties.geometry_constraint_index + 1,
                )
                self.report({"INFO"}, info)

            elif self.action == "UP" and idx >= 1:
                bone_properties.geometry_constraints.move(idx, idx - 1)
                bone_properties.geometry_constraint_index -= 1
                info = 'Item "%s" moved to position %d' % (
                    item.name,
                    bone_properties.geometry_constraint_index + 1,
                )
                self.report({"INFO"}, info)

            elif self.action == "REMOVE":
                info = 'Item "%s" removed from list' % (
                    bone_properties.geometry_constraints[idx].name
                )
                bone_properties.geometry_constraints.remove(idx)
                bone_properties.geometry_constraint_index -= 1
                self.report({"INFO"}, info)

        if self.action == "ADD":
            if context.object:
                item = bone_properties.geometry_constraints.add()
                item.name = context.object.name
                item.obj_type = context.object.type
                item.obj_id = len(bone_properties.geometry_constraints)
                bone_properties.geometry_constraint_index = (
                    len(bone_properties.geometry_constraints) - 1
                )
                info = '"%s" added to list' % (item.name)
                self.report({"INFO"}, info)
            else:
                self.report({"INFO"}, "Nothing selected in the Viewport")
        return {"FINISHED"}


class OperatorDrawTubercle(bpy.types.Operator):
    """Go into Draw mode to draw a tubercle"""

    bl_idname = "arf_bone_mode.draw_tubercle"
    bl_label = "Go into Draw mode to draw a tubercle"

    def execute(self, context):
        bpy.ops.object.add(
            radius=1.0,
            type="CURVE",
            enter_editmode=True,
            align="WORLD",
            location=(0.0, 0.0, 0.0),
            rotation=(0.0, 0.0, 0.0),
            scale=(0.0, 0.0, 0.0),
        )
        return {"FINISHED"}


class VIEW_3D_PT_ARF_Properties(bpy.types.Panel):
    """Creates a Panel in the 3d view window"""

    bl_label = "ARF: Properties"
    bl_space_type = "VIEW_3D"
    bl_category = "Bone Properties"
    bl_region_type = "UI"

    def draw(self, context: bpy.types.Context):
        obj = context.object

        if not hasattr(obj, "ARF"):
            return
        assert isinstance(obj.ARF, ARF_GeneralObjectProperties)

        self.draw_properties_header(obj)
        self.draw_feature_drawing_buttons()
        self.draw_modifier_list(obj)
        self.draw_constraint_properties(obj.ARF)

    def draw_properties_header(self, obj: bpy.types.Object):
        assert hasattr(obj, "ARF")
        layout = self.layout
        layout.row().label(text="Bone geometry constraints", icon="CONSTRAINT_BONE")
        layout.row().label(text=obj.name)
        layout.row().prop(obj.ARF, "object_type", text="Object Type")

    def draw_feature_drawing_buttons(self):
        row = self.layout.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.operator("arf_bone_mode.draw_tubercle", icon="STROKE", text="Draw tubercle")
        row = col.row(align=True)
        row.operator(
            "arf_bone_mode.draw_tubercle",
            icon="CURVE_BEZCIRCLE",
            text="Draw muscle insertion",
        )

    def draw_modifier_list(self, obj: bpy.types.Object) -> None:
        row = self.layout.row()
        self.draw_modifier_list_selector(row, obj)
        self.draw_modifier_list_buttons(row)

    def draw_modifier_list_selector(self, row, obj: bpy.types.Object) -> None:
        if not hasattr(obj, "ARF"):
            return
        assert isinstance(obj.ARF, ARF_GeneralObjectProperties)
        row.template_list(
            "UI_UL_BoneModifiers",
            "Object Modifiers",
            obj.ARF.bone_properties,
            "geometry_constraints",
            obj.ARF.bone_properties,
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

    def draw_constraint_properties(self, obj_ARF: ARF_GeneralObjectProperties) -> None:
        index = obj_ARF.bone_properties.geometry_constraint_index
        geometry_constraints = obj_ARF.bone_properties.geometry_constraints

        # Don't display info if no entry is selected, i.e. index is out of bounds:
        if len(geometry_constraints) <= index:
            return

        item = geometry_constraints[index]
        self.layout.row().prop(item, "constraint_type", text="Type")
        self.layout.row().prop(item, "name", text="Name")
        self.layout.row().prop(item, "constraint_object", text="Constraint Object")

        if item and item.constraint_object:
            if item.constraint_object.ARF.object_type == "JOINT":
                row = self.layout.row()
                row.prop(item, "inner_outer_surface", text="Attach To...")


class CUSTOM_colorCollection(bpy.types.PropertyGroup):
    # name: StringProperty() -> Instantiated by default
    id = bpy.props.IntProperty()


def register():
    bpy.utils.register_class(OperatorDrawTubercle)
    bpy.utils.register_class(UI_UL_BoneModifiers)
    bpy.utils.register_class(VIEW_3D_PT_ARF_Properties)
    bpy.utils.register_class(CUSTOM_colorCollection)
    bpy.utils.register_class(CUSTOM_OT_list_action)
    print("Registered scripts.ui.bone_properties")

    # Custom scene properties
    bpy.types.Object.custom = bpy.props.CollectionProperty(type=CUSTOM_colorCollection)
    bpy.types.Object.custom_index = bpy.props.IntProperty()

    # bpy.types.Bone.length_property = bpy.props.FloatProperty()


def unregister():
    bpy.utils.unregister_class(UI_UL_BoneModifiers)
    bpy.utils.unregister_class(VIEW_3D_PT_ARF_Properties)
    bpy.utils.unregister_class(CUSTOM_colorCollection)
    bpy.utils.unregister_class(CUSTOM_OT_list_action)
    bpy.utils.unregister_class(OperatorDrawTubercle)
    print("Unregistered scripts.ui.bone_properties")

    del bpy.types.Object.custom
    del bpy.types.Object.custom_index

    # del bpy.types.Bone.length_property
