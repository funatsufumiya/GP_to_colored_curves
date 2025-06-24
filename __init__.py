bl_info = {
    "name": "GP to Colored Curves",
    "author": "Fumiya Funatsu",
    "version": (0, 1, 3),
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

gp2meshes = gpcc.GPCC_OT_ConvertGP2Meshes
gp2curves = gpcc.GPCC_OT_ConvertGP2Curves
gp2curves_without_radius = gpcc.GPCC_OT_ConvertGP2CurvesWithoutRadius
submenu = gpcc.GPCC_MT_SubMenu

classes = [
    gp2meshes,
    gp2curves,
    gp2curves_without_radius,
    submenu
]

def menu_fn(self, context):
    self.layout.separator()
    self.layout.menu(submenu.bl_idname)

def register():
    if is_addon_installed(gpcc.addon_id_b):
        unregister()
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_object.append(menu_fn)
    # log("registered")

def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_fn)
    for c in classes:
        bpy.utils.unregister_class(c)
    # log("unregistered")

if __name__ == "__main__":
    register()