import bpy
import os
import datetime

addon_name_for_log = "GPCC"
addon_id_b = "GPCC"
addon_id_s = "gpcc"

# def b_print(data):
#     for window in bpy.context.window_manager.windows:
#         screen = window.screen
#         for area in screen.areas:
#             if area.type == 'CONSOLE':
#                 override = {'window': window, 'screen': screen, 'area': area}
#                 bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")   

def log(s):
    print(f"[{addon_name_for_log}]: {s}")

def version():
    _stat = os.stat(__file__)
    dt = datetime.datetime.fromtimestamp(_stat.st_mtime)
    return dt.strftime('%Y/%m/%d %H:%M:%S.%f')

def gp2curves():
    break_ret = {'FINISHED'}
    last_ret = {'FINISHED'}
    # bpy.ops.mesh.primitive_ico_sphere_add()
    # log("created ico sphere")

    frame_current = bpy.context.scene.frame_current

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

    # log(dir(sel.data))

    name = sel.data.name
    layers = sel.data.layers

    log(f"name: {name}")
    log(f"layers: {layers}")

    if len(layers) > 0:
        layer = layers[0]
        log(f"layer0: {layer}")
        # log(f"layer0 dir: {dir(layer0)}")
        log(f"frames: {layer.frames}")
        if len(layer.frames) > 0:
            # get frame at current frame, by where condition
            frames_match = list(filter(lambda f: f.frame_number == frame_current, layer.frames))
            if len(frames_match) > 0:
                frame = frames_match[0]
                log(f"frame: {frame}")
                # log(f"frame dir: {dir(frame)}")
                log(f"strokes: {frame.strokes}")
                # log(f"strokes dir: {dir(frame.strokes)}")
                # log(f"strokes values: {frame.strokes.values()}")

                strokes = frame.strokes.values()

                for stroke in strokes:
                    log(f"stroke: {stroke}")
                    cs = [p.co for p in stroke.points.values()]
                    log(f"points: {cs}")

                    # c0 = cs[0]
                    # coords = [(stroke.points.matrix_world @ c) for c in cs]
                    # log(coords)

    return last_ret

class GPCC_OT_ConvertGP2Curves(bpy.types.Operator):

    bl_idname = f"{addon_id_s}.convert_gp_to_curves"
    bl_label = "gp_to_curves"
    bl_description = "convert grease pencil into curves"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return gp2curves()