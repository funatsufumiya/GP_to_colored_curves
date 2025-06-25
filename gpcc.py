import bpy

blender_version = bpy.app.version
major_version = blender_version[0]
minor_version = blender_version[1]

is_blv_gpv2 = (major_version == 4 and minor_version <= 2) or (major_version < 4)
is_blv_gpv3 = not is_blv_gpv2

import os
import datetime
import numpy as np
import mathutils
from mathutils import Vector, Quaternion, Euler, Matrix
from bpy.types import Context, bpy_prop_array, Object, Operator
from typing import List
import random

addon_name_for_log = "GP to Colored Curves"
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

def make_empty(name: str, location: Vector, context: Context):
    empty_obj = bpy.data.objects.new( "empty", None, )
    empty_obj.name = name
    empty_obj.empty_display_size = 1 
    context.collection.objects.link(empty_obj)
    empty_obj.location = location
    return empty_obj

def make_curves(
        name: str,
        matrix_world: Matrix,
        coords: List[Vector],
        # vertex_colors: List[bpy_prop_array],
        radiuses: List[float] | None,
        context: Context
    ):
    curveData = bpy.data.curves.new(name, type='CURVE')
    curveData.dimensions = '3D'
    curveData.resolution_u = 2
    polyline = curveData.splines.new('POLY')
    polyline.points.add(len(coords)-1)

    for i, coord in enumerate(coords):
        x,y,z = coord
        polyline.points[i].co = (x, y, z, 1)
        if radiuses is not None:
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

# def color_to_vertices(
#         meshObj: Object,
#     ):
#     assert meshObj.type == "MESH"
#     mesh = meshObj.data

#     if not mesh.attributes.active_color:
#        color_layer = mesh.color_attributes.new("Col", 'FLOAT_COLOR', 'POINT')
#     else:
#        color_layer = mesh.attributes.active_color

#     zs = np.array([v.co[1] for v in mesh.vertices])
#     z_max = np.max(zs)
#     z_min = np.min(zs)
#     for polygon in mesh.polygons:
#         for i, vi in zip(polygon.loop_indices, polygon.vertices):
#             if i < len(color_layer.data):
#                 z = zs[vi]
#                 # color_layer.data[i].color = random_color()
#                 # color_layer.data[i].color = get_color(i, len(color_layer.data))
#                 color_layer.data[i].color = get_color(z, z_min, z_max)

#     # for i in range(len(color_layer.data)):
#     #     color_layer.data[i].color = random_color()

def rgb_to_rgba(rgb: bpy_prop_array, alpha: float) -> list[float]:
    """
    Convert RGB color to RGBA by adding an alpha channel.
    """
    c = list(rgb)
    return [c[0], c[1], c[2], alpha]

def color_to_vertices_from_gp(meshObj: Object, gp_vertex_colors: List[bpy_prop_array], alphas: List[float]):
    mesh = meshObj.data
    if not mesh.attributes.active_color:
        color_layer = mesh.color_attributes.new("Col", 'FLOAT_COLOR', 'POINT')
    else:
        color_layer = mesh.attributes.active_color

    # find nearest curve index
    n_dst = len(mesh.vertices)
    n_src = len(gp_vertex_colors)
    for i, v in enumerate(mesh.vertices):
        # match index linear (assuming the same order)
        idx = int(mapv(i, 0, n_dst-1, 0, n_src-1))
        # color_layer.data[i].color = gp_vertex_colors[idx]
        color_layer.data[i].color = rgb_to_rgba(gp_vertex_colors[idx], alphas[idx])

def mapv(v: float, vmin: float, vmax: float, tmin: float, tmax: float):
    """
    Map a value v from range [vmin, vmax] to range [tmin, tmax].
    """
    return tmin + (v - vmin) * (tmax - tmin) / (vmax - vmin)

# def random_color():
#     r,g,b = [random.uniform(0, 1) for i in range(3)]
#     return [r, g, b, 1.0]

# def get_color(v: float, min: float, max: float):
#     r,g,b = [
#         mapv(v, min, max, 0.0, 1.0),
#         0.0, 0.0 ]
#     return [r, g, b, 1.0]

def get_thickness_factor_gpv2():
    try:
        addon_prefs = bpy.context.preferences.addons[__package__].preferences
        return addon_prefs.thickness_factor_gpv2
    except Exception:
        return 0.05

def get_thickness_factor_gpv3():
    try:
        addon_prefs = bpy.context.preferences.addons[__package__].preferences
        return addon_prefs.thickness_factor_gpv3
    except Exception:
        return 100.0

def gp2curves(convert_to_meshes: bool, with_radius: bool, caller: Operator | None):
    break_ret = {'CANCELLED'}
    last_ret = {'FINISHED'}

    # log(f"caller: {caller}")
    # log(f"caller type: {type(caller)}")
    # log(f"caller is Operator: {isinstance(caller, Operator)}")

    def warn(s):
        if caller is None:
            log(f"[Warning] {s}")
        else:
            caller.report({'WARNING'}, s)
            # bpy.context.window_manager.popup_menu(s, title="Error", icon='ERROR')
            log(f"[Warning] {s}")

    frame_current = bpy.context.scene.frame_current

    sels = bpy.context.selected_objects

    if len(sels) < 1:
        warn("No GP object selected")
        return break_ret
    
    sel = sels[0]
    obj_matrix_world = sel.matrix_world
    obj_type = sel.type

    is_gpv3 = (obj_type == "GREASEPENCIL")
    is_gpv2 = (obj_type == "GPENCIL")
    is_gp = (is_gpv2 or is_gpv3)

    if not is_gp:
        warn("No GP object selected")
        return break_ret

    name = sel.data.name
    layers = sel.data.layers

    if len(layers) == 0:
        warn("No GP_Layers found")
        return break_ret
    
    # FIXME: should also consider other layers
    try_count = 0
    try_limit = 3
    layer_id = 0

    def should_retry():
        return try_count < try_limit

    while should_retry():
        layer_id = try_count
        if layer_id >= len(layers):
            warn("No valid GP Layers found")
            return break_ret

        layer = layers[layer_id]
        if len(layer.frames) == 0:
            if should_retry():
                try_count += 1
                continue
            else:
                warn("No GP_Layers found matches current frame")
                return break_ret
        
        frames_match = list(filter(lambda f: f.frame_number == frame_current, layer.frames))
        if len(frames_match) == 0:
            if should_retry():
                try_count += 1
                continue
            else:
                warn("No GP frame matches")
                return break_ret
        
        frame = frames_match[0]

        if is_gpv2:
            strokes = frame.strokes.values()
        elif is_gpv3:
            drawing = frame.drawing
            # FIXME: should use attributes instead of strokes for performance
            strokes = drawing.strokes

        if len(strokes) == 0:
            if should_retry():
                try_count += 1
                continue
            else:
                caller.report({'WARNING'}, "No GP strokes found")
                return break_ret

        for stroke in strokes:
            if is_gpv2:
                cs = [p.co for p in stroke.points.values()]
                vcs = [p.vertex_color for p in stroke.points.values()]
                alphas = [p.strength for p in stroke.points.values()]
                pressures = [p.pressure for p in stroke.points.values()]
                thickness_factor_gpv2 = get_thickness_factor_gpv2()
                thicknesses = np.array(pressures) * float(stroke.line_width) * thickness_factor_gpv2
            elif is_gpv3:
                # NOTE: for undocumented classes, see
                # https://projects.blender.org/blender/blender/issues/126610

                cs = [p.position for p in stroke.points]
                vcs = [p.vertex_color for p in stroke.points]
                alphas = [p.opacity for p in stroke.points]
                radiuses = [p.radius for p in stroke.points]
                thickness_factor_gpv3 = get_thickness_factor_gpv3()
                thicknesses = np.array(radiuses) * thickness_factor_gpv3

            if with_radius:
                radiuses = thicknesses
            else:
                radiuses = None

            curveObj = make_curves(
                name=f"Curve_{name}",
                matrix_world=obj_matrix_world,
                coords=cs,
                # vertex_colors=vcs,
                radiuses=radiuses,
                context=bpy.context)

            if convert_to_meshes:
                meshObj = convertCurveToMesh(curveObj=curveObj, context=bpy.context)
                selectObject(meshObj)

                color_to_vertices_from_gp(meshObj, vcs, alphas)
            else:
                selectObject(curveObj)

        return last_ret
    
    warn("No valid GP layer found")
    return break_ret

class GPCC_OT_ConvertGP2Meshes(bpy.types.Operator):

    bl_idname = f"{addon_id_s}.convert_gp_to_meshes"
    bl_label = "GP to Meshes (with vertex-color)"
    bl_description = "Convert grease pencil (GP) into colored curved meshes with radius, opacity, vertex-color"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return gp2curves(convert_to_meshes=True, with_radius=True, caller=self)
    
class GPCC_OT_ConvertGP2Curves(bpy.types.Operator):

    bl_idname = f"{addon_id_s}.convert_gp_to_curves"
    bl_label = "GP to Curves (without vertex-color)"
    bl_description = "Convert grease pencil (GP) into curves, with radius but without vertex-color and opacity"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return gp2curves(convert_to_meshes=False, with_radius=True, caller=self)
    
class GPCC_OT_ConvertGP2CurvesWithoutRadius(bpy.types.Operator):

    bl_idname = f"{addon_id_s}.convert_gp_to_curves_without_radius"
    bl_label = "GP to Curves (without radius, vertex-color)"
    bl_description = "Convert grease pencil (GP) into curves, without radius, vertex-color and opacity"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return gp2curves(convert_to_meshes=False, with_radius=False, caller=self)


class GPCC_MT_SubMenu(bpy.types.Menu):
    bl_idname = f"{addon_id_s}.submenu"
    bl_label = "GP to Colored Curves"

    def draw(self, context):
        layout = self.layout
        layout.operator(GPCC_OT_ConvertGP2Meshes.bl_idname)
        layout.operator(GPCC_OT_ConvertGP2Curves.bl_idname)
        layout.operator(GPCC_OT_ConvertGP2CurvesWithoutRadius.bl_idname)