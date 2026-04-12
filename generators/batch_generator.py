"""
Sakartvelo Defenders - Batch Asset Generator
Generates all code-generated assets for Era 0-1
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from sprite_generator import TowerGenerator, ERA_PALETTES
from enemy_generator import EnemyGenerator
from hero_portrait_generator import HeroPortraitGenerator
from map_generator import MapGenerator

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def generate_era_towers(era: int):
    """Generate all 10 tower types for a given era."""
    gen = TowerGenerator(size=512)
    era_info = ERA_PALETTES[era]
    era_code = f"e{era:02d}"
    era_name = era_info.name.lower().replace(" ", "_")
    output_dir = os.path.join(ASSETS_DIR, "towers", f"{era_code}_{era_name}")
    os.makedirs(output_dir, exist_ok=True)

    tower_types = ["archer", "catapult", "wall", "shrine", "cavalry",
                   "gunpowder", "industrial", "bunker", "tech", "special"]

    for tower_type in tower_types:
        tower = gen.generate_tower(tower_type, era)
        filename = f"twr_{era_code}_{tower_type}_v01.png"
        tower.save(os.path.join(output_dir, filename))

    print(f"  ✓ {len(tower_types)} towers for Era {era} ({era_info.name})")

def generate_era_enemies(era: int):
    """Generate enemies for a given era."""
    gen = EnemyGenerator(size=512)
    era_info = ERA_PALETTES[era]
    era_code = f"e{era:02d}"
    era_name = era_info.name.lower().replace(" ", "_")
    output_dir = os.path.join(ASSETS_DIR, "enemies", f"{era_code}_{era_name}")
    os.makedirs(output_dir, exist_ok=True)

    # Era 0 enemies
    if era == 0:
        enemies = ["tribal_raider_infantry", "greek_colonist_infantry"]
    elif era == 1:
        enemies = ["roman_legionary_infantry", "persian_archer"]
    else:
        enemies = ["infantry_default"]

    for enemy_type in enemies:
        try:
            enemy = gen.generate_enemy(enemy_type, era)
            filename = f"ene_{era_code}_{enemy_type}_v01.png"
            enemy.save(os.path.join(output_dir, filename))
        except Exception as e:
            print(f"  ✗ {enemy_type}: {e}")

    print(f"  ✓ {len(enemies)} enemies for Era {era} ({era_info.name})")

def generate_era_heroes(era: int):
    """Generate hero portraits for a given era."""
    gen = HeroPortraitGenerator(size=1024)
    era_info = ERA_PALETTES[era]
    era_code = f"e{era:02d}"
    era_name = era_info.name.lower().replace(" ", "_")
    output_dir = os.path.join(ASSETS_DIR, "heroes", f"{era_code}_{era_name}")
    os.makedirs(output_dir, exist_ok=True)

    hero_map = {
        0: ["medea"],
        1: ["st_nino", "vakhtang_gorgasali"],
        3: ["david_iv", "queen_tamar"],
        5: ["erekle_ii"],
    }

    heroes = hero_map.get(era, [])

    for hero_name in heroes:
        try:
            hero = gen.generate_hero_portrait(hero_name, era)
            filename = f"her_{era_code}_{hero_name}_v01.png"
            hero.save(os.path.join(output_dir, filename))
        except Exception as e:
            print(f"  ✗ {hero_name}: {e}")

    print(f"  ✓ {len(heroes)} heroes for Era {era} ({era_info.name})")

def generate_era_maps(era: int, count: int = 5):
    """Generate map backgrounds for a given era."""
    gen = MapGenerator(size=2048)
    era_info = ERA_PALETTES[era]
    era_code = f"e{era:02d}"
    era_name = era_info.name.lower().replace(" ", "_")
    output_dir = os.path.join(ASSETS_DIR, "maps", f"{era_code}_{era_name}")
    os.makedirs(output_dir, exist_ok=True)

    mood_map = {
        0: "misty",
        1: "clear",
        2: "stormy",
        3: "golden",
        4: "somber",
        5: "warm",
        6: "industrial",
        7: "dramatic",
        8: "gray",
        9: "night",
    }

    mood = mood_map.get(era, "misty")

    map_names = [
        f"{era_name}_map_{i+1:02d}" for i in range(count)
    ]

    for map_name in map_names:
        try:
            map_img = gen.generate_map(map_name, era, mood)
            filename = f"map_{era_code}_{map_name}_v01.jpg"
            map_img.save(os.path.join(output_dir, filename), quality=95)
        except Exception as e:
            print(f"  ✗ {map_name}: {e}")

    print(f"  ✓ {count} maps for Era {era} ({era_info.name})")

if __name__ == "__main__":
    print("=" * 60)
    print("Sakartvelo Defenders - Batch Asset Generator")
    print("=" * 60)

    print("\n[1/4] Generating Era 0 assets...")
    generate_era_towers(0)
    generate_era_enemies(0)
    generate_era_heroes(0)
    generate_era_maps(0, count=5)

    print("\n[2/4] Generating Era 1 assets...")
    generate_era_towers(1)
    generate_era_enemies(1)
    generate_era_heroes(1)
    generate_era_maps(1, count=5)

    print("\n[3/4] Generating silhouette sheets for all eras...")
    gen = TowerGenerator(size=512)
    for era in range(10):
        try:
            sheet = gen.generate_tower_silhouette_sheet(era)
            era_info = ERA_PALETTES[era]
            era_name = era_info.name.lower().replace(" ", "_")
            output_path = os.path.join(ASSETS_DIR, "towers", f"tower_silhouette_sheet_e{era:02d}.png")
            sheet.save(output_path)
            print(f"  ✓ Silhouette sheet for Era {era} ({era_info.name})")
        except Exception as e:
            print(f"  ✗ Era {era}: {e}")

    print("\n[4/4] Counting all generated assets...")
    total_files = 0
    for root, dirs, files in os.walk(ASSETS_DIR):
        for f in files:
            if f.endswith(('.png', '.jpg', '.svg')):
                total_files += 1

    print(f"\n{'=' * 60}")
    print(f"COMPLETE: {total_files} assets generated")
    print(f"{'=' * 60}")
