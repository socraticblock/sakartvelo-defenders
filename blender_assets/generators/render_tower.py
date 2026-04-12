#!/usr/bin/env python3
"""
Render Tower Model to 2D Sprite
"""

import bpy
import os

def setup_render():
    """Configure render settings for tower sprite"""
    scene = bpy.context.scene

    # Resolution (128x128 for towers)
    scene.render.resolution_x = 128
    scene.render.resolution_y = 128
    scene.render.resolution_percentage = 100

    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = True

    if "IsoCamera" in bpy.data.objects:
        scene.camera = bpy.data.objects["IsoCamera"]

    cam = scene.camera
    if cam and cam.data.type != 'ORTHO':
        cam.data.type = 'ORTHO'

def center_and_frame_object():
    """Center object and frame camera"""
    objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']

    if not objects:
        print("No mesh objects found!")
        return

    obj = objects[0]
    bbox = obj.bound_box
    x_coords = [v[0] for v in bbox]
    y_coords = [v[1] for v in bbox]
    z_coords = [v[2] for v in bbox]

    center_x = sum(x_coords) / len(x_coords)
    center_y = sum(y_coords) / len(y_coords)
    min_z = min(z_coords)

    obj.location = (-center_x, -center_y, -min_z)

    scene = bpy.context.scene
    if scene.camera:
        cam_data = scene.camera.data
        max_dim = max(
            max(x_coords) - min(x_coords),
            max(y_coords) - min(y_coords),
            max(z_coords) - min(z_coords)
        )
        cam_data.ortho_scale = max_dim * 1.5

    return obj

def main():
    print("Rendering tower sprite...")
    setup_render()
    obj = center_and_frame_object()
    if obj:
        print(f"  Rendering: {obj.name}")

    script_dir = "/home/socraticblock/hermes-workspace/hermes/development/sakartvelo-defenders/blender_assets"
    output_dir = f"{script_dir}/renders/towers"
    os.makedirs(output_dir, exist_ok=True)

    output_path = f"{output_dir}/tower_e00_stone_watchtower.png"
    bpy.context.scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)

    print(f"✓ Rendered to: {output_path}")
    print("✓ Render complete!")

if __name__ == "__main__":
    main()
