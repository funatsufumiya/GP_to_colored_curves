bl_info = {
    "name": "GP to Colored Curves",
    "author": "Fumiya Funatsu",
    "version": (0, 1, 5),
    "blender": (2, 80, 0),
    "description": "Convert grease pencil (GP) into colored curves (meshes)",
    "category": "Object"
}

import bpy
import addon_utils

import importlib
if "gpcc" in locals():    
    importlib.reload(gpcc)
    
from . import gpcc

log = gpcc.log

def is_addon_installed(addon_name):
    for module in addon_utils.modules():
        if addon_name == module.__name__:
            return True
    return False

class GPCC_OT_ResetPrefs(bpy.types.Operator):
    bl_idname = "gpcc.reset_prefs"
    bl_label = "Reset to Default"
    bl_description = "Reset preferences to default values"

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        prefs.thickness_factor_gpv2 = 0.05
        prefs.thickness_factor_gpv3 = 100.0
        self.report({'INFO'}, "Preferences reset to default values")
        return {'FINISHED'}

class GPCCAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    thickness_factor_gpv2: bpy.props.FloatProperty(
        name="Thickness Factor (GPv2)",
        description="Multiplier for curve thickness (GPv2)",
        default=0.05,
        min=0.001,
        max=10.0
    )
    thickness_factor_gpv3: bpy.props.FloatProperty(
        name="Thickness Factor (GPv3)",
        description="Multiplier for curve thickness (GPv3)",
        default=100.0,
        min=0.1,
        max=10000.0
    )

    def draw(self, context):
        layout = self.layout
        # layout.label(text="test")
        if gpcc.is_blv_gpv2:
            layout.prop(self, "thickness_factor_gpv2")
        elif gpcc.is_blv_gpv3:
            layout.prop(self, "thickness_factor_gpv3")

        layout.operator("gpcc.reset_prefs", icon="LOOP_BACK")

reset_btn = GPCC_OT_ResetPrefs
pref = GPCCAddonPreferences
gp2meshes = gpcc.GPCC_OT_ConvertGP2Meshes
gp2curves = gpcc.GPCC_OT_ConvertGP2Curves
gp2curves_without_radius = gpcc.GPCC_OT_ConvertGP2CurvesWithoutRadius
submenu = gpcc.GPCC_MT_SubMenu

classes = [
    gp2meshes,
    gp2curves,
    gp2curves_without_radius,
    submenu,
    reset_btn,
    pref
]

def menu_fn(self, context):
    self.layout.separator()
    self.layout.menu(submenu.bl_idname)

def register():
    if is_addon_installed(__name__):
        unregister()
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_object.append(menu_fn)
    # log("registered")

def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_fn)
    for c in classes:
        try:
            bpy.utils.unregister_class(c)
        except:
            pass
    # log("unregistered")

if __name__ == "__main__":
    register()