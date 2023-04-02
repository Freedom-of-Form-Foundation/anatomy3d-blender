#!/usr/bin/python3

"""Contains all user interface elements for the Blender plugin."""

from . import bone_properties
from . import mode_selection

def register_all():
    bone_properties.register()
    mode_selection.register()
    print("Registered scripts.ui")


def unregister_all():
    bone_properties.unregister()
    mode_selection.unregister()
    print("Unregistered scripts.ui")
