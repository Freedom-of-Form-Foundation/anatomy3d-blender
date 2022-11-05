#!/usr/bin/python3

import bpy

from .modules.geoscript import test_node_trees

bl_info = {
    "name": "Anatomy Re-engineering Framework",
    "author": "Freedom of Form Foundation",
    "version": (0, 0, 1),
    "blender": (3, 3, 0),
    "location": "Unknown",
    "description": "A CAD tool for humanoid anatomy alterations",
    "warning": "Experimental",
    "category": "3D View",
    "doc_url": "https://",
    "tracker_url": "https://",
}


# Define an operator (button) that allows the user to run the script:
class GeoscriptTestingOperator(bpy.types.Operator):
    """Run GeoScript test functions"""

    bl_idname = "geoscript.run_tests"
    bl_label = "Run GeoScript test functions"

    def execute(self, context):
        test_geometry_modifier = test_node_trees.ExampleFunction(
            "test_geometry_modifier"
        )
        test_normal_distribution = test_node_trees.NormalDistribution(
            "common.normal_distribution"
        )
        test_tubercule = test_node_trees.Tubercule("tubercule")
        return {"FINISHED"}


class TEXT_EDITOR_PT_GeoscriptTestingPanel(bpy.types.Panel):
    """Creates a Panel in the text editor window"""

    bl_label = "_PT_Hello World Panel"
    bl_space_type = "TEXT_EDITOR"
    bl_category = "GeoScript"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Hello world!", icon="WORLD_DATA")

        row = layout.row()
        row.operator("geoscript.run_tests")


def register():
    bpy.utils.register_class(GeoscriptTestingOperator)
    bpy.utils.register_class(TEXT_EDITOR_PT_GeoscriptTestingPanel)
    print("Registered Anatomy Re-engineering Framework Addon")


def unregister():
    bpy.utils.unregister_class(GeoscriptTestingOperator)
    bpy.utils.unregister_class(TEXT_EDITOR_PT_GeoscriptTestingPanel)
    print("Unregistered Anatomy Re-engineering Framework Addon")


if __name__ == "__main__":
    register()
