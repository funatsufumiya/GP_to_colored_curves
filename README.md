# GP to Colored Curves

Convert grease pencil (GP) into colored curves (meshes).

- GP's vertex-color, alpha (strength) and radius (thickness) are applied on converted meshes
- Currently only export meshes, not curves itself (because of vertex-color application.)

![docs/screenshot_a.png](docs/screenshot_a.png)
![docs/screenshot_b.png](docs/screenshot_b.png)

Tested on Blender 4.2 LTS.

- Blender 4.3+ is ***NOT*** currently supported (because of [GPv3](https://projects.blender.org/blender/blender/issues/114419)).
    - as for now, you can use Geometry Nodes named [Grease Pencil to Curves Node](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/curve/operations/grease_pencil_to_curves.html)
    - Geometry Nodes example (for Blender 4.3+): ![docs/screenshot_gn.png](docs/screenshot_gn.png)
    - Shader Nodes example (for Blender 4.3+): ![docs/screenshot_sn.png](docs/screenshot_sn.png)

## Install

Download whole code from GitHub's "Download ZIP" menu, and rename it to "GP to Colored Curves.zip", then drop it into Blender.

## Usage

After install, first, please select a grease pencil (GP) object in Object Mode, and then call `Object > GP to Colored Curves > GP to Colored Curves` menu (you can also directly call it from F3 search menu).

## Known Issues

- Generated meshes have vertex colors (with alpha), but would not shown colors as default. You should create proper shader node for it (using `Color Attribute` node.)
    - Shader Nodes example: ![docs/screenshot_sn_attribute.png](docs/screenshot_sn_attribute.png)
- Radius(es) may bigger or smaller because of unit difference (pixels and meters, on Blender 4.2 LTS)
    - Multiplication factor should be variable, or need proper algorithm to convert units.
- Not all GP_Layers are considered. (This would not be fixed as soon, you can fork the code and modify them.) 

## TODOs

- Adjust multiplication factor from pixels to radius (Blender 4.2 LTS)
- Blender 4.3+ support ([GPv3](https://projects.blender.org/blender/blender/issues/114419) support)
- Curve profile adjustment
- Support more GP_Layers...?
