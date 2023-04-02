#!/usr/bin/python3

from . import scripts

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


def register():
    scripts.register_all()
    print("Registered Anatomy Re-engineering Framework Addon")


def unregister():
    scripts.unregister_all()
    print("Unregistered Anatomy Re-engineering Framework Addon")


if __name__ == "__main__":
    register()
