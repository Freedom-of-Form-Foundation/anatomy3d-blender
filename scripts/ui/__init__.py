#!/usr/bin/python3

"""Contains all user interface elements for the Blender plugin."""

from . import bone_properties


def register_all():
    bone_properties.register()
    print("Registered scripts.ui")


def unregister_all():
    bone_properties.unregister()
    print("Unregistered scripts.ui")
