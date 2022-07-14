import bpy
from bpy.types import NodeTree, Node, NodeSocket


# Defines the side panel for the node graph, can place all sorts of buttons and things here if needed.
class NODE_FFF_SIDEPANEL(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "FFF Proof of Concept"
    bl_idname = "NODE_FFF_MAINPANEL"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "FFF Tools"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("mesh.primitive_cube_add")
        row.operator("node.example_fff_node")


# Defines a new button that simply adds an example node to the current graph.
# As this is what Blender calls an "operator", this button can take the form of
# many different Blender UI elements. We're not restricted to a simple button
# and can be placed in different places if need be.
class NODE_FFF_EXAMPLE_BUTTON(bpy.types.Operator):
    bl_label = "Add Node"
    bl_idname = "node.example_fff_node"

    def execute(self, context):
        bpy.ops.node.add_node(type="FFFExampleNode", use_transform=False)
        return {'FINISHED'}


# Defines a Node Tree that contains all of our special FFF nodes. Basically gives us a blank
# canvas to add any node we need.
class NODE_FFF_TREE(NodeTree):
    bl_idname = "FFFNode"
    bl_label = "Anatomy Node Editor"
    bl_icon = 'NODETREE'


# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class NODE_FFF_TREE_NODE:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'FFFNode'


# Defines a custom "socket" which is essentially a plug/variable that exists on the node itself.
# This is based on the example that blender give us.
class NODE_FFF_EXAMPLE_SOCKET(NodeSocket):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'FFFSocket'
    bl_label = "Custom Node Socket"

    # Enum items list
    my_items = (
        ('DOWN', "Down", "Where your feet are"),
        ('UP', "Up", "Where your head should be"),
        ('LEFT', "Left", "Not right"),
        ('RIGHT', "Right", "Not left"),
    )

    my_enum_prop: bpy.props.EnumProperty(
        name="Direction",
        description="Just an example",
        items=my_items,
        default='UP',
    )

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "my_enum_prop", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)


# Defines a really basic custom node with a changeable input and a few outputs.
class NODE_FFF_BASIC_EXAMPLE_NODE(Node, NODE_FFF_TREE_NODE):
    bl_idname = 'FFFBasicExampleNode'
    bl_label = 'Basic Node'
    bl_icon = 'CUBE'

    def init(self, context):
        self.inputs.new('NodeSocketVector', "Vector")

        self.outputs.new('NodeSocketColor', "Color")
        self.outputs.new('NodeSocketFloat', "Float")


# Defines a custom node with a bunch of fancy features like custom properties and custom sockets.
class NODE_FFF_EXAMPLE_NODE(Node, NODE_FFF_TREE_NODE):
    bl_idname = 'FFFExampleNode'
    bl_label = "Custom Node"
    bl_icon = 'SOUND'

    # === Custom Properties ===
    # These work just like custom properties in ID data blocks
    # Extensive information can be found under
    # http://wiki.blender.org/index.php/Doc:2.6/Manual/Extensions/Python/Properties
    my_string_prop: bpy.props.StringProperty()
    my_float_prop: bpy.props.FloatProperty(default=3.1415926)

    def init(self, context):
        self.inputs.new('FFFSocket', "Hello")
        self.inputs.new('NodeSocketFloat', "World")
        self.inputs.new('NodeSocketVector', "!")

        self.outputs.new('NodeSocketColor', "How")
        self.outputs.new('NodeSocketColor', "are")
        self.outputs.new('NodeSocketFloat', "you")

    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        print("Removing node ", self, ", Goodbye!")

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        layout.label(text="Node settings")
        layout.prop(self, "my_float_prop")

    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "my_float_prop")
        # my_string_prop button will only be visible in the sidebar
        layout.prop(self, "my_string_prop")

    # Optional: custom label
    # Explicit user label overrides this, but here we can define a label dynamically
    def draw_label(self):
        return "Anatomy Thing"


import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem


class ExampleCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'FFFNode'


# all categories in a list
node_categories = [
    ExampleCategory('SOMENODES', "Example Nodes", items=[
        NodeItem("FFFBasicExampleNode"),
        NodeItem("FFFExampleNode"),
    ]),
]

classes = {
    NODE_FFF_SIDEPANEL,
    NODE_FFF_EXAMPLE_BUTTON,
    NODE_FFF_EXAMPLE_SOCKET,
    NODE_FFF_EXAMPLE_NODE,
    NODE_FFF_BASIC_EXAMPLE_NODE,
    NODE_FFF_TREE,
}


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    nodeitems_utils.register_node_categories('FFF_NODES', node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories('FFF_NODES')

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
