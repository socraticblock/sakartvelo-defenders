#!/usr/bin/env python3
"""
Create Standardized Blender Scene Template (v2.1) - Simplified Materials
Per Art Style Guide v2.1, Section 11.1-11.3

This creates the canonical scene template used for all asset rendering.
Uses simplified materials for compatibility.
"""

import bpy
import os
import math
from math import radians

def clear_scene():
    """Clear all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def setup_camera():
    """Camera: Orthographic, X=60°, Y=0°, Z=45° (2:1 isometric)"""
    camera_data = bpy.data.cameras.new(name="IsoCamera")
    camera_object = bpy.data.objects.new("IsoCamera", camera_data)

    camera_data.type = 'ORTHO'
    camera_data.ortho_scale = 4.0
    camera_object.rotation_euler = (radians(60.0), radians(0.0), radians(45.0))
    camera_object.location = (0, 0, 5)

    bpy.context.collection.objects.link(camera_object)
    bpy.context.scene.camera = camera_object
    return camera_object

def setup_lighting():
    """Lighting: Single Sun from upper-left + Ambient via World"""
    for obj in bpy.data.objects:
        if obj.type == 'LIGHT':
            bpy.data.objects.remove(obj, do_unlink=True)

    # Main Sun light
    sun_data = bpy.data.lights.new(name="MainSun", type='SUN')
    sun_object = bpy.data.objects.new(name="MainSun", object_data=sun_data)
    sun_object.location = (5, 5, 5)
    sun_object.rotation_euler = (radians(45), radians(0), radians(135))
    sun_data.energy = 1.0
    sun_data.shadow_soft_size = 0.1
    bpy.context.collection.objects.link(sun_object)

    # Ambient via World
    scene = bpy.context.scene
    if not scene.world:
        scene.world = bpy.data.worlds.new("World")

    world = scene.world
    if not world.use_nodes:
        world.use_nodes = True

    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs['Strength'].default_value = 0.15  # Ambient intensity

def create_simple_material(color, name="Material"):
    """Create simple flat color material"""
    if name in bpy.data.materials:
        return bpy.data.materials[name]

    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = 1.0
    bsdf.inputs['Metallic'].default_value = 0.0
    return mat

def create_era_0_materials():
    """Create Era 0 palette materials"""
    era_0_colors = {
        'Base': (0.176, 0.353, 0.239, 1.0),      # #2D5A3D
        'Highlight': (0.298, 0.686, 0.314, 1.0),  # #4CAF50
        'Shadow': (0.106, 0.227, 0.149, 1.0),     # #1B3A26
        'Accent': (0.831, 0.627, 0.090, 1.0),     # #D4A017
        'Stone': (0.545, 0.455, 0.333, 1.0),      # #8B7355
    }

    materials = {}
    for key, color in era_0_colors.items():
        materials[key] = create_simple_material(color, f"Era0_{key}")

    return materials

def setup_freestyle():
    """Configure Freestyle outlines: 2px, #1A1A1A"""
    scene = bpy.context.scene
    scene.render.use_freestyle = True

    view_layer = scene.view_layers[0]
    if view_layer.freestyle_settings.linesets:
        lineset = view_layer.freestyle_settings.linesets[0]
    else:
        lineset = view_layer.freestyle_settings.linesets.new("Outline")

    lineset.select_silhouette = True
    lineset.select_border = True
    lineset.select_crease = True

    linestyle = lineset.linestyle
    linestyle.color = (0.102, 0.102, 0.102)  # #1A1A1A
    linestyle.thickness = 2.0

def setup_render_settings():
    """Render: 256x256, PNG RGBA, 8x AA, No post-processing"""
    scene = bpy.context.scene
    scene.render.resolution_x = 256
    scene.render.resolution_y = 256
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '8'
    scene.render.film_transparent = True
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
    scene.eevee.taa_render_samples = 64
    scene.eevee.use_taa_reprojection = True

def save_scene(filepath):
    """Save the scene"""
    bpy.ops.wm.save_as_mainfile(filepath=filepath)
    print(f"✓ Scene saved: {filepath}")

def main():
    print("Creating Standardized Scene Template (v2.1 - Simplified)...")

    clear_scene()
    setup_camera()
    setup_lighting()
    create_era_0_materials()
    setup_freestyle()
    setup_render_settings()

    script_dir = "/home/socraticblock/hermes-workspace/hermes/development/sakartvelo-defenders/blender_assets"
    library_dir = f"{script_dir}/library"
    os.makedirs(library_dir, exist_ok=True)

    output_path = f"{library_dir}/shared_scene_template_v2.1.blend"
    save_scene(output_path)

    print("\n✓ Template Created Successfully!")
    print("  Location:", output_path)
    print("  Features: Orthographic Camera, Single Light, Flat Materials, Freestyle Outlines")

if __name__ == "__main__":
    main()
