# Blender Assets - 3D Models for 2D Game

This directory contains all Blender 3D models and rendering pipeline for Sakartvelo Defenders.

## Workflow: 3D Models → 2D Sprites

```
1. Create 3D models in Blender (low-poly, stylized)
2. Set up isometric camera at correct angle
3. Apply cel-shaded materials
4. Render to PNG as 2D sprites
5. Import into Godot as 2D sprites
```

## Directory Structure

```
blender_assets/
├── models/              # 3D .blend files for each asset type
│   ├── base_templates/ # Reusable base models
│   ├── enemies/        # Enemy 3D models (one per era)
│   ├── heroes/         # Hero 3D models
│   └── towers/         # Tower 3D models (base + upgrades)
├── materials/          # Cel-shaded materials library
├── scenes/             # Pre-configured rendering scenes
└── renders/            # Output PNG sprites
    ├── enemies/        # Rendered enemy sprites
    ├── heroes/         # Rendered hero portraits
    ├── towers/         # Rendered tower sprites
    ├── maps/           # Rendered map tiles
    └── vfx/            # Rendered VFX sprite sheets
```

## Quick Start

### 1. Create Base Template
Open Blender and create a simple base model (e.g., a cube for tower, humanoid for enemy)
Save as `models/base_templates/tower_base.blend`

### 2. Set Up Isometric Camera
- Camera rotation: (45°, 35.264°, 0°)
- Orthographic view
- Correct aspect ratio for sprites

### 3. Apply Cel-Shaded Material
- Use toon/cel shader
- Flat shading
- Bold, clean colors

### 4. Render Sprite
- Set render settings (resolution, transparency)
- Render → Save as PNG
- Place in appropriate `renders/` subdirectory

### 5. Import to Godot
Copy from `renders/` to `../assets/` for game use

## Asset Plan

### Enemies (56 total)
- 5 enemies per era × 10 eras = 50
- 6 boss enemies = 6
- Base template: Simple humanoid with era-specific details

### Towers (72 total)
- 8 base towers
- Each tower has L1, L2, L3 upgrades
- Base template: Simple geometric structure

### Heroes (13 total)
- 1 hero per era (except some eras have multiple)
- Base template: Detailed humanoid with era armor/weapons

### Maps
- Isometric tile sets for each era
- Terrain types: grass, stone, water, path

### VFX
- Explosion, projectile, magic effects
- Sprite sheets with multiple frames

## Rendering Settings

```
Resolution: 64x64 (enemies), 128x128 (towers), 256x256 (heroes)
Format: PNG with alpha channel
Samples: 64 (for clean cel-shaded look)
Color Space: Standard
Transparent Background: Enabled
```

## Next Steps

1. ✅ Blender installed
2. ⏳ Create base templates
3. ⏳ Build enemy models
4. ⏳ Build tower models
5. ⏳ Build hero models
6. ⏳ Set up rendering pipeline
7. ⏳ Generate all sprites
8. ⏳ Replace existing 2D assets with Blender renders

## Resources

- Blender manual: https://docs.blender.org/
- Cel-shading tutorial: https://www.youtube.com/watch?v=...
- Isometric camera setup: https://docs.blender.org/manual/en/...
