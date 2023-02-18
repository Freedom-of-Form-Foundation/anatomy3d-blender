#!/usr/bin/python3

from typing import Optional
from queue import LifoQueue
import bpy

# Globals:
_node_tree_stack: LifoQueue[bpy.types.NodeTree] = LifoQueue()
_current_node_tree: Optional[bpy.types.NodeTree] = None


class GeoscriptContext():
    def __init__(self, bl_node_tree: bpy.types.NodeTree):
        self.bl_node_tree = bl_node_tree

    def __enter__(self):
        global _current_node_tree
        _node_tree_stack.put(_current_node_tree)
        _current_node_tree = self.bl_node_tree

    def __exit__(self, exception_type, value, traceback):
        global _current_node_tree
        _current_node_tree = _node_tree_stack.get()

    @staticmethod
    def get_current_bl_node_tree() -> Optional[bpy.types.NodeTree]:
        global _current_node_tree
        return _current_node_tree
