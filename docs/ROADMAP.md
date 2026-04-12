# Sakartvelo Defenders — Art Production Roadmap

*Based on Art Style Guide v2.0 | Companion to Game Design Bible v3.0*

---

## Overview

Production of all visual assets for a 2D isometric cel-shaded tower defense game spanning 10 historical eras of Georgia. All assets follow strict color palettes, proportion systems, and rendering rules defined in the Art Style Guide.

**Total scope:** 200 levels across 10 eras, each requiring unique maps, tower skins, enemy types, hero portraits, UI elements, and scroll designs.

---

## Phase 1: Core Visual Foundation
**Goal:** Validate the art pipeline, produce reference assets, build tooling.
**Status:** 🔨 IN PROGRESS

### 1.1 Project Setup
- [x] Create full /assets/ directory tree (Section 12.2)
- [ ] Build sprite generation toolkit (Python/Pillow pixel art engine)
- [ ] Build SVG vector sprite generator
- [ ] Create palette validation tool (hex color checker ±10 RGB tolerance)

### 1.2 Tower Silhouette Sheet
- [ ] Generate all 10 tower type silhouettes at production quality
- [ ] Archer, Catapult, Wall, Shrine, Cavalry tower types
- [ ] Gunpowder, Industrial, Bunker, Tech, Special tower types
- [ ] Rendered in Era 0 (Ancient Colchis) skin as default
- [ ] Output: single reference sheet + individual PNGs (512x512)

### 1.3 Era 0 Palette Validation Samples
- [ ] 1 Tower (Archer Tower in Colchis palette)
- [ ] 1 Enemy (Tribal Raider infantry)
- [ ] 1 Hero Portrait (Medea)
- [ ] 1 Map Background (Colchian forest / Black Sea coast)
- [ ] Run through Consistency Checklist (Section 13)

### 1.4 UI Prototype
- [ ] HTML/CSS HUD mockup (top bar + bottom bar)
- [ ] Buttons (primary, secondary, hover, disabled states)
- [ ] Panels with era accent strips
- [ ] Health bars (full/mid/low states)
- [ ] Resource counters (SAKART gold, blue resources, red lives)
- [ ] Notification toast system
- [ ] Standard scroll card design (all 4 rarities)
- [ ] Mastery scroll card design

### 1.5 Style Guide Calibration
- [ ] Review P1 output vs style guide specs
- [ ] Adjust prompt templates if needed
- [ ] Adjust palette values if needed
- [ ] Document any deviations and fixes

---

## Phase 2: Era 0-1 Full Asset Set (Phase 1 Prototype)
**Goal:** Complete all visual assets for Eras 0-1 (40 levels).
**Status:** ⏳ PENDING

### 2.1 AI Prompt Pack
- [ ] Generate prompts for all Era 0 tower skins
- [ ] Generate prompts for all Era 0 enemy types
- [ ] Generate prompts for Era 0 hero portraits (Medea, Pharnavaz)
- [ ] Generate prompts for all 20 Era 0 map backgrounds
- [ ] Generate prompts for all Era 1 tower skins
- [ ] Generate prompts for all Era 1 enemy types
- [ ] Generate prompts for Era 1 hero portraits (St. Nino, Vakhtang Gorgasali)
- [ ] Generate prompts for all 20 Era 1 map backgrounds

### 2.2 Era 0: Ancient Colchis Assets
**Palette:** #2D5A3D #4CAF50 #1B3A26 #D4A017 #87CEEB #3A7D44 #8B7355 #2E86AB
**Mood:** Mythological, mysterious, lush
**Environment:** Dense Black Sea forests, river valleys, gold mines, ancient Vani

- [ ] Tower skins (all 10 types in Colchis wood/stone style)
- [ ] Enemy types (tribal raiders, Greek colonists, mythical beasts)
- [ ] Hero portraits: Medea, Pharnavaz
- [ ] 20 map backgrounds (forests, coast, gold mines)
- [ ] Era-specific UI accent strips

### 2.3 Era 1: Kingdom of Iberia Assets
**Palette:** #4A3728 #8D6E63 #2C1F17 #C8A96E #7FB3D8 #5D8A3C #9E8B6E #4682B4
**Mood:** Sacred, transitional, defiant
**Environment:** Mtskheta, Uplistsikhe, Caucasus mountains

- [ ] Tower skins (stone fortresses, early churches)
- [ ] Enemy types (Roman legions, Persian forces)
- [ ] Hero portraits: St. Nino, Vakhtang Gorgasali
- [ ] 20 map backgrounds (highlands, cave cities, mountain passes)
- [ ] Era-specific UI accent strips

---

## Phase 3: Era 2-4 Assets
**Goal:** Arab Invasion, Georgian Golden Age, Mongol Catastrophe.
**Status:** ⏳ PENDING

### 3.1 Era 2: Age of Invasions
**Palette:** #5C3A21 #A0522D #3B2510 #DAA520 #B8860B #6B8E23 #8B7D6B #4A708B
**Mood:** Austere, desperate, resilient

### 3.2 Era 3: Georgian Golden Age ⭐ (Most complex)
**Palette:** #1A4D2E #D4AF37 #0D2818 #C41E3A #4A90D9 #4CAF50 #B8860B #2980B9
**Mood:** Golden, triumphant, ornate

### 3.3 Era 4: Mongol Catastrophe
**Palette:** #3D2B1F #8B6914 #261A11 #CC5500 #8B4513 #556B2F #696969 #4682B4
**Mood:** Somber, devastating, defiant

---

## Phase 4: Remaining Eras & Polish
**Goal:** Eras 5-9, UI elements, scrolls, marketing.
**Status:** ⏳ PENDING

### 4.1 Era 5-9 Asset Sets
- Era 5: Between Empires (Persian/Ottoman)
- Era 6: Russian Empire
- Era 7: First Democratic Republic
- Era 8: The Soviet Century
- Era 9: Modern Georgia

### 4.2 UI & Scroll Assets
- [ ] All UI button variants
- [ ] All UI panel variants
- [ ] All icon set (tower icons, resource icons, ability icons)
- [ ] Standard scroll designs (all types, all rarities)
- [ ] Mastery scroll designs (all types)
- [ ] Loading screen art (per era)

### 4.3 Marketing & Store
- [ ] App store screenshots (per era)
- [ ] Promo art (heroic compositions)
- [ ] Feature graphics
- [ ] Social media assets

### 4.4 Final Polish
- [ ] Cross-era consistency review
- [ ] Regenerate any failed checklist items
- [ ] High-resolution marketing versions
- [ ] Archive all versions to /archive/ directories

---

## File Naming Convention

Format: `[category]_[era]_[type]_[variant]_[version].[ext]`

| Category | Code |
|----------|------|
| Tower | twr |
| Enemy | ene |
| Hero | her |
| Map | map |
| UI | ui |
| Scroll | scr |
| Effects | fxs |
| Background | bg |

| Era | Code |
|-----|------|
| Ancient Colchis | e00 |
| Kingdom of Iberia | e01 |
| Age of Invasions | e02 |
| Georgian Golden Age | e03 |
| Mongol Catastrophe | e04 |
| Between Empires | e05 |
| Russian Empire | e06 |
| First Dem. Republic | e07 |
| Soviet Century | e08 |
| Modern Georgia | e09 |

---

## Technical Specifications

| Asset Type | Resolution | Format | Outline |
|------------|-----------|--------|---------|
| Towers | 512x512 | PNG | 2px #1A1A1A |
| Enemy Sprites | 512x512 | PNG | 3px #1A1A1A |
| Hero Portraits | 1024x1024 | PNG | 3px #1A1A1A |
| Map Backgrounds | 2048x2048 | JPG | N/A |
| UI Icons | 24x24 / 80x80 | SVG | N/A |
| Scroll Cards | 3:4 portrait | PNG | 3px border |

## Rendering Rules (All Assets)
- Shadow: lower-right, 45°, desaturated base at 40% opacity
- Lighting: upper-left directional, highlight at 30% opacity
- Fills: flat color, no gradients (except metallic two-tone)
- Texture: minimal (stone 5-10% noise, wood 2-3 lines, fabric flat)
- Backgrounds: transparent PNG for sprites, JPG for maps

---

*Last updated: 2026-04-11*
*Next milestone: Phase 1 completion*
