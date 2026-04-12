#!/usr/bin/env python3
"""
Wave Composition Designer for Sakartvelo Defenders

Generates wave compositions for all 200 levels (10 eras x 20 levels)
with difficulty scaling, era-specific enemy variants, and boss encounters.

Usage:
    python3 wave_designer.py --output content/waves.json
    python3 wave_designer.py --validate content/waves.json
"""

import argparse
import json
import random
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional

# ---------------------------------------------------------------------------
# Era definitions
# ---------------------------------------------------------------------------

ERAS = [
    {"era_id": 0, "era_name": "Ancient Colchis"},
    {"era_id": 1, "era_name": "Kingdom of Iberia"},
    {"era_id": 2, "era_name": "Arab Conquests"},
    {"era_id": 3, "era_name": "Georgian Golden Age"},
    {"era_id": 4, "era_name": "Mongol Invasions"},
    {"era_id": 5, "era_name": "Between Empires"},
    {"era_id": 6, "era_name": "Russian Empire"},
    {"era_id": 7, "era_name": "First Democratic Republic"},
    {"era_id": 8, "era_name": "The Soviet Century"},
    {"era_id": 9, "era_name": "Modern Georgia"},
]

# Era-specific enemy variant names (thematic per era)
ERA_VARIANTS = {
    0: {
        "infantry": ["tribal_warrior", "axeman", "spearman"],
        "cavalry": ["scout_rider", "light_cavalry"],
        "siege": [],
        "flying": [],
        "boss": ["colchian_chieftain"],
    },
    1: {
        "infantry": ["iberian_soldier", "spearman", "archer"],
        "cavalry": ["iberian_cavalry", "mounted_archer"],
        "siege": [],
        "flying": [],
        "boss": ["king_pharnavaz"],
    },
    2: {
        "infantry": ["arab_warrior", "swordsman", "javelineer"],
        "cavalry": ["arab_horseman", "desert_raider"],
        "siege": ["battering_ram"],
        "flying": [],
        "boss": ["arab_commander"],
    },
    3: {
        "infantry": ["georgian_footman", "monaspa", "crossbowman"],
        "cavalry": ["georgian_knight", "monaspa_cavalry"],
        "siege": ["trebuchet"],
        "flying": [],
        "boss": ["seljuk_general"],
    },
    4: {
        "infantry": ["mongol_warrior", "archer", "spearman"],
        "cavalry": ["mongol_horseman", "heavy_mongol_rider"],
        "siege": ["mangonel", "siege_tower"],
        "flying": [],
        "boss": ["mongol_khan"],
    },
    5: {
        "infantry": ["persian_infantry", "ottoman_janissary", "musketeer"],
        "cavalry": ["persian_cavalry", "sipahi"],
        "siege": ["cannon"],
        "flying": [],
        "boss": ["shah_abbas"],
    },
    6: {
        "infantry": ["russian_soldier", "imperial_guard", "grenadier"],
        "cavalry": ["cossack", "dragoon"],
        "siege": ["heavy_cannon", "mortar"],
        "flying": ["recon_balloon"],
        "boss": ["tsar_general"],
    },
    7: {
        "infantry": ["georgian_volunteer", "national_guard", "rifleman"],
        "cavalry": ["cavalry_scout", "mounted_infantry"],
        "siege": ["field_gun"],
        "flying": ["recon_plane"],
        "boss": ["red_army_commissar"],
    },
    8: {
        "infantry": ["soviet_conscript", "red_army_soldier", "veteran"],
        "cavalry": ["mechanized_infantry"],
        "siege": ["katyusha", "anti_tank_gun"],
        "flying": ["recon_aircraft", "bomber"],
        "boss": ["soviet_commander"],
    },
    9: {
        "infantry": ["modern_soldier", "special_forces", "militant"],
        "cavalry": ["armored_transport", "ifv"],
        "siege": ["howitzer", "mlrs"],
        "flying": ["attack_helicopter", "drone"],
        "boss": ["enemy_commander"],
    },
}

# ---------------------------------------------------------------------------
# Difficulty tier configs
# ---------------------------------------------------------------------------

TIER_CONFIGS = {
    "early": {       # levels 1-5
        "wave_count_range": (3, 5),
        "enemies_per_wave_range": (5, 10),
        "allowed_types": ["infantry", "cavalry"],
        "boss_levels": {5},
    },
    "mid": {         # levels 6-10
        "wave_count_range": (4, 6),
        "enemies_per_wave_range": (8, 15),
        "allowed_types": ["infantry", "cavalry", "siege"],
        "boss_levels": {10},
    },
    "late": {        # levels 11-15
        "wave_count_range": (5, 7),
        "enemies_per_wave_range": (12, 20),
        "allowed_types": ["infantry", "cavalry", "siege", "flying"],
        "boss_levels": {15},
    },
    "final": {       # levels 16-20
        "wave_count_range": (6, 8),
        "enemies_per_wave_range": (15, 30),
        "allowed_types": ["infantry", "cavalry", "siege", "flying"],
        "boss_levels": {20},
    },
}


def get_tier(level: int) -> str:
    """Return the difficulty tier key for a level number (1-20)."""
    if level <= 5:
        return "early"
    elif level <= 10:
        return "mid"
    elif level <= 15:
        return "late"
    else:
        return "final"


def get_tier_config(level: int) -> dict:
    return TIER_CONFIGS[get_tier(level)]


def pick_variant(era_id: int, enemy_type: str, rng: random.Random, prefer_tough: bool = False) -> str:
    """Pick a variant from the era's variant list. Prefer later (tougher) variants if flagged."""
    variants = ERA_VARIANTS[era_id].get(enemy_type, [])
    if not variants:
        return "basic"
    if prefer_tough and len(variants) > 1:
        # Pick from the back half for tougher enemies
        idx = rng.randint(len(variants) // 2, len(variants) - 1)
        return variants[idx]
    return rng.choice(variants)


def is_boss_level(level: int) -> bool:
    return level in (5, 10, 15, 20)


# ---------------------------------------------------------------------------
# Wave generation
# ---------------------------------------------------------------------------

def generate_wave(
    wave_num: int,
    total_waves: int,
    level: int,
    era_id: int,
    config: dict,
    rng: random.Random,
    is_boss_wave: bool = False,
) -> dict:
    """Generate a single wave composition."""
    enemies = []

    if is_boss_wave:
        # Boss wave: one boss + support enemies
        boss_variants = ERA_VARIANTS[era_id].get("boss", ["boss"])
        boss_variant = rng.choice(boss_variants)
        enemies.append({"type": "boss", "count": 1, "variant": boss_variant})

        # 2-3 support enemy groups
        support_count = rng.randint(2, 3)
        for _ in range(support_count):
            etype = rng.choice(config["allowed_types"])
            count = rng.randint(2, 5)
            variant = pick_variant(era_id, etype, rng, prefer_tough=True)
            enemies.append({"type": etype, "count": count, "variant": variant})

    else:
        # Regular wave: mix of allowed types
        min_e, max_e = config["enemies_per_wave_range"]
        # Scale enemy count based on wave progression within level
        wave_progress = wave_num / max(total_waves, 1)
        base_count = min_e + int((max_e - min_e) * wave_progress)

        # Cross-era scaling: later eras inflate counts slightly
        era_scale = 1.0 + era_id * 0.05
        target_count = max(min_e, min(max_e, int(base_count * era_scale)))

        # Pick 1-3 different enemy types for variety
        num_types = rng.randint(1, min(3, len(config["allowed_types"])))
        chosen_types = rng.sample(config["allowed_types"], num_types)

        # Distribute count across types, weighted toward infantry
        remaining = target_count
        for i, etype in enumerate(chosen_types):
            if i == len(chosen_types) - 1:
                count = remaining
            else:
                # Infantry gets more share
                share = 0.5 if etype == "infantry" else 0.3
                count = max(1, int(remaining * share * rng.uniform(0.8, 1.2)))
                remaining -= count
                if remaining < len(chosen_types) - i - 1:
                    count += remaining - (len(chosen_types) - i - 1)
                    remaining = len(chosen_types) - i - 1

            if count < 1:
                count = 1

            # Tougher variants for later waves
            prefer_tough = wave_progress > 0.6
            variant = pick_variant(era_id, etype, rng, prefer_tough=prefer_tough)
            enemies.append({"type": etype, "count": count, "variant": variant})

    return {"wave": wave_num, "enemies": enemies}


def generate_level(level: int, era_id: int, rng: random.Random) -> dict:
    """Generate all waves for a single level."""
    config = get_tier_config(level)
    boss = is_boss_level(level)

    if boss:
        # Boss levels: normal waves + boss wave at the end + 2 support waves before boss
        support_waves = 2
        normal_wave_range = config["wave_count_range"]
        # Use lower end of normal wave range to keep total reasonable
        normal_count = rng.randint(normal_wave_range[0], normal_wave_range[1])
        total_waves = normal_count + support_waves + 1  # +1 for boss wave
    else:
        normal_wave_range = config["wave_count_range"]
        total_waves = rng.randint(normal_wave_range[0], normal_wave_range[1])

    waves = []
    wave_num = 1

    # Generate normal waves (all but last support_waves+1)
    normal_end = total_waves - support_waves - 1 if boss else total_waves
    for w in range(1, normal_end + 1):
        wave = generate_wave(w, total_waves, level, era_id, config, rng)
        waves.append(wave)
        wave_num = w + 1

    if boss:
        # Generate support waves (intensifying before boss)
        for w in range(wave_num, wave_num + support_waves):
            wave = generate_wave(w, total_waves, level, era_id, config, rng)
            waves.append(wave)
            wave_num = w + 1

        # Final boss wave
        boss_wave = generate_wave(wave_num, total_waves, level, era_id, config, rng, is_boss_wave=True)
        waves.append(boss_wave)

    return {"level": level, "waves": waves}


def generate_era(era_id: int, era_name: str, seed: Optional[int] = None) -> dict:
    """Generate all 20 levels for an era."""
    rng = random.Random(seed)
    levels = []
    for level in range(1, 21):
        level_data = generate_level(level, era_id, rng)
        levels.append(level_data)
    return {"era_id": era_id, "era_name": era_name, "levels": levels}


def generate_all_waves(seed: Optional[int] = 42) -> dict:
    """Generate complete wave data for all 200 levels."""
    rng = random.Random(seed)
    eras = []
    for era in ERAS:
        era_seed = rng.randint(0, 999999)
        era_data = generate_era(era["era_id"], era["era_name"], seed=era_seed)
        eras.append(era_data)
    return {"eras": eras}


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_waves(data: dict) -> list:
    """Validate wave data for balance issues. Returns list of warnings/errors."""
    issues = []
    total_levels = 0

    for era in data.get("eras", []):
        era_id = era.get("era_id", "?")
        era_name = era.get("era_name", "?")

        if len(era.get("levels", [])) != 20:
            issues.append(f"[ERROR] {era_name}: expected 20 levels, got {len(era.get('levels', []))}")

        for level_data in era.get("levels", []):
            level = level_data.get("level", "?")
            total_levels += 1
            waves = level_data.get("waves", [])

            if not waves:
                issues.append(f"[ERROR] {era_name} Level {level}: no waves defined")
                continue

            # Check wave count per tier
            tier = get_tier(level)
            config = get_tier_config(level)
            min_w, max_w = config["wave_count_range"]
            if is_boss_level(level):
                # Boss levels get +3 extra waves (2 support + 1 boss), adjust ceiling
                max_w += 3
            if len(waves) < min_w:
                issues.append(f"[WARN] {era_name} Level {level}: only {len(waves)} waves, expected >= {min_w}")
            if len(waves) > max_w:
                issues.append(f"[WARN] {era_name} Level {level}: {len(waves)} waves seems high (max ~{max_w})")

            # Check enemy counts per wave
            for wave in waves:
                wave_num = wave.get("wave", "?")
                total_enemies = sum(e.get("count", 0) for e in wave.get("enemies", []))

                # Flag if any wave has too many enemies (hard cap)
                if total_enemies > 50:
                    issues.append(f"[ERROR] {era_name} Level {level} Wave {wave_num}: {total_enemies} enemies (max 50)")

                # Flag if any wave has too few enemies
                if total_enemies < 1:
                    issues.append(f"[ERROR] {era_name} Level {level} Wave {wave_num}: no enemies")

                # Check for enemy types not allowed at this tier
                allowed = set(config["allowed_types"])
                if is_boss_level(level) and wave == waves[-1]:
                    allowed.add("boss")
                for enemy in wave.get("enemies", []):
                    etype = enemy.get("type", "")
                    if etype not in allowed:
                        issues.append(
                            f"[WARN] {era_name} Level {level} Wave {wave_num}: "
                            f"enemy type '{etype}' not in allowed set {allowed}"
                        )
                    if enemy.get("count", 0) < 0:
                        issues.append(
                            f"[ERROR] {era_name} Level {level} Wave {wave_num}: "
                            f"negative count for {etype}"
                        )

            # Check boss levels have a boss wave
            if is_boss_level(level):
                has_boss = any(
                    any(e.get("type") == "boss" for e in w.get("enemies", []))
                    for w in waves
                )
                if not has_boss:
                    issues.append(f"[ERROR] {era_name} Level {level}: boss level has no boss enemy")

            # Check non-boss levels don't have bosses
            if not is_boss_level(level):
                has_boss = any(
                    any(e.get("type") == "boss" for e in w.get("enemies", []))
                    for w in waves
                )
                if has_boss:
                    issues.append(f"[WARN] {era_name} Level {level}: non-boss level has boss enemy")

            # Check flying enemies only appear in late/final tiers
            tier_name = get_tier(level)
            if tier_name in ("early", "mid"):
                has_flying = any(
                    any(e.get("type") == "flying" for e in w.get("enemies", []))
                    for w in waves
                )
                if has_flying:
                    issues.append(f"[WARN] {era_name} Level {level}: flying enemies in {tier_name} tier")

    if total_levels != 200:
        issues.append(f"[ERROR] Total levels: {total_levels} (expected 200)")

    return issues


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Sakartvelo Defenders - Wave Composition Designer"
    )
    parser.add_argument(
        "--output", "-o",
        default="content/waves.json",
        help="Output JSON file path (default: content/waves.json)",
    )
    parser.add_argument(
        "--seed", "-s",
        type=int,
        default=42,
        help="Random seed for reproducible generation (default: 42)",
    )
    parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="JSON file path (positional, used for validate or as --output shorthand)",
    )
    parser.add_argument(
        "--validate", "-v",
        action="store_true",
        help="Validate an existing waves.json instead of generating",
    )
    args = parser.parse_args()

    # Positional file arg overrides --output default
    if args.file:
        args.output = args.file

    if args.validate:
        # Validate mode
        try:
            with open(args.output, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"ERROR: File not found: {args.output}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in {args.output}: {e}")
            sys.exit(1)

        issues = validate_waves(data)
        if not issues:
            print(f"Validation passed. No issues found in {args.output}")
            sys.exit(0)
        else:
            errors = [i for i in issues if "[ERROR]" in i]
            warnings = [i for i in issues if "[WARN]" in i]
            print(f"Validation complete: {len(errors)} errors, {len(warnings)} warnings")
            for issue in issues:
                print(f"  {issue}")
            sys.exit(1 if errors else 0)
    else:
        # Generation mode
        print(f"Generating wave compositions with seed={args.seed}...")
        data = generate_all_waves(seed=args.seed)

        # Count stats
        total_waves = 0
        for era in data["eras"]:
            for level in era["levels"]:
                total_waves += len(level["waves"])

        print(f"Generated {len(data['eras'])} eras, 200 levels, {total_waves} total waves")

        # Write output
        import os
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved to {args.output}")

        # Auto-validate
        issues = validate_waves(data)
        if issues:
            errors = [i for i in issues if "[ERROR]" in i]
            warnings = [i for i in issues if "[WARN]" in i]
            if errors:
                print(f"\nAuto-validation found {len(errors)} errors, {len(warnings)} warnings:")
                for issue in issues[:10]:
                    print(f"  {issue}")
                if len(issues) > 10:
                    print(f"  ... and {len(issues) - 10} more")
            else:
                print(f"Auto-validation: {len(warnings)} warnings (no errors)")
        else:
            print("Auto-validation passed.")


if __name__ == "__main__":
    main()
