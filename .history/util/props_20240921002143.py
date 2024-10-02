import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       CollectionProperty,
                       )
from bpy.types import (PropertyGroup)

class BaseUIListStructure(PropertyGroup):
    Target: PointerProperty(type=bpy.types.ID)

Register = [BaseUIListStructure]
