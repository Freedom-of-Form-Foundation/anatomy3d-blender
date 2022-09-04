#!/usr/bin/python3

import bpy

from . import geoscript

bl_info = {
    "name": "GeoScript",
    "author": "Lathreas",
    "version": (0, 0, 1),
    "blender": (3, 2, 2),
    "location": "Unknown",
    "description": "Create geometry modifiers using Python code",
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
        test_geometry_modifier = geoscript.ExampleFunction('test_geometry_modifier')
        return {'FINISHED'}


class GeoscriptTestingPanel(bpy.types.Panel):
    """Creates a Panel in the text editor window"""
    bl_label = "Hello World Panel"
    bl_space_type = 'TEXT_EDITOR'
    bl_category = 'GeoScript'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Hello world!", icon='WORLD_DATA')

        row = layout.row()
        row.operator("geoscript.run_tests")


def register():
    bpy.utils.register_class(GeoscriptTestingOperator)
    bpy.utils.register_class(GeoscriptTestingPanel)
    print("Registered GeoScript Addon")

def unregister():
    bpy.utils.unregister_class(GeoscriptTestingOperator)
    bpy.utils.unregister_class(GeoscriptTestingPanel)
    print("Unregistered GeoScript Addon")

if __name__ == "__main__":
    register()
