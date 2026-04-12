#!/usr/bin/env python3
"""
Create Standardized Blender Scene Template (v2.1)
Per Art Style Guide v2.1, Section 11.1-11.3

This creates the canonical scene template used for all asset rendering.
Run: blender -b -P create_shared_scene_template.py
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
    """
    Camera: Orthographic camera positioned for isometric view.
    Camera rotation: X = 60.0 degrees, Y = 0.0 degrees, Z = 45.0 degrees.
    This produces the standard 2:1 isometric pixel ratio.
    """
    camera_data = bpy.data.cameras.new(name="IsoCamera")
    camera_object = bpy.data.objects.new("IsoCamera", camera_data)

    # Orthographic camera for isometric view
    camera_data.type = 'ORTHO'
    camera_data.ortho_scale = 4.0  # Adjust per asset type

    # Rotation: X=60°, Y=0°, Z=45° (per v2.1 spec)
    camera_object.rotation_euler = (radians(60.0), radians(0.0), radians(45.0))
    camera_object.location = (0, 0, 5)

    bpy.context.collection.objects.link(camera_object)
    bpy.context.scene.camera = camera_object

    return camera_object

def setup_lighting():
    """
    Lighting: Single Sun light with Direction = (-1, -1, -1) normalized
    to produce upper-left illumination with lower-right shadows.
    Strength = 1.0, Color = White (#FFFFFF).
    A single ambient light at 0.15 intensity prevents completely black shadow areas.
    """
    # Remove any existing lights
    for obj in bpy.data.objects:
        if obj.type == 'LIGHT':
            bpy.data.objects.remove(obj, do_unlink=True)

    # Main Sun light (upper-left illumination)
    sun_data = bpy.data.lights.new(name="MainSun", type='SUN')
    sun_object = bpy.data.objects.new(name="MainSun", object_data=sun_data)

    # Direction = (-1, -1, -1) normalized
    sun_object.location = (5, 5, 5)
    # Rotation to point toward (-1, -1, -1) direction
    sun_object.rotation_euler = (radians(45), radians(0), radians(135))

    sun_data.energy = 1.0
    sun_data.shadow_soft_size = 0.1  # Sharp shadows for cel-shaded look

    bpy.context.collection.objects.link(sun_object)

    # Setup world for ambient lighting
    scene = bpy.context.scene
    if not scene.world:
        scene.world = bpy.data.worlds.new("World")

    world = scene.world
    if not world.use_nodes:
        world.use_nodes = True

    # Set ambient lighting via world background
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs['Strength'].default_value = 0.15  # Ambient intensity

def create_cel_shader_material(base_color, shadow_color, highlight_color, name="CelShader"):
    """
    Create standardized cel-shading material.
    Uses Geometry nodes to blend between Shadow and Highlight colors.
    """
    if name in bpy.data.materials:
        return bpy.data.materials[name]

    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    nodes.clear()

    # Create nodes
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (400, 0)

    geometry_node = nodes.new(type='ShaderNodeNewGeometry')
    geometry_node.location = (-400, 0)

    # Create MixRGB for shadow/highlight blending
    mix_node = nodes.new(type='ShaderNodeMixRGB')
    mix_node.location = (-100, 0)
    mix_node.blend_type = 'MIX'

    # Create Principled BSDF
    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf_node.location = (100, 0)
    bsdf_node.inputs['Roughness'].default_value = 1.0  # Non-metallic
    bsdf_node.inputs['Metallic'].default_value = 0.0

    # Set colors
    mix_node.inputs['Color1'].default_value = shadow_color
    mix_node.inputs['Color2'].default_value = highlight_color

    # Connect Geometry node to Mix factor (for cel-shading)
    dot_product_node = nodes.new(type='ShaderNodeVectorMath')
    dot_product_node.operation = 'DOT_PRODUCT'
    dot_product_node.location = (-600, -100)
    dot_product_node.inputs[0].default_value = (0, 0, 1)  # Up vector
    links.new(geometry_node.outputs['Normal'], dot_product_node.inputs[1])

    # Map dot product to 0-1 range
    map_range_node = nodes.new(type='ShaderNodeMapRange')
    map_range_node.location = (-400, -100)
    map_range_node.inputs['From Min'].default_value = 0.0
    map_range_node.inputs['From Max'].default_value = 1.0
    map_range_node.inputs['To Min'].default_value = 0.0
    map_range_node.inputs['To Max'].default_value = 1.0
    links.new(dot_product_node.outputs['Value'], map_range_node.inputs['Value'])

    # Connect to Mix factor
    links.new(map_range_node.outputs['Result'], mix_node.inputs['Fac'])

    # Connect Mix to BSDF
    links.new(mix_node.outputs['Result'], bsdf_node.inputs['Base Color'])

    # Connect BSDF to Output
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])

    return mat

def create_era_0_materials():
    """
    Create Era 0 (Ancient Colchis) palette materials.
    Base: #2D5A3D, Highlight: #4CAF50, Shadow: #1B3A26, Accent: #D4A017
    """
    era_0_colors = {
        'Base': (0.176, 0.353, 0.239, 1.0),  # #2D5A3D
        'Highlight': (0.298, 0.686, 0.314, 1.0),  # #4CAF50
        'Shadow': (0.106, 0.227, 0.149, 1.0),  # #1B3A26
        'Accent': (0.831, 0.627, 0.090, 1.0),  # #D4A017
    }

    materials = {}

    # Create cel-shader materials for each color
    materials['Base'] = create_cel_shader_material(
        era_0_colors['Base'],
        era_0_colors['Shadow'],
        era_0_colors['Highlight'],
        name="Era0_Base_CelShader"
    )

    materials['Shadow'] = create_cel_shader_material(
        era_0_colors['Shadow'],
        (0.05, 0.1, 0.07, 1.0),
        era_0_colors['Base'],
        name="Era0_Shadow_CelShader"
    )

    materials['Accent'] = create_cel_shader_material(
        era_0_colors['Accent'],
        (0.6, 0.45, 0.05, 1.0),
        (1.0, 0.9, 0.3, 1.0),
        name="Era0_Accent_CelShader"
    )

    return materials

def setup_freestyle():
    """
    Configure Freestyle for outline rendering.
    Line thickness: 2.0 pixels for standard assets, 3.0 pixels for character models.
    Line color: #1A1A1A (near-black).
    """
    scene = bpy.context.scene

    # Enable Freestyle
    scene.render.use_freestyle = True

    # Get Freestyle line set
    if scene.view_layers and scene.view_layers[0].freestyle_settings.linesets:
        lineset = scene.view_layers[0].freestyle_settings.linesets[0]
    else:
        lineset = scene.view_layers[0].freestyle_settings.linesets.new("Outline")

    # Configure line set
    lineset.select_silhouette = True
    lineset.select_border = True
    lineset.select_crease = True
    lineset.crease_angle = math.radians(60)

    # Line style
    linestyle = lineset.linestyle
    linestyle.color = (0.102, 0.102, 0.102)  # #1A1A1A
    linestyle.thickness = 2.0  # 2 pixels for standard assets

    # Uniform thickness (no modulation)
    linestyle.use_chaining = True

def setup_render_settings():
    """
    Render Resolution: 256x256 pixels per frame (per v2.1 spec).
    Output format = PNG with RGBA (alpha channel).
    Color depth = 8-bit per channel (sRGB).
    Anti-aliasing = 8x multisample.
    No post-processing effects.
    """
    scene = bpy.context.scene

    # Resolution (256x256 for all sprites)
    scene.render.resolution_x = 256
    scene.render.resolution_y = 256
    scene.render.resolution_percentage = 100

    # Output format
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '8'

    # Transparent background
    scene.render.film_transparent = True

    # Anti-aliasing: 8x multisample
    scene.render.antialiasing_samples = '8'

    # Disable post-processing
    scene.render.use_compositing = False
    scene.render.use_sequencer = False

    # Engine
    scene.render.engine = 'BLENDER_EEVEE'

    # EEVEE settings for clean cel-shaded look
    scene.eevee.taa_render_samples = 64
    scene.eevee.use_taa_reprojection = True

def save_scene(filepath):
    """Save the scene template"""
    bpy.ops.wm.save_as_mainfile(filepath=filepath)
    print(f"✓ Scene template saved to: {filepath}")

def main():
    """Main template creation function"""
    print("Creating Standardized Blender Scene Template (v2.1)...")

    # Setup scene
    clear_scene()
    setup_camera()
    setup_lighting()
    create_era_0_materials()
    setup_freestyle()
    setup_render_settings()

    # Save to library directory
    script_dir = "/home/socraticblock/hermes-workspace/hermes/development/sakartvelo-defenders/blender_assets"
    library_dir = f"{script_dir}/library"
    os.makedirs(library_dir, exist_ok=True)

    output_path = f"{library_dir}/shared_scene_template_v2.1.blend"
    save_scene(output_path)

    print("\n✓ Standardized Scene Template Created Successfully!")
    print("\nSpecifications (per v2.1):")
    print("  Camera: Orthographic, X=60°, Y=0°, Z=45°")
    print("  Lighting: Single Sun from upper-left")
    print("  Materials: Cel-shading with Geometry nodes")
    print("  Freestyle: Enabled, 2px outlines, #1A1A1A")
    print("  Resolution: 256x256 pixels")
    print("  Anti-aliasing: 8x multisample")
    print("  Format: PNG with RGBA")
    print("\nUse this template as the starting point for all asset rendering!")

if __name__ == "__main__":
    main()
