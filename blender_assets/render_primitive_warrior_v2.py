#!/usr/bin/env python3
"""
Render Primitive Warrior to 2D Sprite (v2)
Run: blender -b models/enemies/enemy_e00_primitive_warrior_v2.blend -P render_primitive_warrior_v2.py
"""

import bpy
import os

def setup_render():
    """Configure render settings (already set in template, but verify)"""
    scene = bpy.context.scene

    # Resolution (256x256 per v2.1 spec)
    scene.render.resolution_x = 256
    scene.render.resolution_y = 256
    scene.render.resolution_percentage = 100

    # Output format
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '8'

    # Transparent background
    scene.render.film_transparent = True

    # Ensure camera is set
    if "IsoCamera" in bpy.data.objects:
        scene.camera = bpy.data.objects["IsoCamera"]

    # Verify orthographic
    cam = scene.camera
    if cam and cam.data.type != 'ORTHO':
        cam.data.type = 'ORTHO'

def center_and_frame_object():
    """Center object and frame camera"""
    objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']

    if not objects:
        print("Error: No mesh objects found!")
        return None

    obj = objects[0]
    bbox = obj.bound_box
    x_coords = [v[0] for v in bbox]
    y_coords = [v[1] for v in bbox]
    z_coords = [v[2] for v in bbox]

    center_x = sum(x_coords) / len(x_coords)
    center_y = sum(y_coords) / len(y_coords)
    min_z = min(z_coords)

    # Center object
    obj.location = (-center_x, -center_y, -min_z)

    # Frame camera
    scene = bpy.context.scene
    if scene.camera:
        cam_data = scene.camera.data
        max_dim = max(
            max(x_coords) - min(x_coords),
            max(y_coords) - min(y_coords),
            max(z_coords) - min(z_coords)
        )
        cam_data.ortho_scale = max_dim * 1.3  # 1.3x for padding

    return obj

def main():
    print("Rendering Primitive Warrior v2...")
    print("Based on specification: specs/enemy_e00_primitive_warrior_spec.md")

    setup_render()
    obj = center_and_frame_object()

    if obj:
        print(f"  Rendering: {obj.name}")
    else:
        print("  Error: No object to render!")
        return

    # Output path
    script_dir = "/home/socraticblock/hermes-workspace/hermes/development/sakartvelo-defenders/blender_assets"
    output_dir = f"{script_dir}/renders/enemies"
    os.makedirs(output_dir, exist_ok=True)

    output_path = f"{output_dir}/enemy_e00_primitive_warrior_v2.png"
    bpy.context.scene.render.filepath = output_path

    # Render
    print(f"  Output: {output_path}")
    bpy.ops.render.render(write_still=True)

    print("\n✓ Render Complete!")
    print(f"  File: {output_path}")
    print(f"  Size: 256x256 PNG with RGBA")

    # Verify file exists
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"  Size on disk: {file_size} bytes")
    else:
        print("  Warning: Output file not found!")

if __name__ == "__main__":
    main()
