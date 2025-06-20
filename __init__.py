import bpy

addon_name = "my_test_addon"
addon_id_b = "GPCC"
addon_id_s = "gpcc"

bl_info = {
    "name": "my test addon",
    "author": "Fumiya Funatsu",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "description": "create ico sphere",
    "category": "Object"
}

def b_print(data):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")   

def log(s):
    b_print(f"[{addon_name}]: {s}")

class GPCC_OT_CreateObject(bpy.types.Operator):

    bl_idname = f"{addon_id_s}.createobject"
    bl_label = "ico_sphere"
    bl_description = "create ico sphere"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        log("created ico sphere")

        return {'FINISHED'}


def menu_fn(self, context):
    self.layout.separator()
    self.layout.operator(GPCC_OT_CreateObject.bl_idname)

def register():
    bpy.utils.register_class(GPCC_OT_CreateObject)
    bpy.types.VIEW3D_MT_add.append(menu_fn)
    log("registered")

def unregister():
    bpy.types.VIEW3D_MT_add.remove(menu_fn)
    bpy.utils.unregister_class(GPCC_OT_CreateObject)
    log("unregistered")

if __name__ == "__main__":
    register()