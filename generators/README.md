# Asset Generators

This directory contains all Python scripts for generating game assets. All assets are fully regeneratable.

## Quick Start

### Generate Everything at Once
```bash
python batch_generator.py
```

### Individual Generators

#### Sprite Generation
```bash
python sprite_generator.py          # Base sprite system
```

#### Enemies
```bash
python enemy_generator.py           # Initial 5 enemies per era
python expanded_enemy_generator.py  # Full expansion + bosses
```

#### Heroes
```bash
python hero_portrait_generator.py   # Hero portraits
python full_hero_generator.py       # Complete hero system
```

#### Towers
```bash
python tower_upgrades_generator.py  # L1/L2/L3 upgrade variants
```

#### Visual Effects
```bash
python vfx_generator.py             # VFX sprite sheets
```

#### Other Assets
```bash
python scroll_generator.py          # Mastery scroll graphics
python map_generator.py             # Isometric map tiles
```

#### Content Generation
```bash
python cultural_footer.py           # Cultural facts
```

#### Tools
```bash
python prompt_generator.py          # Generate AI prompts
python consistency_checker.py       # Validate generated assets
```

## Dependencies

All generators use Python 3.11+ with:
- Pillow (PIL)
- JSON
- Standard library only (no external ML dependencies)

## Output Locations

- **Enemies**: `../assets/enemies/`
- **Heroes**: `../assets/heroes/`
- **Towers**: `../assets/towers/`
- **Maps**: `../assets/maps/`
- **Scrolls**: `../assets/scrolls/`
- **VFX**: `../assets/vfx/`

## Regenerating Specific Eras

Most generators support era-specific regeneration. Check individual scripts for details.
