# Geoscript addon
Geoscript is the placeholder name for a new addon that will act as a code-based wrapper
around Geometry Nodes. This would allow us to write geometry generators and modifiers
as code, rather than as opaque `.blend` binary files. This commit adds the classes that
handle arithmetic operations and will generate the node tree from a piece of
developer-written code.

## Using this plugin

You can write new geometry scripts by subclassing the class `GeometryFunction`.
`GeometryFunction` will internally handle the creation of a node tree, such that you
don't need to worry about that when you write it yourself.

```python3
class ExampleFunction(GeometryFunction):
    """This is an example Geoscript object"""

    def __init__(self, name: str):
        super().__init__(name)

        # Here goes your Geoscript code.
```

Each Geoscript object is, in essence, just a wrapper around Geometry Nodes. Within
the `__init__` method, we can add our code. This code will only be run once, when
the object is created. The code you write does not get executed when Blender
applies a modifier. Instead, the code you write will be 'compiled' into Blender's
native Geometry Nodes and that is what gets executed. Even so, writing Geoscript
functions should feel quite similar to writing normal functions! There's no need
to keep track of nodes, you simply write the logic you want to write.

Blender will not know of the existence of your Geoscript object until you
instantiate the class. You can do that as follows:

```python3
test_geometry_modifier = ExampleFunction('test_geometry_modifier')
```

This will construct the Geometry Nodes based on the Geoscript `ExampleFunction`,
and register the Geometry Nodes tree under the name `'test_geometry_modifier'` in
the active .blend file when run in Blender.

**Note:** Any existing Geometry Nodes tree with the same name as given as a
parameter value in the constructor of a `GeometryFunction` will be overwritten
entirely. Make sure you give your Geometry Node trees unique names.

### Adding inputs to our function
Like a true function, a Geoscript object must have inputs and outputs as well. We
must first define our inputs and outputs. These will be visible to the user of
the software as well, so you can add a descriptive name string and tooltips
during the creation of the inputs and outputs. An example of a good Geoscript
input would be a parameter that the user is meant to manipulate, such as the
width of a bone as a scalar value.

We can add such inputs by calling `GeometryFunction.Input<Type>()`, where `<Type>`
must be replaced by the appropriate variable type.

For example, you can add a `geometry`-type input by adding the following line to
our `__init__` function:
```python3
        main_input = self.InputGeometry()
```
A reference to the input variable will be stored in `main_input`, so that you can
use the input in later calculations. Calling this function will also add an input
to the user interface.

**Note:** Every Geoscript that is to be used as a modifier in Blender must have a list
of inputs that start with one of type `Geometry`, as well as a list of outputs that
starts with one of type `Geometry`. Otherwise, the Geoscript will not function as
a modifier. For Geoscripts that will be used as smaller, reusable components do not
have this constraint.

We can add other types of inputs as well, like this:
```python3
        user_editable_input1 = self.InputFloat('Width of a bone')
```
You can specify a user-readable name for the input, as this input will also be displayed
in the user interface upon creation.

### Doing calculations using our inputs
Now that we have our inputs, we can begin to manipulate our inputs. You can use the
object returned by `InputFloat` as if they were of type `float`, and similarly you
can use objects returned by `InputVector` as if they were 3D vectors. For example,
you can do this:
```python3
class ExampleFunction(GeometryFunction):
    """Add tubercules to bones"""

    def __init__(self, name: str):
        super().__init__(name)

        # Add new nodes to the tree:
        input = self.InputGeometry()
        variable = self.InputFloat('Float Input')
        vector1 = self.InputVector('Vector Input')

        variable2 = variable + 3.0
        variable3 = variable2 + variable
        variable4 = 4.0 + variable2
        variable5 = variable + (3.0 + 2.0) * variable

        vector2 = vector1 + vector1
```

### Adding outputs
After we have done our calculations, we want to return the values to exit the function.
This can be done by defining outputs.

<Note: work in progress.>

## Full code example
```python3
class ExampleFunction(GeometryFunction):
    """Add tubercules to bones"""

    def __init__(self, name: str):
        super().__init__(name)

        # Add new nodes to the tree:
        input = self.InputGeometry()
        output = self.OutputGeometry()
        variable = self.InputFloat('Float Input')
        vector1 = self.InputVector('Vector Input')

        variable2 = variable + 3.0
        variable3 = variable2 + variable
        variable4 = 4.0 + variable2
        variable5 = variable + (3.0 + 2.0) * variable

        vector2 = vector1 + vector1
```

## How does it work?

This plugin works as follows:

Each arithmetic type, such as a Float or a Vector, is represented as a class. The arithmetic operators, such as `+`, `-`, `*` or `/` are implemented in these classes. The overloaded operators do not perform any calculations when they're called, instead they generate the appropriate piece of the node tree that represents the mathematical operation. In essence, the code is 'compiled' while you write it, and not executed until Blender uses it internally. As a result, there is no need to worry about performance in this code, since none of the code is run once the graph has built and the geometry modifier is run.

This commit introduces the types `Scalar` and `Vector`, which are the main types that are used for most operations in a node tree. These classes inherit from `AbstractSocket`, and `AbstractTensor`, which are classes that handle the general functionality of variables inside Geoscript code. This commit also introduces the class `GeometryFunction`, which is the main entry point that developers can subclass to implement their own custom Geoscript functions. A `GeometryFunction` takes the role of a Geometry Nodes tree, but instead written in code form.
