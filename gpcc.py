import bpy
import os
import datetime
import numpy as np
import mathutils
from mathutils import Vector
from bpy.types import Context
from typing import List

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

# https://blender.stackexchange.com/questions/51290/how-to-add-empty-object-not-using-bpy-ops
def make_empty(name: str, location: Vector, context: Context):
    empty_obj = bpy.data.objects.new( "empty", None, )
    empty_obj.name = name
    empty_obj.empty_display_size = 1 
    # bpy.data.collections[coll_name].objects.link(empty_obj)
    context.collection.objects.link(empty_obj)
    empty_obj.location = location
    return empty_obj

def make_curves(name: str, location: Vector, coords: List[Vector], context: Context):
    curveData = bpy.data.curves.new(name, type='CURVE')
    curveData.dimensions = '3D'
    curveData.resolution_u = 2
    polyline = curveData.splines.new('POLY')
    polyline.points.add(len(coords))
    for i, coord in enumerate(coords):
        x,y,z = coord
        polyline.points[i].co = (x, y, z, 1)

    curveObj = bpy.data.objects.new(name, curveData)
    curveData.bevel_depth = 0.01
    context.collection.objects.link(curveObj)
    curveObj.location = location
    return curveObj

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
                    # log(f"points: {cs}")

                    # # make empty at center point
                    # # FIXME: this point is relative to object transform
                    # center_point = Vector([
                    #     np.mean([c.x for c in cs]),
                    #     np.mean([c.y for c in cs]),
                    #     np.mean([c.z for c in cs]),
                    # ])
                    # log(f"p0: {cs[0]}")
                    # log(f"p0 (x, y, z): {cs[0].x}, {cs[0].y}, {cs[0].z}")
                    # log(f"center_point: {center_point}")

                    # make_empty("test_empty", center_point, bpy.context)

                    # make curves

                    # FIXME: curve location
                    curve_location = Vector([0, 0, 0])

                    make_curves("test_curve", curve_location, cs, bpy.context)

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