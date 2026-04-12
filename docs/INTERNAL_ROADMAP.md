# Sakartvelo Defenders - Internal Execution Roadmap
*Auto-generated detailed work plan | Based on Art Style Guide v2.0*

---

## STATUS CHECK: Available Capabilities

### ✅ CONFIRMED CAN DO:
1. **Code-generated sprites** - Pillow-based pixel art engine ✓
2. **Programmatic map generation** - Layer depth, isometric terrain ✓
3. **UI HTML/CSS mockup** - Working browser prototype ✓
4. **AI Prompt Pack generation** - Production-ready prompts ✓
5. **SVG vector sprite generation** - For UI icons ✓
6. **Palette validation tools** - Hex color compliance checker ✓
7. **File organization** - Full directory structure ✓
8. **Sprite sheet generation** - Multi-sprite composites ✓

### ❌ CANNOT DO DIRECTLY:
1. **Stable Diffusion generation** - No diffusers/replicate APIs available
2. **DALL-E/Midjourney integration** - No API access
3. **High-fidelity AI art** - Requires external image generation services

### 🔶 WORKAROUND:
- Generate comprehensive AI prompts that user can paste into Stable Diffusion/DALL-E
- Provide exact prompt templates with all era-specific parameters

---

## PHASE 1: CORE FOUNDATION (In Progress)
**Target:** Complete validation assets + tooling

### 1.1 Complete Tower Generation ✅ PARTIAL
- [x] sprite_generator.py with all 10 era palettes
- [x] Tower Silhouette Sheet (Era 0)
- [x] 4 tower types (archer, catapult, wall, shrine)
- [ ] Remaining 6 tower types:
  - [ ] Cavalry tower
  - [ ] Gunpowder tower
  - [ ] Industrial tower
  - [ ] Bunker tower
  - [ ] Tech tower
  - [ ] Special tower
- [ ] Generate all towers for Era 1 (Iberia)
- [ ] Generate silhouette reference for all 10 eras

### 1.2 Era 0 Validation Assets
**Need: 1 tower, 1 enemy, 1 hero portrait, 1 map background**

#### 1.2.1 Tower (✅ DONE - Archer Tower)
- [x] twr_e00_archer_v01.png
- [x] Follows Colchis palette: #2D5A3D #4CAF50 #1B3A26 #D4A017
- [x] Cel-shaded, 2px outline, lower-right shadows

#### 1.2.2 Enemy Sprite
- [ ] Create enemy_generator.py
- [ ] Tribal Raider infantry (Era 0: Ancient Colchis)
- [ ] 10-unit proportion system (Section 5)
- [ ] Palette: Shadow #1B3A26 (armor), Accent #D4A017 (jewelry)
- [ ] Silhouette: Shield/spear shape (Section 7.1)
- [ ] Save: ene_e00_tribal_raider_infantry_v01.png
- [ ] Generate enemy silhouette reference

#### 1.2.3 Hero Portrait
- [ ] Create hero_portrait_generator.py
- [ ] Medea (Era 0 hero)
- [ ] Half-body, three-quarter view (Section 6.1)
- [ ] Background: #2D5A3D with #D4A017 radial glow
- [ ] Expression: Calm, serene (support hero)
- [ ] Era markers: Greek artifacts, gold jewelry
- [ ] Resolution: 1024x1024
- [ ] Save: her_e00_medea_v01.png

#### 1.2.4 Map Background
- [ ] Create map_generator.py
- [ ] Era 0: Colchian forest / Black Sea coast
- [ ] Three-layer depth (Section 8.1):
  - Foreground (40%): Tower placement zone
  - Midground (35%): Enemy path with river crossing
  - Background (25%): Sky #87CEEB, distant mountains
- [ ] Features: Dense forest (#3A7D44), gold mine (#8B7355), river (#2E86AB)
- [ ] Resolution: 2048x2048
- [ ] Mood: Misty, humid, golden light
- [ ] Save: map_e00_colchis_forest_coast_v01.jpg

### 1.3 Consistency Check (Section 13)
- [ ] Run palette validation on all 4 assets
- [ ] Verify silhouette compliance (90% match)
- [ ] Check rendering rules (shadow direction, outline weight)
- [ ] Document any deviations

### 1.4 UI Mockup
- [ ] Create ui_mockup.html with embedded CSS
- [ ] Global UI Palette (Section 2)
- [ ] Components:
  - [ ] HUD layout (top + bottom bars, 80% opacity)
  - [ ] Buttons (primary/secondary, hover/disabled states)
  - [ ] Panels (12px border radius, era accent strip)
  - [ ] Health bars (full/mid/low: #27AE60/#3498DB/#E74C3C)
  - [ ] Resource counters (SAKART gold, blue resources, red lives)
  - [ ] Notification toast system
  - [ ] Standard scroll card (4 rarities: gray/green/blue/purple)
  - [ ] Mastery scroll card (gold border, blockchain indicator)
- [ ] Era 0 accent strip demo
- [ ] Save: ui_mockup.html

---

## PHASE 2: AI PROMPT PACK (Era 0-1)
**Target:** All prompts needed for 40 levels (20 per era)

### 2.1 Master Prompt Template
- [ ] Document standard structure (Section 10.1)
- [ ] Create prompt_generator.py
- [ ] Function to generate prompts for any asset type + era

### 2.2 Era 0 Prompt Pack
#### 2.2.1 Tower Prompts (10 types × variants)
- [ ] Archer Tower: "isometric tower game sprite, Ancient Colchis wooden watchtower on stone foundation with thatched roof, 2D isometric cel-shaded game art, flat color fills in #2D5A3D #4CAF50 #1B3A26 #D4A017 #8B7355, 2px dark outline, clean lines, no text, isometric view, centered composition, transparent background PNG, high resolution, crisp edges, production game art"
- [ ] Catapult Tower (siege damage)
- [ ] Wall Tower (defense)
- [ ] Shrine Tower (special ability)
- [ ] Cavalry Tower (mounted units)
- [ ] Gunpowder Tower (explosive)
- [ ] Industrial Tower (area damage)
- [ ] Bunker Tower (fortified)
- [ ] Tech Tower (special effects)
- [ ] Special Tower (unique)

#### 2.2.2 Enemy Prompts (Era 0)
- [ ] Tribal Raider Infantry
- [ ] Tribal Raider Cavalry
- [ ] Greek Colonist Infantry
- [ ] Greek Colonist Archer
- [ ] Mythical Beast (Colchian guardian creature)

#### 2.2.3 Hero Portrait Prompts (Era 0)
- [ ] Medea: "Medea portrait, Ancient Colchis sorceress and healer, half-body three-quarter view, 2D isometric cel-shaded game art, #2D5A3D background with #D4A017 radial glow, Greek ceremonial robes in #D4A017 with gold jewelry, calm serene expression, bronze amulet, ancient Vani ruins in background, clean lines, 3px dark outline, flat color fills, no gradients except metallic jewelry, no text no watermark, game sprite style, high resolution 1024x1024"
- [ ] Pharnavaz: "King Pharnavaz I of Iberia portrait..."

#### 2.2.4 Map Background Prompts (Era 0 - 20 maps)
- [ ] Map 1: Colchian Forest Outpost
- [ ] Map 2: Black Sea Coastal Defense
- [ ] Map 3: River Valley Crossing
- [ ] Map 4: Ancient Gold Mine
- [ ] Map 5: Vani Ruins Defense
- [ ] Map 6: Dense Forest Ambush
- [ ] Map 7: Mountain Pass Fort
- [ ] Map 8: Coastal Bay Watchtower
- [ ] Map 9: Forest Path Convergence
- [ ] Map 10: River Delta Outpost
- [ ] Maps 11-20 (variations of above with different weather/lighting)

### 2.3 Era 1 Prompt Pack (Kingdom of Iberia)
- [ ] All tower prompts (stone fortresses, early churches)
- [ ] Enemy prompts (Roman legions, Persian forces)
- [ ] Hero portrait prompts (St. Nino, Vakhtang Gorgasali)
- [ ] Map prompts (Mtskheta, Uplistsikhe, Caucasus mountains)

### 2.4 Output
- [ ] Save: prompts_e00_towers.txt
- [ ] Save: prompts_e00_enemies.txt
- [ ] Save: prompts_e00_heroes.txt
- [ ] Save: prompts_e00_maps.txt
- [ ] Save: prompts_e01_towers.txt
- [ ] Save: prompts_e01_enemies.txt
- [ ] Save: prompts_e01_heroes.txt
- [ ] Save: prompts_e01_maps.txt

---

## PHASE 3: CODE-GENERATED ASSETS (Era 0-1)
**Target:** All sprite assets generated via Pillow/Python

### 3.1 Complete Tower Set (Era 0)
- [ ] All 10 tower types
- [ ] Variants: default, damaged, winter (optional)
- [ ] Save to assets/towers/e00_colchis/

### 3.2 Complete Tower Set (Era 1)
- [ ] All 10 tower types in Iberian stone style
- [ ] Save to assets/towers/e01_iberia/

### 3.3 Enemy Sprites (Era 0)
- [ ] Tribal Raider Infantry (walking, attacking, death frames)
- [ ] Tribal Raider Cavalry (3 frames)
- [ ] Greek Colonist Infantry (3 frames)
- [ ] Greek Colonist Archer (3 frames)
- [ ] Save to assets/enemies/e00_colchis/

### 3.4 Enemy Sprites (Era 1)
- [ ] Roman Legionary Infantry (3 frames)
- [ ] Roman Legionary Cavalry (3 frames)
- [ ] Persian Immortal Infantry (3 frames)
- [ ] Persian Archer (3 frames)
- [ ] Save to assets/enemies/e01_iberia/

### 3.5 Hero Portraits (Era 0-1)
- [ ] Medea (Era 0)
- [ ] Pharnavaz (Era 1)
- [ ] St. Nino (Era 1)
- [ ] Vakhtang Gorgasali (Era 1)
- [ ] Save to assets/heroes/e0*_*/

### 3.6 Map Backgrounds (Era 0-1)
- [ ] Generate 20 Era 0 maps (programmatic terrain, rivers, forests)
- [ ] Generate 20 Era 1 maps (mountains, cave cities, highlands)
- [ ] Save to assets/maps/e0*_*/

### 3.7 UI Icons (SVG)
- [ ] Create icon_generator.py
- [ ] Generate all tower icons (24x24 and 80x80)
- [ ] Generate resource icons (SAKART, lives, gold)
- [ ] Generate ability icons
- [ ] Save to assets/ui/icons/

---

## PHASE 4: SCROLL DESIGNS
**Target:** Standard and Mastery scroll card designs

### 4.1 Standard Scroll Cards
- [ ] Create scroll_generator.py
- [ ] 4 rarity levels (Common/Uncommon/Rare/Epic)
- [ ] Scroll types: Damage, Economy, Crowd Control, Healing, Protection
- [ ] Design elements:
  - 3:4 portrait ratio
  - Parchment background #F5E6C8
  - Top 30%: Icon (flame/coin/snowflake/heart/shield)
  - Middle 40%: Name
  - Bottom 30%: Description
  - Rarity border (3px, subtle glow)
  - Stack badge (top-right)
- [ ] Save: scr_standard_damage_common.png, scr_standard_damage_rare.png, etc.

### 4.2 Mastery Scroll Cards
- [ ] Darker parchment #D4C4A0
- [ ] Georgian cross motif overlay (5% opacity)
- [ ] Larger icon
- - Tower/hero silhouette
- [ ] Bonus percentage (3%/6%/9%)
- [ ] Blockchain verification indicator (shield icon)
- [ ] Gold border (#D4AF37)
- [ ] Pulsing glow effect (simulated in code)
- [ ] Save: scr_mastery_damage_3pct.png, etc.

---

## PHASE 5: POLISH & VALIDATION
**Target:** Ensure all assets meet Art Style Guide standards

### 5.1 Palette Compliance Tool
- [ ] Create palette_validator.py
- [ ] For each PNG: sample pixels, compare to era palette
- [ ] Report colors outside ±10 RGB tolerance
- [ ] Generate compliance report

### 5.2 Silhouette Validation
- [ ] For each sprite: convert to solid black silhouette
- [ ] Compare to reference silhouette
- [ ] Report percentage match (must be ≥90%)

### 5.3 File Naming Validation
- [ ] Scan all files in /assets/
- [ ] Verify naming convention: [category]_[era]_[type]_[variant]_[version].[ext]
- [ ] Report any violations

### 5.4 Archive System
- [ ] Create /archive/ subdirectories for each category
- [ ] Move old versions to archive when regenerating
- [ ] Maintain version history

---

## PHASE 6: DOCUMENTATION & HANDOFF
**Target:** Complete documentation for user

### 6.1 Asset Catalog
- [ ] Create ASSET_CATALOG.md
- [ ] List all generated assets with file paths
- [ ] Include preview descriptions

### 6.2 AI Prompt Catalog
- [ ] Create PROMPT_CATALOG.md
- [ ] Organize all prompts by era, category, type
- [ ] Include usage instructions

### 6.3 Status Report
- [ ] Create STATUS_REPORT.md
- [ ] What was completed
- [ ] What requires external tools (Stable Diffusion)
- [ ] Known issues/limitations
- [ ] Next steps for user

### 6.4 Setup Instructions
- [ ] How to use generated assets
- [ ] How to run AI prompts in Stable Diffusion
- [ ] How to validate new assets

---

## EXECUTION ORDER

1. **Immediate:** Complete Phase 1.1 (remaining 6 towers), 1.2.2-1.2.4 (enemy, hero, map), 1.4 (UI mockup)
2. **Then:** Phase 2 (AI Prompt Pack) - generate all prompts
3. **Then:** Phase 3 (Code-generated assets) - towers, enemies, heroes, maps for Era 0-1
4. **Then:** Phase 4 (Scroll designs)
5. **Then:** Phase 5 (Polish & validation)
6. **Finally:** Phase 6 (Documentation & handoff)

---

## TRACKING SHEET

| Phase | Task | Status | Notes |
|-------|------|--------|-------|
| 1.1 | Tower generator | 60% | 4/10 towers done |
| 1.2 | Era 0 validation | 25% | Tower done |
| 1.3 | Consistency check | 0% | Waiting for assets |
| 1.4 | UI mockup | 0% | Not started |
| 2 | AI Prompt Pack | 0% | Not started |
| 3 | Code-generated assets | 0% | Not started |
| 4 | Scroll designs | 0% | Not started |
| 5 | Polish & validation | 0% | Not started |
| 6 | Documentation | 0% | Not started |

---

**Last updated:** 2026-04-11 22:10
**Next action:** Complete remaining 6 tower types, then enemy generator
