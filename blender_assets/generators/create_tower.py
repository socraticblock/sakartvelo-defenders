#!/usr/bin/env python3
"""
Generate Simple Tower Model (Era 0 - Ancient Colchis)
Run in Blender: blender -b isometric_template.blend -P create_tower.py
"""

import bpy
import math

def clear_scene():
    """Clear all objects except camera and lights"""
    for obj in bpy.data.objects:
        if obj.name not in ["IsoCamera", "MainLight", "FillLight"]:
            bpy.data.objects.remove(obj, do_unlink=True)

def create_stone_watchtower():
    """Create a simple stone watchtower"""

    # Base (cube)
    bpy.ops.mesh.primitive_cube_add(
        size=1.2,
        location=(0, 0, 0.6)
    )
    base = bpy.context.active_object
    base.name = "Tower_Base"

    # Main tower body (cylinder)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.5,
        depth=1.5,
        location=(0, 0, 1.5)
    )
    body = bpy.context.active_object
    body.name = "Tower_Body"

    # Top platform (cylinder)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.6,
        depth=0.2,
        location=(0, 0, 2.4)
    )
    platform = bpy.context.active_object
    platform.name = "Tower_Platform"

    # Roof (cone)
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.7,
        radius2=0.0,
        depth=0.8,
        location=(0, 0, 2.9)
    )
    roof = bpy.context.active_object
    roof.name = "Tower_Roof"

    # Battlements (small cubes around platform)
    for i in range(4):
        angle = math.radians(i * 90)
        x = 0.5 * math.cos(angle)
        y = 0.5 * math.sin(angle)

        bpy.ops.mesh.primitive_cube_add(
            size=0.15,
            location=(x, y, 2.55)
        )
        battlement = bpy.context.active_object
        battlement.name = f"Battlement_{i}"

    # Join all parts
    all_objects = [obj for obj in bpy.context.selected_objects]
    if len(all_objects) > 1:
        bpy.context.view_layer.objects.active = all_objects[0]
        bpy.ops.object.join()

    return bpy.context.active_object

def apply_cel_material(obj, color=(0.4, 0.4, 0.45, 1.0)):
    """Apply cel-shaded material to object"""
    mat_name = "Tower_E0_Material"
    if mat_name in bpy.data.materials:
        mat = bpy.data.materials[mat_name]
    else:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes

        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Roughness'].default_value = 0.1
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Base Color'].default_value = color

    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

def setup_model_for_render(obj):
    """Position model for optimal rendering"""
    obj.location = (0, 0, 0)
    obj.rotation_euler = (0, 0, 0)
    obj.scale = (1, 1, 1)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

def save_model(filepath):
    """Save the model"""
    bpy.ops.wm.save_as_mainfile(filepath=filepath)
    print(f"✓ Model saved to: {filepath}")

def main():
    """Main generation function"""
    print("Generating Era 0 Stone Watchtower...")

    clear_scene()
    tower = create_stone_watchtower()
    apply_cel_material(tower, color=(0.45, 0.42, 0.38, 1.0))  # Stone gray
    setup_model_for_render(tower)

    script_dir = "/home/socraticblock/hermes-workspace/hermes/development/sakartvelo-defenders/blender_assets"
    models_dir = f"{script_dir}/models/towers"
    import os
    os.makedirs(models_dir, exist_ok=True)

    output_path = f"{models_dir}/tower_e00_stone_watchtower.blend"
    save_model(output_path)

    print("✓ Stone Watchtower created successfully!")
    print(f"  Open in Blender: {output_path}")

if __name__ == "__main__":
    main()
