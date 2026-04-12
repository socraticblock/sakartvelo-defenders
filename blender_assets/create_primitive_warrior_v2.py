#!/usr/bin/env python3
"""
Create Primitive Warrior Model (Era 0 Enemy) v2
Based on specification: specs/enemy_e00_primitive_warrior_spec.md

Run: blender -b library/shared_scene_template_v2.1.blend -P create_primitive_warrior_v2.py
"""

import bpy
import math
from math import radians

def clear_model():
    """Clear existing mesh objects (keep camera, lights, materials)"""
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            bpy.data.objects.remove(obj, do_unlink=True)

def get_material(name):
    """Get material from template, return default if not found"""
    if name in bpy.data.materials:
        return bpy.data.materials[name]

    # Fallback colors if materials not found
    colors = {
        'Era0_Shadow': (0.106, 0.227, 0.149, 1.0),
        'Era0_Stone': (0.545, 0.455, 0.333, 1.0),
        'Era0_Accent': (0.831, 0.627, 0.090, 1.0),
    }

    if name in colors:
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = colors[name]
        bsdf.inputs['Roughness'].default_value = 1.0
        bsdf.inputs['Metallic'].default_value = 0.0
        return mat

    print(f"Warning: Material {name} not found, using default")
    return bpy.data.materials[0]

def create_primitive_warrior():
    """Create primitive warrior based on specification"""

    # Group all parts
    parts = []

    # === HEAD (Skin - Stone/Earth) ===
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.35,
        location=(0, 0, 2.5),
        scale=(1.0, 1.0, 1.2)  # Slightly elongated
    )
    head = bpy.context.active_object
    head.name = "Head_Skin"
    head.data.materials.append(get_material('Era0_Stone'))
    parts.append(head)

    # === HAIR (Animal fur - Shadow) ===
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.38,
        location=(0, 0, 2.65),
        scale=(1.0, 1.0, 0.5),
        rotation=(0, 0, radians(20))
    )
    hair = bpy.context.active_object
    hair.name = "Hair_Fur"
    hair.data.materials.append(get_material('Era0_Shadow'))
    parts.append(hair)

    # === TORSO (Animal fur - Shadow) ===
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.4,
        depth=1.0,
        location=(0, 0, 1.6)
    )
    torso = bpy.context.active_object
    torso.name = "Torso_Fur"
    torso.data.materials.append(get_material('Era0_Shadow'))
    parts.append(torso)

    # Fur trim on shoulders (small spheres)
    for x_pos in [-0.35, 0.35]:
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.2,
            location=(x_pos, 0, 2.0),
            scale=(1.5, 1.0, 0.8)
        )
        shoulder_fur = bpy.context.active_object
        shoulder_fur.name = f"Shoulder_Fur_{x_pos}"
        shoulder_fur.data.materials.append(get_material('Era0_Shadow'))
        parts.append(shoulder_fur)

    # Fur texture bumps on torso (for detail)
    for i in range(6):
        angle = radians(i * 60)
        x = 0.35 * math.cos(angle)
        y = 0.35 * math.sin(angle)
        z = 1.6 + (i % 2) * 0.3

        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.06,
            location=(x, y, z),
            scale=(1.2, 1.2, 0.8)
        )
        fur_bump = bpy.context.active_object
        fur_bump.name = f"Torso_Fur_Bump_{i}"
        fur_bump.data.materials.append(get_material('Era0_Shadow'))
        parts.append(fur_bump)

    # === ARMS ===

    # Right arm (skin + leather wrap)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.12,
        depth=0.6,
        location=(0.5, 0, 1.9),
        rotation=(0, 0, radians(-15))
    )
    right_arm = bpy.context.active_object
    right_arm.name = "Right_Arm_Skin"
    right_arm.data.materials.append(get_material('Era0_Stone'))
    parts.append(right_arm)

    # Left arm (skin + leather wrap)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.12,
        depth=0.6,
        location=(-0.5, 0, 1.9),
        rotation=(0, 0, radians(15))
    )
    left_arm = bpy.context.active_object
    left_arm.name = "Left_Arm_Skin"
    left_arm.data.materials.append(get_material('Era0_Stone'))
    parts.append(left_arm)

    # Forearm leather wraps (Shadow)
    for side, x_base, rot in [("Right", 0.5, -15), ("Left", -0.5, 15)]:
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.13,
            depth=0.4,
            location=(x_base + 0.15 * (1 if side == "Right" else -1), 0, 1.5),
            rotation=(0, 0, radians(rot))
        )
        forearm_wrap = bpy.context.active_object
        forearm_wrap.name = f"{side}_Forearm_Leather"
        forearm_wrap.data.materials.append(get_material('Era0_Shadow'))
        parts.append(forearm_wrap)

    # === HANDS (Skin) ===
    for side, x_base, rot in [("Right", 0.65, -15), ("Left", -0.65, 15)]:
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.1,
            location=(x_base, 0, 1.2)
        )
        hand = bpy.context.active_object
        hand.name = f"{side}_Hand_Skin"
        hand.data.materials.append(get_material('Era0_Stone'))
        parts.append(hand)

    # === LEGS (Leather wraps - Shadow) ===
    for x_pos in [-0.2, 0.2]:
        # Upper leg (skin, partially covered)
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.15,
            depth=0.5,
            location=(x_pos, 0, 0.9)
        )
        upper_leg = bpy.context.active_object
        upper_leg.name = f"Leg_Skin_{x_pos}"
        upper_leg.data.materials.append(get_material('Era0_Stone'))
        parts.append(upper_leg)

        # Lower leg (leather wraps)
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.16,
            depth=0.5,
            location=(x_pos, 0, 0.4)
        )
        lower_leg = bpy.context.active_object
        lower_leg.name = f"Leg_Leather_{x_pos}"
        lower_leg.data.materials.append(get_material('Era0_Shadow'))
        parts.append(lower_leg)

    # === FEET (Skin - Stone/Earth) ===
    for x_pos in [-0.2, 0.2]:
        bpy.ops.mesh.primitive_cube_add(
            size=0.25,
            location=(x_pos, 0.05, 0.1),
            scale=(1.5, 1.2, 0.6)
        )
        foot = bpy.context.active_object
        foot.name = f"Foot_Skin_{x_pos}"
        foot.data.materials.append(get_material('Era0_Stone'))
        parts.append(foot)

    # === WAIST BELT (Shadow - for detail) ===
    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.42,
        minor_radius=0.04,
        location=(0, 0, 1.2),
        rotation=(radians(90), 0, 0)
    )
    belt = bpy.context.active_object
    belt.name = "Waist_Belt"
    belt.data.materials.append(get_material('Era0_Shadow'))
    parts.append(belt)

    # Belt buckle (Stone/Earth - primitive)
    bpy.ops.mesh.primitive_cube_add(
        size=0.08,
        location=(0.42, 0, 1.2),
        scale=(1, 2, 1)
    )
    belt_buckle = bpy.context.active_object
    belt_buckle.name = "Belt_Buckle"
    belt_buckle.data.materials.append(get_material('Era0_Stone'))
    parts.append(belt_buckle)

    # === NECKLACE (Gold - Accent) ===
    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.25,
        minor_radius=0.03,
        location=(0, 0, 2.15),
        rotation=(radians(90), 0, 0)
    )
    necklace = bpy.context.active_object
    necklace.name = "Necklace_Gold"
    necklace.data.materials.append(get_material('Era0_Accent'))
    parts.append(necklace)

    # === WRISTBANDS (Gold - Accent) ===
    for side, x_base, z_pos in [("Right", 0.65, 1.25), ("Left", -0.65, 1.25)]:
        bpy.ops.mesh.primitive_torus_add(
            major_radius=0.12,
            minor_radius=0.02,
            location=(x_base, 0, z_pos),
            rotation=(radians(90), 0, 0)
        )
        wristband = bpy.context.active_object
        wristband.name = f"Wristband_Gold_{side}"
        wristband.data.materials.append(get_material('Era0_Accent'))
        parts.append(wristband)

    # === WEAPON (Wooden club - Stone/Earth) ===
    # Single connected club by overlapping cylinders at SAME location

    # Handle (lower, thinner part)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.06,
        depth=1.0,
        location=(1.15, 0.55, 1.55),
        rotation=(radians(30), 0, radians(70))
    )
    handle = bpy.context.active_object
    handle.name = "Club_Handle"
    handle.data.materials.append(get_material('Era0_Stone'))
    parts.append(handle)

    # Head (upper, thicker part) - SAME LOCATION as handle center
    # This creates guaranteed overlap/attachment
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.18,
        depth=0.6,
        location=(1.15, 0.55, 1.55),  # EXACT SAME location as handle!
        rotation=(radians(30), 0, radians(70))
    )
    head = bpy.context.active_object
    head.name = "Club_Head"
    head.data.materials.append(get_material('Era0_Stone'))
    parts.append(head)

    # Decorative band
    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.18,
        minor_radius=0.02,
        location=(1.15, 0.55, 1.55),
        rotation=(radians(30), 0, radians(70))
    )
    band = bpy.context.active_object
    band.name = "Club_Band"
    band.data.materials.append(get_material('Era0_Shadow'))
    parts.append(band)

    # === SHIELD (Wood + hide - Stone/Earth + Shadow) ===
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.38,
        depth=0.08,
        location=(-0.75, 0.15, 1.5),
        rotation=(radians(45), 0, 0)
    )
    shield = bpy.context.active_object
    shield.name = "Shield_Wood"
    shield.data.materials.append(get_material('Era0_Stone'))
    parts.append(shield)

    # Shield rim (Shadow - for detail)
    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.38,
        minor_radius=0.04,
        location=(-0.75, 0.05, 1.5),
        rotation=(radians(45), 0, 0)
    )
    shield_rim = bpy.context.active_object
    shield_rim.name = "Shield_Rim"
    shield_rim.data.materials.append(get_material('Era0_Shadow'))
    parts.append(shield_rim)

    # Shield boss (center decoration - Shadow)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.12,
        depth=0.12,
        location=(-0.75, -0.1, 1.5),
        rotation=(radians(45), 0, 0)
    )
    shield_boss = bpy.context.active_object
    shield_boss.name = "Shield_Boss"
    shield_boss.data.materials.append(get_material('Era0_Shadow'))
    parts.append(shield_boss)

    # Shield pattern lines (for detail - Shadow)
    for angle in [0, 45, 90, 135]:
        rad_angle = radians(angle)
        bpy.ops.mesh.primitive_cube_add(
            size=0.03,
            location=(-0.75 + 0.25 * math.cos(rad_angle), -0.05 + 0.25 * math.sin(rad_angle), 1.5),
            rotation=(0, 0, rad_angle),
            scale=(1, 4, 1)
        )
        shield_line = bpy.context.active_object
        shield_line.name = f"Shield_Pattern_{angle}"
        shield_line.data.materials.append(get_material('Era0_Shadow'))
        parts.append(shield_line)

    # Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.select_set(True)

    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()

    return bpy.context.active_object

def setup_model_for_render(obj):
    """Position model for optimal rendering"""
    # Center vertically
    obj.location = (0, 0, 0)

    # Apply transforms
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    return obj

def save_model(filepath):
    """Save the model"""
    bpy.ops.wm.save_as_mainfile(filepath=filepath)
    print(f"✓ Model saved: {filepath}")

def main():
    """Main generation function"""
    print("Creating Primitive Warrior Model (v2)...")
    print("Based on specification: specs/enemy_e00_primitive_warrior_spec.md")

    clear_model()
    warrior = create_primitive_warrior()
    setup_model_for_render(warrior)

    script_dir = "/home/socraticblock/hermes-workspace/hermes/development/sakartvelo-defenders/blender_assets"
    models_dir = f"{script_dir}/models/enemies"
    import os
    os.makedirs(models_dir, exist_ok=True)

    output_path = f"{models_dir}/enemy_e00_primitive_warrior_v2.blend"
    save_model(output_path)

    print("\n✓ Primitive Warrior v2 Created Successfully!")
    print(f"  Location: {output_path}")
    print("\nModel Features:")
    print("  • Animal fur/skin on torso (Shadow #1B3A26)")
    print("  • Leather wraps on legs and forearms (Shadow #1B3A26)")
    print("  • Gold necklace and wristbands (Accent #D4A017)")
    print("  • Wooden club weapon (Stone/Earth #8B7355)")
    print("  • Round shield (Stone/Earth + Shadow)")
    print("  • Skin tone (Stone/Earth #8B7355)")
    print("  • Tribal/feral posture")
    print("\nReady for rendering!")

if __name__ == "__main__":
    main()
