from typing import List
import bpy
from bpy.types import Panel
from . import util

bDebug = True

AllPanelClasses = []

PanelIDname = "AD_PT_"
Space_Type = "PROPERTIES"
Region_Type = "WINDOW"
Panel_Context = "output"

# All panels
# 0.AutoData: Main panel contains all sub-panels
# 1.Object: Handle the objects for categories
# 2.Material: Handle the material option for each individual object
# 3.Light: Handle the light for all sences
# 4.Camera: Handle the camera for all sences
# 5.General: All other config and final render button in here
# 6.Physics: Physics setting based on blender riged body system
# 7.Movement: Manual set objects movement

Panel_Names = ["AutoDataset", "Object", "Material", "Light", "Camera", "Physics", "Movement"]

def SignRegisterProps(order:int):
    bl_order = order 
    bl_idname = PanelIDname + Panel_Names[bl_order]
    bl_label = Panel_Names[bl_order]
    bl_parent_id = PanelIDname + Panel_Names[0]
    return bl_order, bl_idname, bl_label, bl_parent_id

def ButtonProps(
    button, 
    action: str,
    panel_name: str,
    structure_name: str,
    idx_name: str,
    type: str,
    bObj = True
    ):

    button.action = action
    button.panel_name = panel_name
    button.structure_name = structure_name
    button.idx_name = idx_name
    button.type = type
    button.bObj = bObj

def SubPropsShow(
    SelectedSturcture, 
    SelectedIndex, 
    layout:bpy.types.UILayout, 
    props_list: List[str],
    ):

    try: 
        item = SelectedSturcture[SelectedIndex]
    except IndexError:
        pass
    else:
        column = layout.column(align=True)
        for each_attribute in props_list:
            column.prop(item, each_attribute)

# Base Class
class P_Master(Panel):
    bl_space_type = Space_Type
    bl_region_type = Region_Type
    bl_context = Panel_Context

    @classmethod
    def poll(self, context):
        return context.mode == "OBJECT"
    
    def __init__(self) -> None:
        super().__init__()
        self.context = bpy.context
        self.scene = self.context.scene
        self.render = self.scene.render
        self.Props_All = self.scene.P_S

        self.props_general = self.Props_All.General 
        self.props_obj = self.Props_All.Obj
        self.props_mat = self.Props_All.Mat
        self.props_light = self.Props_All.Light
        self.props_camera = self.Props_All.Camera
        self.props_physics = self.Props_All.Physics
        self.props_movement = self.Props_All.Movement

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.enabled = not self.props_general.bInPreview

        if bDebug:
            layout.label(text="! DEBUGING !")

# Main Panel
class P_General(P_Master):

# Props:
# Random or not (boolean)
# Random seed (int)
# HDRI files (path)
# Number of videos (int)
# Warning: output and render seting will direcly use the blender seting. 
# If you want to do some changes you should change them in those panels.

    bl_order, bl_idname, bl_label, _ = SignRegisterProps(0)

    def draw(self, context):
        super().draw(context)

        layout = self.layout
        layout.enabled = True

        if self.props_general.bInPreview:
            column_back = layout.column()
            column_back.operator('ad.action', icon='SCREEN_BACK', text='Back From Preview').action = 'BACK'

        column = layout.column()
        column.enabled = not self.props_general.bInPreview
        row = column.row(align=True)
        row.operator_context = 'INVOKE_DEFAULT'
        row.operator('ad.action', icon='OUTPUT', text='Render').action = 'RENDER'
        row.operator('ad.action', icon='VIEWZOOM', text='Preview').action = 'PREVIEW'

        column.prop(self.props_general, "RandomSeed")
        column.prop(self.props_general, 'VideoNumber')

        column.prop(self.props_general, 'StartVideoIndex')
        column.prop(self.props_general, 'StartFrameIndex')

        row = column.row(align=True)
        row.label(icon='WORLD')
        row.prop(self.props_general, 'HDRIRoot')

        column.prop(self.props_general, "bRandomOrNot", text="Random generation?")
        column.prop(self.props_general, "bNoneTrackBK", text="Non-track as background?")

        column.label(text=
        "Choose output annotation."
        )
        column.prop(self.props_general, "bObjectsTrack")
        subcolumn = 

        column.label(text=
        "Output and render seting will direcly use the blender seting."
        )

# Object Panel
class P_Object(P_Master):

# Props:
# Define which objects to track (collection select)
# Objects max and min number (int)
# Objects appear range (float)
# Object scale random (float)
# Physical or not (boolean)
# Initial speed (float)

    bl_order, bl_idname, bl_label, bl_parent_id = SignRegisterProps(1)

    def __init__(self) -> None:
        super().__init__()
        bpy.ops.ad_util.sync_collecetions()

    def draw(self, context):
        super().draw(context)

        layout = self.layout

        layout.label(text="Select collection as class to Track")
        layout.template_list(util.ui.UL_SelectedCollections.bl_idname, "UL_OBJ", 
                            bpy.data, "collections", 
                            self.props_obj, "Index",  
                            )
        
        column = layout.column(align=True)
        column.prop(self.props_obj, "MaxAmount", text='Amount Max')
        column.prop(self.props_obj, "MinAmount", text='Min')

        layout.separator_spacer()
        layout.prop(self.props_obj, "AppearRange")
        layout.prop(self.props_obj, "RandomScale")


# Material Panel
class P_Material(P_Master):

# Props:
# Random material selelct (object select)
# Random base PBR material (material parameter)

    bl_order, bl_idname, bl_label, bl_parent_id = SignRegisterProps(2)

    def __init__(self) -> None:
        super().__init__()
        bpy.ops.ad_util.list_check(
            panel_name='Mat',
            structure_name='SelectedMesh',
            idx_name='Index',
            type_name='MESH',
            bObj=True,
        )

    def draw(self, context):
        super().draw(context)

        layout = self.layout
        self.bFound = True

        row = layout.row()
        row.template_list(util.ui.UL_SelectedObjects.bl_idname,
                          'UL_Mat',
                          self.props_mat, 'SelectedMesh',
                          self.props_mat, 'Index')

        col = row.column(align=True)
        button = col.operator('ad_util.list_action', icon='ADD', text='')
        ButtonProps(button, 'ADD', 'Mat', 'SelectedMesh', 'Index', 'MESH')
        button = col.operator('ad_util.list_action', icon='REMOVE', text='')
        ButtonProps(button, 'REMOVE', 'Mat', 'SelectedMesh', 'Index', 'MESH')

        self.bFound = SubPropsShow(
                                self.props_mat.SelectedMesh, 
                                self.props_mat.Index, 
                                layout, 
                                ['MetallicMax', 'MetallicMin', 
                                'RoughnessMax', 'RoughnessMin', 
                                'SpecularMax', 'SpecularMin',],
                                )

# Light Panel
class P_Light(P_Master): 

# Props:
# Lights max min number for each type (int)
# Lights power, transform, special parmaters (float, vector, float)
## maybe move lights?

    bl_order, bl_idname, bl_label, bl_parent_id = SignRegisterProps(3)

    def __init__(self) -> None:
        super().__init__()

    def draw(self, context):
        super().draw(context)

        layout = self.layout

        layout.label(text='Max number for each light type, 0 for none')
        column = layout.column(align=True)
        row = column.row(align=True)
        row.label(icon='LIGHT_POINT')
        row.prop(self.props_light, 'PointMax', text='Point')
        row = column.row(align=True)
        row.label(icon='LIGHT_SUN')
        row.prop(self.props_light, 'SunMax', text='Sun')
        row = column.row(align=True)
        row.label(icon='LIGHT_SPOT')
        row.prop(self.props_light, 'SpotMax', text='Spot')
        row = column.row(align=True)
        row.label(icon='LIGHT_AREA')
        row.prop(self.props_light, 'AreaMax', text='Area')

        layout.separator_spacer()
        layout.prop(self.props_light, 'bRandomSpec')
        layout.prop(self.props_light, 'Color')
        layout.prop(self.props_light, 'Power')
        layout.prop(self.props_light, 'PointRadius')
        layout.prop(self.props_light, 'SunAngle')
        column = layout.column(align=True)
        column.prop(self.props_light, 'SpotRadius')
        column.prop(self.props_light, 'SpotSize')
        column.prop(self.props_light, 'SpotBlend')
        column = layout.column(align=True)
        column.prop(self.props_light, 'AreaSizeX')
        column.prop(self.props_light, 'AreaSizeY')

# Camera Panel
class P_Camera(P_Master):

# Props:
# Lens (lens setting)
# Depth of field (dof setting)
# Sensor (enum, int)
# Camera numbers (int)
# Camera motion range (float)
# Foucus or not (boolean)
# Rotate or not (boolean)
# Complex rate (int)

    bl_order, bl_idname, bl_label, bl_parent_id = SignRegisterProps(4)

    def __init__(self) -> None:
        super().__init__()
        bpy.ops.ad_util.list_check(
            panel_name='Camera',
            structure_name='Curves',
            idx_name='Index',
            type_name='CURVE',
            bObj=True,
        )

    def draw(self, context):
        super().draw(context)

        layout = self.layout

        layout.label(text=
        'WARNNING! If you selected curves, will not random generate but choice from this list.'
        )
        row = layout.row()
        row.template_list(util.ui.UL_SelectedObjects.bl_idname,'UL_Camera',
                            self.props_camera, 'Curves',
                            self.props_camera, 'Index')

        col = row.column(align=True)
        button = col.operator('ad_util.list_action', icon='ADD', text='')
        ButtonProps(button, 'ADD', 'Camera', 'Curves', 'Index', 'CURVE')
        button = col.operator('ad_util.list_action', icon='REMOVE', text='')
        ButtonProps(button, 'REMOVE', 'Camera', 'Curves', 'Index', 'CURVE')

        layout.prop(self.props_camera, 'LensFocalLength')
        
        layout.separator_spacer()
        layout.prop(self.props_camera, 'bUseDoF')
        column = layout.column(align=True)
        column.enabled = self.props_camera.bUseDoF
        column.prop(self.props_camera, 'FocalDistance')
        column.prop(self.props_camera, 'FStop')
        column.prop(self.props_camera, 'Blades')
        column.prop(self.props_camera, 'ApertureRotation')
        column.prop(self.props_camera, 'ApertureRatio')

        layout.separator_spacer()
        layout.prop(self.props_camera, 'SensorFit')
        layout.prop(self.props_camera, 'SensorSize')

        layout.separator_spacer()
        layout.prop(self.props_camera, 'ComplexRate')
        layout.prop(self.props_camera, 'CameraNumber')
        layout.prop(self.props_camera, 'CameraMotionRange')

        selected_curve = None
        if self.props_camera.Curves:
            try:
                selected_curve = self.props_camera.Curves[self.props_camera.Index]
            except:
                pass
            if selected_curve:
                column = layout.column(align=True)
                column.enabled = not selected_curve.bCameraRotate
                column.prop(selected_curve, 'bCameraFocus')
                column = layout.column(align=True)
                column.enabled = selected_curve.bCameraFocus
                column.prop(selected_curve, 'FocusCenter')
                column = layout.column(align=True)
                column.enabled = not selected_curve.bCameraFocus
                column.prop(selected_curve, 'bCameraRotate')
        else:
            column = layout.column(align=True)
            column.enabled = not self.props_camera.bRandomCameraRotate
            column.prop(self.props_camera, 'bRandomCameraFocus')
            column = layout.column(align=True)
            column.enabled = self.props_camera.bRandomCameraFocus
            column.prop(self.props_camera, 'RandomFocusCenter')
            column = layout.column(align=True)
            column.enabled = not self.props_camera.bRandomCameraFocus
            column.prop(self.props_camera, 'bRandomCameraRotate')


# Physics Panel
# Objects (List)
# Mass, Surface response, Dynamics setting
# Initial Speed (float)
# Time scale (float)
# Substeps (int)
# Solver Iterations (int)
class P_Physics(P_Master):
    bl_order, bl_idname, bl_label, bl_parent_id = SignRegisterProps(5)

    def __init__(self) -> None:
        super().__init__()
        bpy.ops.ad_util.list_check(
            panel_name='Physics',
            structure_name='SelectedObject',
            idx_name='Index',
            type_name='MESH',
            bObj=True,
        )

    def draw(self, context):
        super().draw(context)

        layout = self.layout

        row = layout.row()
        row.template_list(util.ui.UL_SelectedObjects.bl_idname,'UL_Phy',
                            self.props_physics, 'SelectedObject',
                            self.props_physics, 'Index')
        col = row.column(align=True)
        button = col.operator('ad_util.list_action', icon='ADD', text='')
        ButtonProps(button, 'ADD', 'Physics', 'SelectedObject', 'Index', 'MESH')

        button = col.operator('ad_util.list_action', icon='REMOVE', text='')
        ButtonProps(button, 'REMOVE', 'Physics', 'SelectedObject', 'Index', 'MESH')
        
        SubPropsShow(
            self.props_physics.SelectedObject, 
            self.props_physics.Index, 
            layout, 
            ['Shape', 'Source', 'Mass', 'Friction', 'Bounciness'],
            )

        layout.prop(self.props_physics, "TimeScale")
        column = layout.column(align=True)
        column.prop(self.props_physics, "Substeps")
        column.prop(self.props_physics, "Iterations")


# Movement Panel
class P_Movement(P_Master):
    # Props:
    # InitialVelVal (Initial Velocity Value)
    # InitialVelDir (Initial Velocity Direction)

    bl_order, bl_idname, bl_label, bl_parent_id = SignRegisterProps(6)

    def __init__(self) -> None:
        super().__init__()
        bpy.ops.ad_util.list_check(
            panel_name='Movement',
            structure_name='Curves',
            idx_name='Index',
            type_name='CURVE',
            bObj=True,
        )

    def draw(self, context):
        super().draw(context)

        layout = self.layout

        layout.label(text=
                     'WARNNING! If you selected curves, will not random generate but choice from this list.'
                     )
        row = layout.row()
        row.template_list(util.ui.UL_SelectedObjects.bl_idname, 'UL_Movement',
                          self.props_movement, 'Curves',
                          self.props_movement, 'Index')

        col = row.column(align=True)
        button = col.operator('ad_util.list_action', icon='ADD', text='')
        ButtonProps(button, 'ADD', 'Movement', 'Curves', 'Index', 'CURVE')
        button = col.operator('ad_util.list_action', icon='REMOVE', text='')
        ButtonProps(button, 'REMOVE', 'Movement', 'Curves', 'Index', 'CURVE')

        layout.separator_spacer()
        layout.prop(self.props_movement, 'bRandomVelVal')
        column = layout.column(align=True)
        column.enabled = self.props_movement.bRandomVelVal
        column.prop(self.props_movement, 'MaxVel', text='Max Random Velocity')
        column.prop(self.props_movement, 'MinVel', text='Min Random Velocity')
        column = layout.column(align=True)
        column.enabled = not self.props_movement.bRandomVelVal
        column.prop(self.props_movement, 'InitialVelVal', text='Initial Velocity Value')

        layout.separator_spacer()
        layout.prop(self.props_movement, 'bRandomVelDir')
        column = layout.column(align=True)
        column.enabled = not self.props_movement.bRandomVelDir
        column.prop(self.props_movement, 'InitialVelDir')


AllPanelClasses = [P_General, P_Object, P_Material, P_Light, P_Camera, P_Physics, P_Movement]
