# GP to Colored Curves

Convert grease pencil (GP) into colored curves (meshes).

- GP's alpha (strength) and radius (thickness) are applied on converted meshes

![docs/screenshot_a.png](docs/screenshot_a.png)
![docs/screenshot_b.png](docs/screenshot_b.png)

Tested on Blender 4.2 LTS.

Blender 4.3+ is ***NOT*** currently supported (because of [GPv3](https://projects.blender.org/blender/blender/issues/114419)).

## Install

Download whole code from GitHub's "Download ZIP" menu, and rename it to "GP to Colored Curves.zip", then drop it into Blender.

## Usage

After install, first, please select a grease pencil (GP) object in Object Mode, and then call `Object > GP to Colored Curves > GP to Colored Curves` menu (you can also directly call it from F3 search menu).

## Known Issues

- Generated meshes has vertex colors (with alpha), but would not shown colors as default. You should create proper shader node for it (using `Color Attribute` node.)

## TODOs

- Adjust multiplication factor from pixels to radius (Blender 4.2 LTS)
- Blender 4.3+ support ([GPv3](https://projects.blender.org/blender/blender/issues/114419) support)
- Curve profile adjustment
