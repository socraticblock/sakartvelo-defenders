#!/usr/bin/env python3
"""
Generate Simple Enemy Model (Era 0 - Ancient Colchis)
Run in Blender: blender -b isometric_template.blend -P create_enemy.py
Or: Open Blender, open this file in Text Editor, click Run
"""

import bpy
import math

def clear_scene():
    """Clear all objects except camera and lights"""
    for obj in bpy.data.objects:
        if obj.name not in ["IsoCamera", "MainLight", "FillLight"]:
            bpy.data.objects.remove(obj, do_unlink=True)

def create_primitive_warrior():
    """Create a simple primitive warrior enemy"""

    # Body (cylinder)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.3,
        depth=0.8,
        location=(0, 0, 0.5)
    )
    body = bpy.context.active_object
    body.name = "Enemy_E0_PrimitiveWarrior"

    # Head (sphere)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.25,
        location=(0, 0, 1.0)
    )
    head = bpy.context.active_object
    head.name = "Head"

    # Arms (small cylinders)
    # Left arm
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.08,
        depth=0.4,
        location=(-0.4, 0, 0.6),
        rotation=(0, 0, math.radians(-20))
    )
    left_arm = bpy.context.active_object
    left_arm.name = "LeftArm"

    # Right arm (holding weapon)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.08,
        depth=0.4,
        location=(0.4, 0, 0.6),
        rotation=(0, 0, math.radians(20))
    )
    right_arm = bpy.context.active_object
    right_arm.name = "RightArm"

    # Simple club/weapon
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.05,
        depth=0.8,
        location=(0.6, 0, 1.0),
        rotation=(0, 0, math.radians(45))
    )
    weapon = bpy.context.active_object
    weapon.name = "Weapon"

    # Legs (small cylinders)
    # Left leg
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.1,
        depth=0.3,
        location=(-0.15, 0, 0.1)
    )
    left_leg = bpy.context.active_object
    left_leg.name = "LeftLeg"

    # Right leg
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.1,
        depth=0.3,
        location=(0.15, 0, 0.1)
    )
    right_leg = bpy.context.active_object
    right_leg.name = "RightLeg"

    # Join all parts
    all_parts = [body, head, left_arm, right_arm, weapon, left_leg, right_leg]
    for part in all_parts[1:]:  # Select all except body
        part.select_set(True)
    body.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.join()

    return bpy.context.active_object

def apply_cel_material(obj, color=(0.6, 0.4, 0.2, 1.0)):
    """Apply cel-shaded material to object"""
    # Create material if it doesn't exist
    mat_name = "Enemy_E0_Material"
    if mat_name in bpy.data.materials:
        mat = bpy.data.materials[mat_name]
    else:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes

        # Get principled BSDF
        bsdf = nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Roughness'].default_value = 0.0
            bsdf.inputs['Metallic'].default_value = 0.0
            bsdf.inputs['Base Color'].default_value = color

    # Assign material to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

def setup_model_for_render(obj):
    """Position model for optimal rendering"""
    # Center at origin
    obj.location = (0, 0, 0)
    obj.rotation_euler = (0, 0, 0)
    obj.scale = (1, 1, 1)

    # Apply transforms
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

def save_model(filepath):
    """Save the model"""
    bpy.ops.wm.save_as_mainfile(filepath=filepath)
    print(f"✓ Model saved to: {filepath}")

def main():
    """Main generation function"""
    print("Generating Era 0 Primitive Warrior Enemy...")

    # Clear scene
    clear_scene()

    # Create model
    enemy = create_primitive_warrior()

    # Apply material (brown/tan for ancient primitive look)
    apply_cel_material(enemy, color=(0.65, 0.45, 0.25, 1.0))

    # Setup for rendering
    setup_model_for_render(enemy)

    # Save model
    script_dir = "/home/socraticblock/hermes-workspace/hermes/development/sakartvelo-defenders/blender_assets"
    models_dir = f"{script_dir}/models/enemies"
    import os
    os.makedirs(models_dir, exist_ok=True)

    output_path = f"{models_dir}/enemy_e00_primitive_warrior.blend"
    save_model(output_path)

    print("✓ Primitive Warrior Enemy created successfully!")
    print(f"  Open in Blender: {output_path}")
    print("  Press F12 to render preview, or run render_helper.py to export sprite")

if __name__ == "__main__":
    main()
