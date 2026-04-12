#!/usr/bin/env python3
"""
Blender Rendering Helper for Sakartvelo Defenders
Automates rendering 3D models to 2D isometric sprites

Usage in Blender:
- Open this script in Blender's Text Editor
- Run script with the object selected
- Outputs: renders/[category]/[name].png
"""

import bpy
import os
from math import radians

# Configuration
RENDER_PATH = os.path.join(os.path.dirname(__file__), "renders")
ISO_CAMERA_ROTATION = (radians(45), radians(35.264), 0)  # True isometric
RENDER_RESOLUTIONS = {
    "enemies": (64, 64),
    "heroes": (256, 256),
    "towers": (128, 128),
    "maps": (128, 128),
    "vfx": (128, 128)
}

def setup_isometric_camera():
    """Configure camera for isometric rendering"""
    if "IsoCamera" not in bpy.data.objects:
        # Create camera if it doesn't exist
        camera_data = bpy.data.cameras.new("IsoCamera")
        camera_object = bpy.data.objects.new("IsoCamera", camera_data)
        bpy.context.collection.objects.link(camera_object)

    camera = bpy.data.objects["IsoCamera"]
    camera.data.type = 'ORTHO'
    camera.rotation_euler = ISO_CAMERA_ROTATION
    camera.location = (0, 0, 5)

    bpy.context.scene.camera = camera
    return camera

def setup_render_settings(resolution=(128, 128), transparent=True):
    """Configure render settings"""
    scene = bpy.context.scene

    # Resolution
    scene.render.resolution_x = resolution[0]
    scene.render.resolution_y = resolution[1]
    scene.render.resolution_percentage = 100

    # Output
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'

    # Transparency
    if transparent:
        scene.render.film_transparent = True
        scene.render.image_settings.color_depth = '8'

    # Background (for debugging, disable for final renders)
    world = scene.world
    if world:
        world.node_tree.nodes["Background"].inputs['Strength'].default_value = 0.0

def center_object_to_origin(obj):
    """Center object at origin"""
    # Get bounding box
    bbox = obj.bound_box
    x_coords = [v[0] for v in bbox]
    y_coords = [v[1] for v in bbox]
    z_coords = [v[2] for v in bbox]

    center_x = sum(x_coords) / len(x_coords)
    center_y = sum(y_coords) / len(y_coords)
    center_z = sum(z_coords) / len(z_coords)

    # Move to origin
    obj.location = (-center_x, -center_y, -min(z_coords))

def render_to_file(category, name):
    """Render current scene to file"""
    # Create output directory
    output_dir = os.path.join(RENDER_PATH, category)
    os.makedirs(output_dir, exist_ok=True)

    # Set output path
    output_path = os.path.join(output_dir, f"{name}.png")
    bpy.context.scene.render.filepath = output_path

    # Render
    bpy.ops.render.render(write_still=True)

    print(f"✓ Rendered to: {output_path}")
    return output_path

def render_selected_object(category="enemies", resolution_override=None):
    """Main function to render selected object"""
    # Get selected object
    selected = bpy.context.selected_objects
    if not selected:
        print("Error: No object selected")
        return

    obj = selected[0]
    obj_name = obj.name

    print(f"Rendering: {obj_name}")

    # Setup scene
    setup_isometric_camera()
    resolution = resolution_override or RENDER_RESOLUTIONS.get(category, (128, 128))
    setup_render_settings(resolution=resolution)

    # Center object
    center_object_to_origin(obj)

    # Clear other objects from scene (optional)
    # for other_obj in bpy.data.objects:
    #     if other_obj != obj and other_obj.name != "IsoCamera":
    #         other_obj.hide_render = True

    # Render
    render_to_file(category, obj_name)

    # Unhide objects
    # for other_obj in bpy.data.objects:
    #     other_obj.hide_render = False

    print("Done!")

# Example usage
if __name__ == "__main__":
    # This will run when script is executed in Blender
    render_selected_object(category="enemies")
