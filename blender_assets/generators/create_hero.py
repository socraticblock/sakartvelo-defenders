#!/usr/bin/env python3
"""
Generate Hero Model (Era 0 - Ancient Colchis)
Run in Blender: blender -b isometric_template.blend -P create_hero.py
"""

import bpy
import math

def clear_scene():
    """Clear all objects except camera and lights"""
    for obj in bpy.data.objects:
        if obj.name not in ["IsoCamera", "MainLight", "FillLight"]:
            bpy.data.objects.remove(obj, do_unlink=True)

def create_ancient_hero():
    """Create a detailed ancient hero/king"""

    # Body (cylinder)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.35,
        depth=1.0,
        location=(0, 0, 0.6)
    )
    body = bpy.context.active_object
    body.name = "Hero_Body"

    # Head (sphere)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.28,
        location=(0, 0, 1.2)
    )
    head = bpy.context.active_object
    head.name = "Hero_Head"

    # Helmet (slightly larger sphere on top of head)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.32,
        location=(0, 0, 1.25),
        scale=(1, 1, 0.6)
    )
    helmet = bpy.context.active_object
    helmet.name = "Hero_Helmet"

    # Helmet crest (cylinder on top)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.05,
        depth=0.4,
        location=(0, 0, 1.55)
    )
    crest = bpy.context.active_object
    crest.name = "Hero_Crest"

    # Shoulders/Armor (two spheres)
    # Left shoulder
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.25,
        location=(-0.5, 0, 1.0),
        scale=(0.8, 1, 0.8)
    )
    left_shoulder = bpy.context.active_object
    left_shoulder.name = "Left_Shoulder"

    # Right shoulder
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.25,
        location=(0.5, 0, 1.0),
        scale=(0.8, 1, 0.8)
    )
    right_shoulder = bpy.context.active_object
    right_shoulder.name = "Right_Shoulder"

    # Arms (cylinders)
    # Left arm (holding shield side)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.1,
        depth=0.6,
        location=(-0.6, 0, 0.8),
        rotation=(0, 0, math.radians(-15))
    )
    left_arm = bpy.context.active_object
    left_arm.name = "Left_Arm"

    # Right arm (holding sword)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.1,
        depth=0.6,
        location=(0.6, 0, 0.8),
        rotation=(0, 0, math.radians(15))
    )
    right_arm = bpy.context.active_object
    right_arm.name = "Right_Arm"

    # Sword (long cylinder with cone tip)
    # Blade
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.04,
        depth=1.2,
        location=(0.9, 0, 1.1),
        rotation=(0, 0, math.radians(60))
    )
    blade = bpy.context.active_object
    blade.name = "Sword_Blade"

    # Sword tip (cone)
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.04,
        radius2=0.0,
        depth=0.3,
        location=(1.2, 0.8, 1.5),
        rotation=(0, 0, math.radians(60))
    )
    sword_tip = bpy.context.active_object
    sword_tip.name = "Sword_Tip"

    # Shield (flattened cylinder on left arm)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.4,
        depth=0.05,
        location=(-0.8, 0.2, 0.7),
        rotation=(math.radians(45), 0, 0)
    )
    shield = bpy.context.active_object
    shield.name = "Shield"

    # Legs (cylinders)
    # Left leg
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.12,
        depth=0.5,
        location=(-0.2, 0, 0.15)
    )
    left_leg = bpy.context.active_object
    left_leg.name = "Left_Leg"

    # Right leg
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.12,
        depth=0.5,
        location=(0.2, 0, 0.15)
    )
    right_leg = bpy.context.active_object
    right_leg.name = "Right_Leg"

    # Cape (plane behind)
    bpy.ops.mesh.primitive_plane_add(
        size=1.0,
        location=(0, -0.5, 1.0),
        rotation=(math.radians(-10), 0, 0)
    )
    cape = bpy.context.active_object
    cape.name = "Cape"

    # Join all parts
    all_objects = [obj for obj in bpy.context.selected_objects]
    if len(all_objects) > 1:
        bpy.context.view_layer.objects.active = all_objects[0]
        bpy.ops.object.join()

    return bpy.context.active_object

def apply_hero_materials(obj):
    """Apply cel-shaded materials to hero parts"""
    # Body material (bronze/armor)
    body_mat = bpy.data.materials.new(name="Hero_Body_Material")
    body_mat.use_nodes = True
    bsdf = body_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Roughness'].default_value = 0.1
        bsdf.inputs['Metallic'].default_value = 0.8
        bsdf.inputs['Base Color'].default_value = (0.8, 0.5, 0.2, 1.0)  # Bronze

    # Head material (skin tone)
    head_mat = bpy.data.materials.new(name="Hero_Skin_Material")
    head_mat.use_nodes = True
    bsdf = head_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Roughness'].default_value = 0.3
        bsdf.inputs['Metallic'].default_value = 0.0
        bsdf.inputs['Base Color'].default_value = (0.9, 0.7, 0.6, 1.0)  # Skin

    # Gold material (helmet, crest, details)
    gold_mat = bpy.data.materials.new(name="Hero_Gold_Material")
    gold_mat.use_nodes = True
    bsdf = gold_mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Roughness'].default_value = 0.1
        bsdf.inputs['Metallic'].default_value = 1.0
        bsdf.inputs['Base Color'].default_value = (1.0, 0.8, 0.2, 1.0)  # Gold

    # Apply materials based on object name
    if "Head" in obj.name and "Helmet" not in obj.name:
        obj.data.materials.append(head_mat)
    elif "Helmet" in obj.name or "Crest" in obj.name or "Shield" in obj.name:
        obj.data.materials.append(gold_mat)
    else:
        obj.data.materials.append(body_mat)

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
    print("Generating Era 0 Ancient Hero...")

    clear_scene()
    hero = create_ancient_hero()
    apply_hero_materials(hero)
    setup_model_for_render(hero)

    script_dir = "/home/socraticblock/hermes-workspace/hermes/development/sakartvelo-defenders/blender_assets"
    models_dir = f"{script_dir}/models/heroes"
    import os
    os.makedirs(models_dir, exist_ok=True)

    output_path = f"{models_dir}/hero_e00_ancient_king.blend"
    save_model(output_path)

    print("✓ Ancient Hero created successfully!")
    print(f"  Open in Blender: {output_path}")

if __name__ == "__main__":
    main()
