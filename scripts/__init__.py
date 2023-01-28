#!/usr/bin/python3

import bpy
from ..modules.geoscript import test_node_trees
from . import ui
from . import anatomic_types

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


def register_all():
    anatomic_types.register()
    ui.register_all()
    bpy.utils.register_class(GeoscriptTestingOperator)
    bpy.utils.register_class(TEXT_EDITOR_PT_GeoscriptTestingPanel)
    print("Registered scripts")


def unregister_all():
    ui.unregister_all()
    anatomic_types.unregister()
    bpy.utils.unregister_class(GeoscriptTestingOperator)
    bpy.utils.unregister_class(TEXT_EDITOR_PT_GeoscriptTestingPanel)
    print("Registered scripts")
