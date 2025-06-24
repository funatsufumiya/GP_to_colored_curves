import bpy
import os
import datetime
import numpy as np
import mathutils
from mathutils import Vector, Quaternion, Euler, Matrix
from bpy.types import Context, bpy_prop_array, Object
from typing import List
import random

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

def make_curves(
        name: str,
        matrix_world: Matrix,
        coords: List[Vector],
        # vertex_colors: List[bpy_prop_array],
        radiuses: List[float],
        context: Context
    ):
    curveData = bpy.data.curves.new(name, type='CURVE')
    curveData.dimensions = '3D'
    curveData.resolution_u = 2
    polyline = curveData.splines.new('POLY')
    polyline.points.add(len(coords)-1)
    # TODO: set vertex color
    for i, coord in enumerate(coords):
        x,y,z = coord
        polyline.points[i].co = (x, y, z, 1)
        polyline.points[i].radius = radiuses[i]

    curveObj = bpy.data.objects.new(name, curveData)
    curveData.bevel_depth = 0.01
    context.collection.objects.link(curveObj)
    curveObj.matrix_world = matrix_world
    return curveObj

def deleteObject(obj: Object):
    sels = bpy.context.selected_objects
    for o in sels:
        o.select_set(False)
    obj.select_set(True)
    bpy.ops.object.delete()
    for o in sels:
        o.select_set(True)

def deselect():
    sels = bpy.context.selected_objects
    for o in sels:
        o.select_set(False)

    bpy.ops.object.select_all(action='DESELECT')

def selectObject(obj: Object, need_deselect=True):
    if need_deselect:
        deselect()
    obj.select_set(True)

def convertCurveToMesh(
        curveObj: Object,
        context: Context
    ):
    assert curveObj.type == "CURVE"
    mesh = bpy.data.meshes.new_from_object(curveObj)
    new_obj = bpy.data.objects.new(f"Mesh_{curveObj.name}", mesh)
    new_obj.matrix_world = curveObj.matrix_world
    context.collection.objects.link(new_obj)
    deleteObject(curveObj)
    return new_obj

def color_to_vertices(
        meshObj: Object,
    ):
    assert meshObj.type == "MESH"
    mesh = meshObj.data

    if not mesh.attributes.active_color:
       color_layer = mesh.color_attributes.new("Col", 'FLOAT_COLOR', 'POINT')
    else:
       color_layer = mesh.attributes.active_color

    # for polygon in mesh.polygons:
    #     for i, index in enumerate(polygon.vertices):
    #         loop_index = polygon.loop_indices[i]
    #         # mesh.vertex_colors.active.data[loop_index].color = color
    #         color_layer.data[loop_index].color = random_color()

    for i in range(len(color_layer.data)):
        color_layer.data[i].color = random_color()

def random_color():
    r,g,b = [random.uniform(0, 1) for i in range(3)]
    return [r, g, b, 1.0]

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
    # obj_name = sel.name
    # obj_location = sel.location
    # obj_rot_euler = sel.rotation_euler
    # obj_scale = sel.scale
    obj_matrix_world = sel.matrix_world
    obj_type = sel.type

    # log(f"rot_quat: {obj_rot_quat}")
    
    ## log(type(sel))
    # log(obj_type)

    if obj_type != "GPENCIL":
        return break_ret
    
    # log("yeah! gpencil!")

    # log(dir(sel.data))

    name = sel.data.name
    layers = sel.data.layers

    # log(f"name: {name}")
    # log(f"layers: {layers}")

    if len(layers) > 0:
        layer = layers[0]
        # log(f"layer0: {layer}")
        ## log(f"layer0 dir: {dir(layer0)}")
        # log(f"frames: {layer.frames}")
        if len(layer.frames) > 0:
            # get frame at current frame, by where condition
            frames_match = list(filter(lambda f: f.frame_number == frame_current, layer.frames))
            if len(frames_match) > 0:
                frame = frames_match[0]
                # log(f"frame: {frame}")
                ## log(f"frame dir: {dir(frame)}")
                # log(f"strokes: {frame.strokes}")
                ## log(f"strokes dir: {dir(frame.strokes)}")
                ## log(f"strokes values: {frame.strokes.values()}")

                strokes = frame.strokes.values()

                for stroke in strokes:
                    # log(f"stroke: {stroke}")
                    cs = [p.co for p in stroke.points.values()]
                    vcs = [p.vertex_color for p in stroke.points.values()]
                    pressures = [p.pressure for p in stroke.points.values()]
                    thickness_factor = 0.05
                    thicknesses = np.array(pressures) * float(stroke.line_width) * thickness_factor
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

                    curveObj = make_curves(
                        name=f"Curve_{name}",
                        matrix_world=obj_matrix_world,
                        coords=cs,
                        # vcs,
                        radiuses=thicknesses,
                        context=bpy.context)

                    # selectObject(curveObj)

                    meshObj = convertCurveToMesh(curveObj=curveObj, context=bpy.context)
                    selectObject(meshObj)

                    color_to_vertices(meshObj)
                    # color_to_vertices(color=RGB)

    return last_ret

class GPCC_OT_ConvertGP2Curves(bpy.types.Operator):

    bl_idname = f"{addon_id_s}.convert_gp_to_curves"
    bl_label = "gp_to_curves"
    bl_description = "convert grease pencil into curves"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return gp2curves()