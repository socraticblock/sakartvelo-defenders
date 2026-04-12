# Primitive Warrior (Era 0 Enemy) - Design Specification

## 1. OVERVIEW

**Asset Type:** Era 0 Enemy - Infantry
**Era:** Ancient Colchis (~1500 BC – 300 BC)
**Category:** Infantry (Standard 10-unit, Ground path)
**Movement:** Fast (low HP, high speed)
**Render Resolution:** 256x256 pixels (per v2.1 spec)

## 2. VISUAL DESIGN

### 2.1 Silhouette
- Humanoid figure, 10-unit proportion system
- Distinctive tribal warrior stance
- Shield/spear shape as key silhouette element
- Slightly hunched/aggressive posture (raider)

### 2.2 Body Composition

| Body Part | Geometry | Material | Color | Notes |
|-----------|----------|----------|-------|-------|
| **Head** | Slightly elongated sphere | Skin | Stone/Earth #8B7355 | Primitive, weathered appearance |
| **Hair** | Rough tuft on head | Animal fur | Shadow #1B3A26 | Messy, tribal style |
| **Torso** | Cylinder/chest | Animal skin | Shadow #1B3A26 | Fur texture visible |
| **Arms** | Cylinders | Skin/Leather mix | Stone/Earth + Shadow | Exposed lower arms |
| **Legs** | Cylinders | Leather wraps | Shadow #1B3A26 | Primitive leather strips |
| **Feet** | Simple shapes | Leather/Skin | Stone/Earth | Barefoot or simple wraps |
| **Necklace** | Torc/collar | Gold | Accent #D4A017 | Ceremonial item |
| **Wristbands** | Small bands | Gold | Accent #D4A017 | Gold jewelry |
| **Weapon** | Club/spear | Wood/Bone | Stone/Earth #8B7355 | Simple, crude weapon |
| **Shield** | Round/oval | Wood + animal hide | Stone/Earth + Shadow | Sturdy, primitive |

### 2.3 Key Design Decisions

#### ANIMAL SKIN CLOTHING (User Requirement)
- **Torso:** Covered in animal fur/skin (wolf or bear pelt)
- **Shoulders:** Fur trim visible
- **Legs:** Leather strips wrapped around lower legs
- **Appearance:** Rough, uneven texture (not smooth fur)

#### LEATHER ARMOR (Style Guide Requirement)
- **Primary Material:** Shadow color (#1B3A26) for all leather/fur
- **Texture:** Rough, primitive, worn
- **Coverage:** Torso fully covered, arms partially covered

#### GOLD JEWELRY (Style Guide Requirement)
- **Neck:** Large gold torc/necklace (Ancient Colchian style)
- **Wrists:** Simple gold bands on both wrists
- **Purpose:** Ceremonial/tribal status marker
- **Color:** Accent gold (#D4A017) - sparing use per guidelines

#### WEAPON
- **Type:** Crude wooden club or primitive spear
- **Material:** Wood (Stone/Earth #8B7355) with bone tip
- **Appearance:** Worn, handmade, not refined
- **Position:** Held in right hand, ready to strike

#### SHIELD
- **Shape:** Round or oval (Bronze Age style)
- **Material:** Wooden base covered in animal hide
- **Decoration:** Simple tribal pattern on shield face
- **Position:** Held in left hand, protective stance

## 3. COLOR MAPPING

### 3.1 Primary Colors (90% of model)
- **Shadow (#1B3A26):** Leather armor, animal fur, hair, leg wraps
- **Stone/Earth (#8B7355):** Skin, weapon, shield, feet

### 3.2 Accent Colors (10% of model)
- **Accent Gold (#D4A017):** Necklace, wristbands only (sparing use per style guide)

### 3.3 Colors NOT to Use
- ❌ Base green (#2D5A3D) - Save for player towers
- ❌ Highlight green (#4CAF50) - Save for player towers
- ❌ Vegetation blue (#3A7D44) - Not for enemies

## 4. PROPORTIONS (10-Unit System)

| Body Part | Height in Units | Notes |
|-----------|-----------------|-------|
| Head | 1.5 units | Slightly larger than normal (primitive look) |
| Torso | 2.5 units | Covered in fur |
| Arms | 3.0 units each | Exposed lower arms |
| Legs | 2.5 units each | Leather-wrapped |
| Weapon | 4.0 units | Extends upward |
| Shield | 2.0 units diameter | Round/oval |
| **Total Height** | **~8.5 units** | Within 10-unit system |

## 5. MATERIAL SPECIFICATIONS

### 5.1 Fur/Animal Skin
- **Color:** Shadow #1B3A26
- **Texture:** Rough, uneven, visible hair direction
- **Placement:** Torso, shoulders, upper arms
- **Style:** Not smooth - looks like real pelt

### 5.2 Leather Wraps
- **Color:** Shadow #1B3A26
- **Texture:** Criss-cross pattern on legs
- **Placement:** Lower legs, forearms
- **Style:** Primitive, uneven wrapping

### 5.3 Skin
- **Color:** Stone/Earth #8B7355
- **Texture:** Weathered, sun-exposed
- **Placement:** Face, hands, lower arms, feet
- **Style:** No modern smooth appearance

### 5.4 Gold
- **Color:** Accent #D4A017
- **Texture:** Muted, not shiny (bronze age gold)
- **Placement:** Neck torc, wrist bands
- **Style:** Simple, hammered, not ornate

## 6. CULTURAL/HISTORICAL ACCURACY

### 6.1 Colchian Civilization References
- **Archaeology:** Based on Vani archaeological site findings
- **Clothing:** Simple furs and leathers (Bronze Age)
- **Jewelry:** Gold torcs and bands (Colchian goldsmithing)
- **Weapons:** Crude clubs/spears (early metalworking)
- **Shields:** Wooden with hide coverings

### 6.2 Georgian Folklore
- **Tribal Appearance:** Reflects "devi" mythology influence
- **Wild Look:** Not civilized, more feral
- **Feral Nature:** Aggressive, raiding posture

### 6.3 No Caricatures
- ✅ Realistic proportions
- ✅ No exaggerated features
- ✅ Dignified representation
- ✅ Military unit, not cartoon character

## 7. TECHNICAL SPECS

### 7.1 Blender Setup
- **Template:** shared_scene_template_v2.1.blend
- **Camera:** Orthographic, X=60°, Y=0°, Z=45°
- **Lighting:** Single Sun from upper-left
- **Materials:** Flat colors (simplified for now)
- **Outlines:** Freestyle enabled, 2px, #1A1A1A

### 7.2 Model Complexity
- **Polycount:** Keep low (simple shapes)
- **Materials:** Use Era0_Shadow, Era0_Stone, Era0_Accent from template
- **Texture:** No complex textures needed (flat colors work for now)

### 7.3 Rendering
- **Resolution:** 256x256 (all sprites same size per v2.1)
- **Format:** PNG with RGBA
- **Background:** Transparent
- **Output:** `renders/enemies/enemy_e00_primitive_warrior.png`

## 8. QUALITY CHECKLIST

Before approving for render, verify:

- [ ] Animal fur/skin visible on torso (not solid color)
- [ ] Leather wraps on legs (Shadow #1B3A26)
- [ ] Gold necklace and wristbands (Accent #D4A017)
- [ ] Weapon held in right hand (Stone/Earth #8B7355)
- [ ] Shield held in left hand (Stone/Earth + Shadow)
- [ ] Only Shadow and Stone/Earth colors for body (90%)
- [ ] Only Accent gold for jewelry (10%)
- [ ] No Base or Highlight green used
- [ ] Tribal/feral posture (aggressive)
- [ ] Humanoid 10-unit proportions
- [ ] Historical/realistic appearance (no caricature)

## 9. REFERENCE IMAGES (For Future)

To gather when available:
- Colchian gold artifacts (torcs, bands)
- Bronze Age tribal warrior depictions
- Vani archaeological findings
- Animal fur/leather textures
- Primitive shield designs

## 10. NEXT STEPS

1. ✅ **Specification Approved** (awaiting user confirmation)
2. Create Blender model script based on this spec
3. Test render to verify colors and proportions
4. Refine based on feedback
5. Final render to 256x256 PNG
6. Repeat for other Era 0 enemies

---

**Created:** April 12, 2026
**Version:** 1.0
**Based On:** Art Style Guide v2.1 + Game Bible v3.0 + User Requirements
