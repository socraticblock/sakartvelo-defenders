# Sakartvelo Defenders

A 2D isometric tower defense game through 10 eras of Georgian history, built with Godot 4.x and Immutable zkEVM blockchain integration.

## Project Structure

```
sakartvelo-defenders/
├── GODOT_PROJECT/           # Godot game project (to be created)
├── assets/                   # All game assets (PNGs, SVGs)
│   ├── enemies/             # Enemy sprites (5 per era + bosses)
│   ├── heroes/              # Hero portraits (13 total)
│   ├── towers/              # Tower sprites with upgrades (L1/L2/L3)
│   ├── maps/                # Isometric map tiles
│   ├── scrolls/             # Mastery scroll graphics
│   ├── vfx/                 # Visual effects sprite sheets
│   ├── effects/             # Additional effects
│   └── ui/                  # UI icons and elements
├── content/                  # Game content and data
│   ├── encyclopedia/        # Historical lore for each era (11 files)
│   ├── waves.json           # 200 levels, 1,211 waves, 21,174 enemies
│   ├── historical_popups.txt  # 200 educational pop-ups
│   ├── cultural_footer.txt  # 136 cultural facts (10 categories)
│   └── synergy_reference.md # Tower/enemy/hero synergies
├── generators/              # Asset generation scripts
│   ├── sprite_generator.py        # Base sprite generation
│   ├── enemy_generator.py         # Enemy sprite generation
│   ├── expanded_enemy_generator.py # Full enemy expansion
│   ├── hero_portrait_generator.py # Hero portrait generation
│   ├── full_hero_generator.py     # Complete hero system
│   ├── tower_upgrades_generator.py # Tower upgrade variants
│   ├── vfx_generator.py           # Visual effects
│   ├── scroll_generator.py        # Mastery scroll graphics
│   ├── map_generator.py           # Isometric map tiles
│   ├── prompt_generator.py        # AI prompt generation
│   ├── batch_generator.py         # Batch processing
│   ├── consistency_checker.py     # Asset validation
│   └── cultural_footer.py         # Cultural fact generation
├── tools/                   # Utility tools
│   └── wave_designer.py    # Wave configuration tool
├── docs/                    # Project documentation
│   ├── ROADMAP.md          # Public development roadmap
│   └── INTERNAL_ROADMAP.md # Detailed internal roadmap
├── web/                     # Web preview mockups
│   ├── index.html          # Main landing page
│   ├── about.html          # About page
│   ├── blockchain.html     # Blockchain integration info
│   ├── gameplay.html       # Gameplay preview
│   ├── ui_mockup.html      # UI mockups
│   └── css/                # Stylesheets
├── prompts/                 # AI generation prompts by era
└── react-build/            # React prototype (legacy)
```

## Asset Inventory

- **178 PNG files**: Heroes (13), Enemies (56), Towers (72), VFX (11), UI icons (33 SVG)
- **Content**: 200 pop-ups, 136 cultural facts, 11 encyclopedia files (~36,700 words)
- **Data**: 18,968-line waves.json with 200 levels
- **Synergies**: 35 pairs + 10 triples documented

## Getting Started

### Generate Assets
```bash
cd generators
python sprite_generator.py
python enemy_generator.py
# ... etc
```

### Regenerate All Assets
```bash
cd generators
python batch_generator.py
```

### Godot Project (Coming Soon)
The GODOT_PROJECT/ directory will contain the full Godot 4.x game project with:
- Isometric camera and tile system
- Tower placement and upgrade mechanics
- Enemy pathfinding and wave system
- Era switching mechanics
- UI implementation
- Blockchain integration (Immutable zkEVM)

## Game Features

- **10 Historical Eras**: From Ancient Colchis to Modern Georgia
- **13 Heroes**: Each with unique abilities across eras
- **72 Tower Variants**: Base towers with L1/L2/L3 upgrades
- **200 Levels**: Progressive difficulty with educational content
- **Blockchain Integration**: SAKART token, ERC-1155 skins, ERC-721 mastery scrolls
- **Educational**: Historical pop-ups and cultural facts at every level

## Development Status

- ✅ Phase 1-4: Assets and content generation complete
- 🔄 Phase 5: Godot project setup (in progress)
- ⏳ Phase 6: Core gameplay systems
- ⏳ Phase 7: UI and polish
- ⏳ Phase 8: Blockchain integration
- ⏳ Phase 9: Testing and deployment

## Contributing

This is a solo-dev project with a $100/mo budget. All assets are procedurally generated and fully regeneratable.

## License

To be determined.
