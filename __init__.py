bl_info = {
    "name": "GPCC",
    "author": "Fumiya Funatsu",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "description": "convert grease pencil into colored curve",
    "category": "Object"
}

import bpy
import addon_utils

import importlib
if "gpcc" in locals():    
    importlib.reload(gpcc)
    
from . import gpcc

gp2curves = gpcc.GPCC_OT_ConvertGP2Curves
log = gpcc.log

def is_addon_installed(addon_name):
    for module in addon_utils.modules():
        if addon_name == module.__name__:
            return True
    return False

def menu_fn(self, context):
    self.layout.separator()
    self.layout.operator(gp2curves.bl_idname)

def register():
    if is_addon_installed(gpcc.addon_id_b):
        unregister()
    bpy.utils.register_class(gp2curves)
    bpy.types.VIEW3D_MT_add.append(menu_fn)
    log("registered")

def unregister():
    bpy.types.VIEW3D_MT_add.remove(menu_fn)
    bpy.utils.unregister_class(gp2curves)
    log("unregistered")

if __name__ == "__main__":
    register()