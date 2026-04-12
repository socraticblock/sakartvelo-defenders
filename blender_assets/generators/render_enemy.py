#!/usr/bin/env python3
"""
Render Enemy Model to 2D Sprite
Run: blender -b enemy_e00_primitive_warrior.blend -P render_enemy.py
"""

import bpy
import os
from math import radians

def setup_render():
    """Configure render settings for enemy sprite"""
    scene = bpy.context.scene

    # Resolution (64x64 for enemies)
    scene.render.resolution_x = 64
    scene.render.resolution_y = 64
    scene.render.resolution_percentage = 100

    # PNG with alpha
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'

    # Transparent background
    scene.render.film_transparent = True

    # Ensure camera is active
    if "IsoCamera" in bpy.data.objects:
        scene.camera = bpy.data.objects["IsoCamera"]

    # Make sure camera is orthographic
    cam = scene.camera
    if cam and cam.data.type != 'ORTHO':
        cam.data.type = 'ORTHO'

def center_and_frame_object():
    """Center object and frame camera"""
    # Get all mesh objects
    objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']

    if not objects:
        print("No mesh objects found!")
        return

    # Use the first mesh object
    obj = objects[0]

    # Center at origin
    bbox = obj.bound_box
    x_coords = [v[0] for v in bbox]
    y_coords = [v[1] for v in bbox]
    z_coords = [v[2] for v in bbox]

    center_x = sum(x_coords) / len(x_coords)
    center_y = sum(y_coords) / len(y_coords)
    min_z = min(z_coords)

    obj.location = (-center_x, -center_y, -min_z)

    # Frame camera to object
    scene = bpy.context.scene
    if scene.camera:
        # Simple orthographic scaling
        cam_data = scene.camera.data
        max_dim = max(
            max(x_coords) - min(x_coords),
            max(y_coords) - min(y_coords),
            max(z_coords) - min(z_coords)
        )
        cam_data.ortho_scale = max_dim * 1.5  # 50% padding

    return obj

def render_sprite(output_path):
    """Render and save sprite"""
    bpy.context.scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)
    print(f"✓ Rendered to: {output_path}")

def main():
    """Main render function"""
    print("Rendering enemy sprite...")

    # Setup render settings
    setup_render()

    # Center and frame object
    obj = center_and_frame_object()
    if obj:
        print(f"  Rendering: {obj.name}")

    # Create output directory
    script_dir = "/home/socraticblock/hermes-workspace/hermes/development/sakartvelo-defenders/blender_assets"
    output_dir = f"{script_dir}/renders/enemies"
    os.makedirs(output_dir, exist_ok=True)

    # Render
    output_path = f"{output_dir}/enemy_e00_primitive_warrior.png"
    render_sprite(output_path)

    print("✓ Render complete!")

if __name__ == "__main__":
    main()
