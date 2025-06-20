import bpy

addon_name_for_log = "GPCC"
addon_id_b = "GPCC"
addon_id_s = "gpcc"

bl_info = {
    "name": "GPCC",
    "author": "Fumiya Funatsu",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "description": "convert grease pencil into colored curve",
    "category": "Object"
}

# def b_print(data):
#     for window in bpy.context.window_manager.windows:
#         screen = window.screen
#         for area in screen.areas:
#             if area.type == 'CONSOLE':
#                 override = {'window': window, 'screen': screen, 'area': area}
#                 bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")   

def log(s):
    print(f"[{addon_name_for_log}]: {s}")

class GPCC_OT_ConvertGP2Curves(bpy.types.Operator):

    bl_idname = f"{addon_id_s}.convert_gp_to_curves"
    bl_label = "gp_to_curves"
    bl_description = "convert grease pencil into curves"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        break_ret = {'FINISHED'}
        last_ret = {'FINISHED'}
        # bpy.ops.mesh.primitive_ico_sphere_add()
        # log("created ico sphere")

        sels = bpy.context.selected_objects
        # log(sel)

        if len(sels) < 1:
            return break_ret
        
        sel = sels[0]
        obj_type = sel.type
        
        # log(type(sel))
        log(obj_type)

        if obj_type != "GPENCIL":
            return break_ret
        
        log("yeah! gpencil!")

        return last_ret
    
gp2curves = GPCC_OT_ConvertGP2Curves

def menu_fn(self, context):
    self.layout.separator()
    self.layout.operator(gp2curves.bl_idname)

def register():
    bpy.utils.register_class(gp2curves)
    bpy.types.VIEW3D_MT_add.append(menu_fn)
    log("registered")

def unregister():
    bpy.types.VIEW3D_MT_add.remove(menu_fn)
    bpy.utils.unregister_class(gp2curves)
    log("unregistered")

if __name__ == "__main__":
    register()