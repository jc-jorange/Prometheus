from math import pi
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

from .util import props


def MaxStartVideoCheck(self, context):
    MaxVideo = self.VideoNumber
    if self.StartVideoIndex > MaxVideo:
        self.StartVideoIndex = MaxVideo


def MaxStartFrameCheck(self, context):
    MaxFrame = context.scene.frame_end
    if self.StartFrameIndex > MaxFrame:
        self.StartFrameIndex = MaxFrame


class General(PropertyGroup):
    bInPreview: BoolProperty(default=False)
    bRandomOrNot: BoolProperty(default=True)
    bNoneTrackBK: BoolProperty(default=False)
    RandomSeed: IntProperty(name="Random Seed", default=1, min=1, max=9999)
    VideoNumber: IntProperty(name='Video Amount', default=1, min=1, max=9999)
    StartVideoIndex: IntProperty(name='Start Video Index', default=1, min=1, max=9999,
                                 update=lambda self, context : MaxStartVideoCheck(self, context))
    StartFrameIndex: IntProperty(name='Start Frame Index', default=1, min=1, max=9999,
                                 update=lambda self, context : MaxStartVideoCheck(self, context))
    HDRIRoot: StringProperty(name='HDRI Background path', default='/tmp\\', subtype='DIR_PATH')

    bObjectsTrack


def AmountCheck(self, context, action):
    Max = self.MaxAmount
    Min = self.MinAmount
    if Max < Min:
        if action == 'Min':
            self.MaxAmount = Min
        elif action == 'Max':
            self.MinAmount = Max


class Objects(PropertyGroup): 
    Collections: CollectionProperty(type=props.TrackCollectionStructure)
    Index: IntProperty(default=0, min=0)
    MaxAmount: IntProperty(name="Max", default=1, min=1, max=1024,
    update=lambda self, context: AmountCheck(self, context, 'Max'))
    MinAmount: IntProperty(name="Min", default=1, min=1, max=1024,
    update=lambda self, context : AmountCheck(self, context, 'Min'))
    AppearRange: FloatProperty(name="Max spawn range", default=2, min=0.01, max=50000.0, subtype='DISTANCE')
    RandomScale: FloatProperty(name="Random scale +-", min=0, max=0.9999)


class Material(PropertyGroup):
    SelectedMesh: CollectionProperty(type=props.MaterialMeshStructure)
    Index: IntProperty(default=0, min=0)


class Light(PropertyGroup):
    PointMax: IntProperty(default=0, min=0, max=5)
    SunMax: IntProperty(default=0, min=0, max=5)
    SpotMax: IntProperty(default=0, min=0, max=5)
    AreaMax: IntProperty(default=0, min=0, max=5)
    bRandomSpec: BoolProperty(name='Random Light Specs?', default=True)
    Color: FloatVectorProperty(name="Light color", subtype='COLOR', default=[1,1,1], min=0, max=1)
    Power: FloatProperty(name='Light power', default=10.0, min=1.0, subtype='POWER')
    PointRadius: FloatProperty(name='Point Light Radius', default=0.25, min=0.0, max=100.0, subtype='DISTANCE')
    SunAngle: FloatProperty(name='Sun Light Angle', default=0.009180, min=0.0, max=pi, subtype='ANGLE')
    SpotRadius: FloatProperty(name='Spot Light Radius', default=1.0, min=0.0, max=100.0, subtype='DISTANCE')
    SpotSize: FloatProperty(name='Spot Light Size', default=pi/4, min=1.0, max=pi, subtype='ANGLE')
    SpotBlend: FloatProperty(name='Spot Light Blend', default=0.15, min=0, max=1)
    AreaSizeX: FloatProperty(name='Area Light SizeX', default=0.25, min=0.0, max=100.0, unit='LENGTH')
    AreaSizeY: FloatProperty(name='Area Light SizeY', default=0.25, min=0.0, max=100.0, unit='LENGTH')


class Camera(PropertyGroup):
    Curves: CollectionProperty(type=props.CameraCurvesStructure)
    Index: IntProperty(default=0, min=0)
    LensFocalLength: FloatProperty(name="Focal Length", default=50, min=1, max=1000, subtype='DISTANCE_CAMERA')
    bUseDoF: BoolProperty(name='Use Depth of Field?', default=False)
    FocalDistance: FloatProperty(name='Focal Distance', default=10, min=0.1, subtype='DISTANCE')
    FStop: FloatProperty(name='F-Stop', default=2.8, min=0.1, max=22)
    Blades: IntProperty(name='Blades', default=0, min=0, max=16)
    ApertureRotation: FloatProperty(name='Aperture Rotation', default=0, min=-pi, max=pi, subtype='ANGLE')
    ApertureRatio: FloatProperty(name='Aperture Ratio', default=1, min=1, max=2)
    SensorFit: EnumProperty(
        name="Sensor Fit",
        items=[
        ('AUTO', 'Auto', ''),
        ('HORIZONTAL', 'Horizontal', ''),
        ('VERTICAL', 'Vertical', ''),
        ]
    )
    SensorSize: FloatProperty(name='Size', default=36, min=1, max=100, subtype='DISTANCE_CAMERA')
    CameraNumber: IntProperty(name='Camera Amount', default=1, min=1, max=100)
    CameraMotionRange: FloatProperty(name="Camera range", default=5, min=1.0, max=50000.0, subtype='DISTANCE')
    bRandomCameraFocus: BoolProperty(name='Random Keep Focusing', default=True)
    RandomFocusCenter: FloatVectorProperty(name="Random Focus Center", default=[0, 0, 0])
    bRandomCameraRotate: BoolProperty(name='Random Rotation Follow Path', default=False)
    ComplexRate: IntProperty(name='Camera Path Complex', default=2, min=1, max=10)


class Physics(PropertyGroup):
    SelectedObject: CollectionProperty(type=props.PhysicObjectsStructure)
    Index: IntProperty(default=0, min=0)
    TimeScale: FloatProperty(name="Time scale", default=1.0, min=0.001, max=10.000)
    Substeps: IntProperty(name='Substeps Per Frame', default=10, min=1, max=1000)
    Iterations: IntProperty(name='Solver Iterations', default=10, min=10, max=100)


class Movement(PropertyGroup):
    bRandomVelVal: BoolProperty(name='Random Initial Velocity Value?', default=True)
    MaxVel: FloatProperty(name="Max Velocity", default=1, min=1, max=1024,
    update=lambda self, context: AmountCheck(self, context, 'Max Velocity'), unit='VELOCITY')
    MinVel: FloatProperty(name="Min Velocity", default=1, min=1, max=1024,
    update=lambda self, context : AmountCheck(self, context, 'Min Velocity'), unit='VELOCITY')
    InitialVelVal: FloatProperty(name="Initial Velocity", default=0.0, min=0.0, max=100.0, unit='VELOCITY')
    bRandomVelDir: BoolProperty(name='Random Initial Velocity Direction?', default=True)
    InitialVelDir: FloatVectorProperty(name="Random Initial Velocity Direction", default=[0, 0, 0])
    Curves: CollectionProperty(type=props.VelocityCurvesStructure)
    Index: IntProperty(default=0, min=0)


class Props_All(PropertyGroup):
    General: PointerProperty(type=General)
    Obj: PointerProperty(type=Objects)
    Mat: PointerProperty(type=Material)
    Light: PointerProperty(type=Light)
    Camera: PointerProperty(type=Camera)
    Physics: PointerProperty(type=Physics)
    Movement: PointerProperty(type=Movement)


AllPropClasses = [General, Objects, Material, Light, Camera, Physics, Movement, Props_All]
