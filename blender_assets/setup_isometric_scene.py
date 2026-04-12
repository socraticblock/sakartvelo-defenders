#!/usr/bin/env python3
"""
Create a basic isometric scene setup in Blender
Run this from command line: blender -b -P setup_isometric_scene.py
"""

import bpy
import os
import sys
from math import radians

def clear_scene():
    """Clear default scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_isometric_camera():
    """Create orthographic isometric camera"""
    camera_data = bpy.data.cameras.new("IsoCamera")
    camera_object = bpy.data.objects.new("IsoCamera", camera_data)

    # Isometric angle
    camera_object.rotation_euler = (0.785398, 0.61548, 0)  # 45°, 35.264°, 0°
    camera_object.location = (0, 0, 5)

    camera_data.type = 'ORTHO'
    camera_data.ortho_scale = 4

    bpy.context.collection.objects.link(camera_object)
    bpy.context.scene.camera = camera_object

    return camera_object

def create_lighting():
    """Setup basic lighting for cel-shaded look"""
    # Remove default lights
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()

    # Main light (top-right)
    light_data = bpy.data.lights.new(name="MainLight", type='SUN')
    light_object = bpy.data.objects.new(name="MainLight", object_data=light_data)
    light_object.location = (2, 2, 5)
    light_object.rotation_euler = (radians(-45), radians(-35), radians(0))
    light_data.energy = 3.0
    bpy.context.collection.objects.link(light_object)

    # Fill light (soft)
    fill_data = bpy.data.lights.new(name="FillLight", type='SUN')
    fill_object = bpy.data.objects.new(name="FillLight", object_data=fill_data)
    fill_object.location = (-2, -2, 3)
    fill_object.rotation_euler = (radians(45), radians(35), radians(180))
    fill_data.energy = 0.5
    bpy.context.collection.objects.link(fill_object)

def create_cel_shader_material(name="CelShader"):
    """Create basic cel-shaded material"""
    if name in bpy.data.materials:
        return bpy.data.materials[name]

    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    nodes.clear()

    # Create nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (400, 0)

    shader = nodes.new(type='ShaderNodeBsdfPrincipled')
    shader.location = (0, 0)

    # Set properties for cel-shaded look
    shader.inputs['Roughness'].default_value = 0.0
    shader.inputs['Metallic'].default_value = 0.0

    # Link
    links.new(shader.outputs['BSDF'], output.inputs['Surface'])

    return mat

def create_base_grid():
    """Create a reference grid for alignment"""
    # Create plane
    bpy.ops.mesh.primitive_plane_add(size=10)
    grid = bpy.context.active_object
    grid.name = "ReferenceGrid"

    # Add wireframe material
    mat = bpy.data.materials.new(name="GridMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = (0.3, 0.3, 0.3, 0.5)
    bsdf.inputs['Alpha'].default_value = 0.3
    mat.blend_method = 'BLEND'

    grid.data.materials.append(mat)

    return grid

def setup_render_settings():
    """Configure render settings for sprite output"""
    scene = bpy.context.scene

    # Resolution
    scene.render.resolution_x = 128
    scene.render.resolution_y = 128
    scene.render.resolution_percentage = 100

    # Output format
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '8'

    # Transparency
    scene.render.film_transparent = True

    # Background
    if not scene.world:
        scene.world = bpy.data.worlds.new("World")

    world = scene.world
    if world.use_nodes:
        bg_node = world.node_tree.nodes.get("Background")
        if bg_node:
            bg_node.inputs['Strength'].default_value = 0.0

    # Anti-aliasing (less for cel-shaded look)
    # Note: In Blender 4.2, samples are set via the render engine settings

def save_scene(filepath="isometric_template.blend"):
    """Save the template scene"""
    bpy.ops.wm.save_as_mainfile(filepath=filepath)
    print(f"Scene saved to: {filepath}")

def main():
    """Main setup function"""
    print("Setting up isometric template scene...")

    clear_scene()
    create_isometric_camera()
    create_lighting()
    create_cel_shader_material()
    create_base_grid()
    setup_render_settings()

    # Save to models directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(script_dir, "models", "base_templates")
    os.makedirs(models_dir, exist_ok=True)

    output_path = os.path.join(models_dir, "isometric_template.blend")
    save_scene(output_path)

    print("✓ Isometric template scene created successfully!")
    print(f"  Open Blender and load: {output_path}")
    print("  Then create your models and render them using render_helper.py")

if __name__ == "__main__":
    main()
