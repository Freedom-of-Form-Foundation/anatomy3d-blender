#!/usr/bin/python3


class BlenderMismatchError(Exception):
    """Raised when Blender behaves differently than what the addon expected.

    This exception usually means there is a programmer bug in the addon, or that
    Blender's API has changed."""

    def __init_(self, message):
        super().__init__(message)


class BlenderTypeError(BlenderMismatchError):
    """Raised when Blender fails to return the requested bpy.type object.

    This exception usually means there is a programmer bug in the addon, or that
    Blender's API has changed."""

    def __init_(self, received_object: object, requested_type_string: str) -> None:
        super().__init__(
            "Unexpected Blender type {} after requesting object of type {}.".format(
                received_object.__class__, requested_type_string
            )
        )
