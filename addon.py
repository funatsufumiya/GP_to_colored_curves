import bpy

addon_name = "my_test_addon"

bl_info = {
    "name": addon_name,
    "author": "Fumiya Funatsu",
    "version": (0, 1),
    "blender": (4, 2, 0),
    "location": "3D View > Add > Mesh",
    "description": "create ico sphere",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

def log(s):
    print(f"[{addon_name}]: {s}")

class CreateObject(bpy.types.Operator):

    bl_idname = "object.create_object"
    bl_label = "ico_sphere"
    bl_description = "create ico sphere"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        log("created ico sphere")

        return {'FINISHED'}


def menu_fn(self, context):
    self.layout.separator()
    self.layout.operator(CreateObject.bl_idname)

def register():
    bpy.utils.register_module(addon_name)
    bpy.types.INFO_MT_mesh_add.append(menu_fn)
    log("registered")

def unregister():
    bpy.types.INFO_MT_mesh_add.remove(menu_fn)
    bpy.utils.unregister_module(addon_name)
    log("unregistered")

if __name__ == "__main__":
    register()