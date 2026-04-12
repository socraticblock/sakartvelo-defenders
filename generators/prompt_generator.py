"""
Sakartvelo Defenders AI Prompt Generator
Generates production-ready prompts for Stable Diffusion / DALL-E / Midjourney
Based on Art Style Guide v2.0 Section 10
"""

from sprite_generator import ERA_PALETTES

# Master Prompt Template (Section 10.1)
# "[ASSET TYPE], [ERA KEYWORDS], [STYLE TAGS], [COMPOSITION TAGS], [TECHNICAL TAGS]"

STYLE_TAGS = "2D isometric cel-shaded game art, flat color fills, 2px dark outline (#1A1A1A), no gradients except metallic, clean lines, no text, no watermark, game sprite style, consistent lighting from upper-left"

TECHNICAL_TAGS = "high resolution, crisp edges, no JPEG artifacts, no blur, vector-quality line art, production game art"

# Era Keyword Libraries (Section 10.2)
ERA_KEYWORDS = {
    0: {
        "name": "Ancient Colchis",
        "architecture": "wooden watchtowers, stone foundations, thatched roofs, gold-panning sluices",
        "clothing": "bronze armor, leather cuirass, tribal jewelry, linen tunics",
        "environment": "dense Black Sea forests, river valleys, gold mines, ancient Vani",
        "mood": "mythological, mysterious, lush",
        "tower_style": "wooden watchtower on stone foundation with thatched roof",
        "enemy_factions": "tribal raiders, Greek colonists, mythical beasts",
        "heroes": ["Medea", "Pharnavaz"],
    },
    1: {
        "name": "Kingdom of Iberia",
        "architecture": "stone fortresses, early churches, cave cities, wooden palisades",
        "clothing": "chain mail, Roman-influenced helmets, early Christian robes, cloaks",
        "environment": "Mtskheta, Uplistsikhe, Tbilisi founding, Caucasus mountains",
        "mood": "sacred, transitional, defiant",
        "tower_style": "stone fortress with early church elements and wooden palisades",
        "enemy_factions": "Roman legions, Persian forces",
        "heroes": ["St. Nino", "Vakhtang Gorgasali"],
    },
    2: {
        "name": "Age of Invasions",
        "architecture": "siege-damaged walls, fortified monasteries, mountain redoubts",
        "clothing": "Arab desert armor, Seljuk Turk helmets, worn Georgian chain mail",
        "environment": "Tbilisi Emirate, battle-scarred countryside, mountain passes",
        "mood": "austere, desperate, resilient",
        "tower_style": "siege-damaged stone fortress with fortified monastery elements",
        "enemy_factions": "Arab forces, Seljuk Turks",
        "heroes": [],
    },
    3: {
        "name": "Georgian Golden Age",
        "architecture": "ornate stone castles, gold-domed churches, Gelati monastery, Vardzia cave city",
        "clothing": "Georgian royal armor, queen's robes, monaspa guard regalia, religious vestments",
        "environment": "prosperous towns, grand cathedrals, fertile valleys",
        "mood": "golden, triumphant, ornate",
        "tower_style": "ornate stone castle with gold cross and intricate carvings",
        "enemy_factions": "Seljuk remnants, nomadic raiders",
        "heroes": ["David IV", "Queen Tamar"],
    },
    4: {
        "name": "Mongol Catastrophe",
        "architecture": "crumbling fortresses, burned cities, mountain retreats, refugee camps",
        "clothing": "Mongol leather-lamellar armor, fur-trimmed helmets, worn Georgian armor",
        "environment": "scorched earth, smoke-filled skies, barren mountains",
        "mood": "somber, devastating, defiant",
        "tower_style": "damaged crumbling stone fortress with smoke and fire damage",
        "enemy_factions": "Mongol forces",
        "heroes": [],
    },
    5: {
        "name": "Between Empires",
        "architecture": "Persian-influenced palaces, Ottoman forts, wine country estates",
        "clothing": "gunpowder-era uniforms, Persian-style caftans, Ottoman janissary armor",
        "environment": "Kartli-Kakheti vineyards, three kingdoms, border fortresses",
        "mood": "cosmopolitan, turbulent, rich",
        "tower_style": "Persian-influenced stone palace with Ottoman fort elements",
        "enemy_factions": "Ottoman forces, Persian forces",
        "heroes": ["Erekle II"],
    },
    6: {
        "name": "Russian Empire",
        "architecture": "European-style buildings, brick factories, railway stations, theaters",
        "clothing": "Russian imperial uniforms, Georgian national dress (chokha), formal suits",
        "environment": "modernizing Tbilisi, Svaneti towers, Black Sea Batumi",
        "mood": "melancholic, transitional, cultured",
        "tower_style": "European-style brick fortress with railway-era industrial elements",
        "enemy_factions": [],
        "heroes": ["Ilia Chavchavadze"],
    },
    7: {
        "name": "First Dem. Republic",
        "architecture": "sandbag bunkers, barricaded streets, early concrete structures",
        "clothing": "WWI-era uniforms, democratic sashes, mixed civilian-military clothing",
        "environment": "war-torn countryside, Black Sea coast, Tbilisi streets",
        "mood": "hopeful, fragile, determined",
        "tower_style": "sandbag reinforced concrete bunker with democratic sash banners",
        "enemy_factions": [],
        "heroes": [],
    },
    8: {
        "name": "The Soviet Century",
        "architecture": "concrete brutalist blocks, factory complexes, Soviet monuments, panel housing",
        "clothing": "Soviet military uniforms, workers' clothing, dissident plain clothing",
        "environment": "industrial zones, Soviet Tbilisi, mountain villages",
        "mood": "oppressive, utilitarian, resilient",
        "tower_style": "brutalist concrete bunker with Soviet monument and factory elements",
        "enemy_factions": [],
        "heroes": [],
    },
    9: {
        "name": "Modern Georgia",
        "architecture": "contemporary glass buildings, military outposts, highway infrastructure",
        "clothing": "modern military gear, NATO-influenced uniforms, civilian fashion",
        "environment": "modern Tbilisi, conflict zones, Georgian Military Highway",
        "mood": "sleek, sophisticated, tense",
        "tower_style": "modern glass and steel military outpost with digital displays",
        "enemy_factions": [],
        "heroes": [],
    },
}

# Tower types with descriptions
TOWER_TYPES = {
    "archer": "archer tower with elevated shooting platform and parapets",
    "catapult": "catapult siege tower with throwing arm and stone ammunition",
    "wall": "defensive wall tower with battlements and reinforced stone",
    "shrine": "shrine tower with religious dome and cross decoration",
    "cavalry": "cavalry tower with horse stable and mounted unit deployment",
    "gunpowder": "gunpowder cannon tower with gunports and smoke effects",
    "industrial": "industrial area damage tower with smokestack and steam vents",
    "bunker": "fortified bunker tower with sandbags and machine gun position",
    "tech": "high-tech special tower with energy crystal and antenna array",
    "special": "special unique tower with ornate gold dome and decorative columns",
}

# Enemy types with descriptions
ENEMY_TYPES = {
    0: [
        ("tribal_raider_infantry", "tribal raider infantry with leather armor, bronze spear, and round shield"),
        ("tribal_raider_cavalry", "tribal raider cavalry on horseback with javelins and tribal jewelry"),
        ("greek_colonist_infantry", "Greek colonist infantry with bronze aspis shield and dory spear"),
        ("greek_colonist_archer", "Greek colonist archer with linen tunic and composite bow"),
        ("mythical_guardian", "mythical Colchian guardian beast with golden scales"),
    ],
    1: [
        ("roman_legionary_infantry", "Roman legionary infantry with rectangular scutum shield and gladius"),
        ("roman_legionary_cavalry", "Roman auxiliary cavalry with lance and oval shield"),
        ("persian_immortal_infantry", "Persian Immortal infantry with wicker shield and composite bow"),
        ("persian_archer", "Persian mounted archer with caftan and recurve bow"),
    ],
    2: [
        ("arab_warrior_infantry", "Arab desert warrior infantry with scimitar and chain mail"),
        ("seljuk_turk_cavalry", "Seljuk Turk cavalry with composite bow and lamellar armor"),
        ("georgian_guerrilla", "Georgian guerrilla fighter in worn armor defending mountain pass"),
    ],
    3: [
        ("seljuk_raider_infantry", "Seljuk raider infantry with curved sword and round shield"),
        ("nomadic_raider_cavalry", "nomadic raider cavalry on steppe horse with javelins"),
    ],
    4: [
        ("mongol_warrior_infantry", "Mongol warrior infantry with leather-lamellar armor and composite bow"),
        ("mongol_horse_archer", "Mongol horse archer with fur-trimmed helmet and quiver"),
        ("mongol_siege_engine", "Mongol siege engine operator with battering ram crew"),
        ("mongol_boss_khan", "Mongol Khan boss, 12-unit scale, ornate fur-trimmed armor with war banner"),
    ],
    5: [
        ("ottoman_janissary", "Ottoman Janissary infantry with musket and distinctive tall hat"),
        ("persian_qizilbash", "Persian Qizilbash cavalry with saber and shield"),
        ("ottoman_cannon_crew", "Ottoman cannon crew with bronze artillery piece"),
    ],
}

# Map descriptions per era
MAP_DESCRIPTIONS = {
    0: [
        ("colchis_forest_outpost", "Colchian forest outpost clearing with dense trees and wooden watchtower"),
        ("black_sea_coast", "Black Sea coastal defense with sandy beach, cliffs, and distant Greek ships"),
        ("river_valley_crossing", "river valley crossing with stone bridge and gold-panning sluices"),
        ("ancient_gold_mine", "ancient gold mine entrance in forested hillside with miners' huts"),
        ("vani_ruins_defense", "defense of ancient Vani temple ruins with broken columns"),
        ("dense_forest_ambush", "dense Colchian forest ambush path with limited visibility"),
        ("mountain_pass_fort", "Caucasus mountain pass fortress with narrow winding path"),
        ("coastal_bay_watchtower", "coastal bay watchtower overlooking turquoise harbor"),
        ("forest_path_convergence", "forest path convergence where three enemy paths meet"),
        ("river_delta_outpost", "river delta outpost at the mouth of the Rioni river"),
        ("colchis_marsh_swamp", "Colchian marsh and swamp with raised wooden walkways"),
        ("golden_fleece_shrine", "mythical Golden Fleece shrine beside a sacred grove"),
        ("village_defense", "small Colchian village defense with thatched huts and communal fire"),
        ("trading_post", "trading post on the ancient Silk Road route through Colchis"),
        ("harbor_fortress", "harbor fortress protecting Greek trading vessels"),
        ("timber_camp", "timber camp and lumberyard in deep Colchian forest"),
        ("sacred_spring", "sacred spring and healing shrine in forested mountain hollow"),
        ("border_watchtower", "border watchtower marking the edge of Colchian territory"),
        ("night_forest_raid", "nighttime forest raid under moonlight through ancient oaks"),
        ("storm_coast", "stormy coastal defense with crashing waves and lightning"),
    ],
    1: [
        ("mtskheta_approach", "approach to Mtskheta, ancient capital, with Svetitskhoveli cathedral"),
        ("uplistsikhe_cave", "Uplistsikhe cave city defense with carved stone chambers"),
        ("caucasus_mountain_fort", "Caucasus mountain fortress on narrow cliff ledge"),
        ("tbilisi_founding", "Tbilisi founding site with sulfur hot springs and wooden fortress"),
        ("roman_border_fort", "Roman border fortification along the Caucasus frontier"),
        ("persian_frontier", "Persian frontier watchtower in arid highland landscape"),
        ("early_church_defense", "defense of early Christian church with stone walls"),
        ("wine_valley", "Georgian wine valley with vineyards and hillside monastery"),
        ("mountain_shepherd_path", "mountain shepherd path through alpine meadows"),
        ("iron_mine_defense", "iron mine defense in rugged mountain terrain"),
        ("river_ferry_crossing", "river ferry crossing point on the Kura river"),
        ("royal_hunting_grounds", "royal hunting grounds with dense forest and clearings"),
        ("monastery_on_cliff", "cliffside monastery accessible only by narrow path"),
        ("stone_bridge_battle", "battle at stone bridge spanning a deep mountain gorge"),
        ("tbilisi_springs", "defense of Tbilisi's legendary sulfur springs district"),
        ("frontier_market", "frontier market town where Roman and Persian trade routes meet"),
        ("avalanche_pass", "narrow mountain pass with avalanche risk and ice walls"),
        ("pilgrim_road", "pilgrim road to sacred site with way stations"),
        ("night_siege_iberia", "nighttime siege of Iberian hilltop fortress"),
        ("golden_autumn_valley", "golden autumn valley with fallen leaves and mist"),
    ],
}

def generate_tower_prompt(tower_type: str, era: int) -> str:
    """Generate a tower prompt using Master Prompt Template."""
    palette = ERA_PALETTES[era]
    keywords = ERA_KEYWORDS[era]
    tower_desc = TOWER_TYPES[tower_type]

    prompt = (
        f"isometric tower game sprite, {keywords['name']} {tower_desc}, "
        f"{keywords['tower_style']}, {STYLE_TAGS}, "
        f"flat color fills in {palette.base} {palette.highlight} {palette.shadow} {palette.accent}, "
        f"isometric view, centered composition, transparent background PNG, {TECHNICAL_TAGS}"
    )
    return prompt

def generate_enemy_prompt(enemy_type: str, era: int, enemy_desc: str) -> str:
    """Generate an enemy prompt using Master Prompt Template."""
    palette = ERA_PALETTES[era]
    keywords = ERA_KEYWORDS[era]

    prompt = (
        f"isometric enemy game sprite, {keywords['name']} {enemy_desc}, "
        f"{STYLE_TAGS}, "
        f"flat color fills in {palette.shadow} {palette.stone_earth} {palette.accent}, "
        f"3px dark outline, no text, isometric view, action pose, transparent background PNG, {TECHNICAL_TAGS}"
    )
    return prompt

def generate_hero_prompt(hero_name: str, era: int) -> str:
    """Generate a hero portrait prompt using Section 6.2 template."""
    palette = ERA_PALETTES[era]
    keywords = ERA_KEYWORDS[era]

    # Determine role and expression based on hero
    hero_data = {
        "Medea": {"role": "sorceress and healer", "expression": "calm serene expression", "feature": "golden amulet and ceremonial robes", "marker": "ancient Vani ruins and Greek artifacts"},
        "Pharnavaz": {"role": "first king of Iberia, military commander", "expression": "determined focused expression", "feature": "crown and royal armor", "marker": "early Georgian cross symbol"},
        "St. Nino": {"role": "Christian missionary and healer", "expression": "calm serene expression", "feature": "grapevine cross necklace and simple robes", "marker": "cross symbol and early church"},
        "Vakhtang Gorgasali": {"role": "warrior king of Iberia", "expression": "determined focused expression", "feature": "crown and wolf-skin pelt on armor", "marker": "Tbilisi sulfur springs in background"},
        "David IV": {"role": "Georgian Golden Age royal military commander", "expression": "determined focused expression", "feature": "crown, royal armor in gold accents, Georgian cross on shield", "marker": "Gelati monastery and grand cathedral"},
        "Queen Tamar": {"role": "Georgian Golden Age queen ruler", "expression": "thoughtful contemplative expression", "feature": "royal robes in green and gold with crown", "marker": "gold-domed church and Georgian cross banner"},
        "Erekle II": {"role": "Georgian king and military reformer", "expression": "determined focused expression", "feature": "royal armor and chokha, crown", "marker": "Persian-influenced palace architecture"},
        "Ilia Chavchavadze": {"role": "Georgian writer and national movement leader", "expression": "thoughtful contemplative expression", "feature": "formal suit and Georgian national dress elements", "marker": "manuscript and European-style building"},
    }

    hero = hero_data.get(hero_name, hero_data["Medea"])

    prompt = (
        f"{hero_name} portrait, {keywords['name']} Georgian {hero['role']}, "
        f"half-body three-quarter view, {STYLE_TAGS}, "
        f"{palette.base} background with {palette.accent} radial glow, "
        f"{palette.base} and {palette.accent} clothing highlights, "
        f"{hero['expression']}, {hero['feature']}, {hero['marker']}, "
        f"3px dark outline, flat color fills, no gradients except metallic, "
        f"no text no watermark, game sprite style, high resolution 1024x1024"
    )
    return prompt

def generate_map_prompt(map_name: str, map_desc: str, era: int) -> str:
    """Generate a map background prompt using Master Prompt Template."""
    palette = ERA_PALETTES[era]
    keywords = ERA_KEYWORDS[era]

    prompt = (
        f"wide game map background, {keywords['name']} {map_desc}, "
        f"{STYLE_TAGS}, "
        f"{palette.sky} sky gradient to {palette.base} horizon, "
        f"{palette.vegetation} vegetation, {palette.stone_earth} stone structures, "
        f"{palette.accent} banners and accents, "
        f"{palette.water} rivers and water, "
        f"three-layer depth parallax, clear path road, no characters no text, "
        f"{keywords['mood']} atmosphere, {TECHNICAL_TAGS}"
    )
    return prompt


def generate_all_prompts() -> dict:
    """Generate the complete AI prompt pack for all eras."""
    all_prompts = {}

    for era in range(10):
        era_key = f"e{era:02d}_{ERA_KEYWORDS[era]['name'].lower().replace(' ', '_')}"
        all_prompts[era_key] = {
            "towers": {},
            "enemies": {},
            "heroes": {},
            "maps": {},
        }

        # Tower prompts
        for tower_type, tower_desc in TOWER_TYPES.items():
            prompt = generate_tower_prompt(tower_type, era)
            all_prompts[era_key]["towers"][tower_type] = prompt

        # Enemy prompts
        if era in ENEMY_TYPES:
            for enemy_id, enemy_desc in ENEMY_TYPES[era]:
                prompt = generate_enemy_prompt(enemy_id, era, enemy_desc)
                all_prompts[era_key]["enemies"][enemy_id] = prompt

        # Hero prompts
        for hero_name in ERA_KEYWORDS[era]["heroes"]:
            prompt = generate_hero_prompt(hero_name, era)
            all_prompts[era_key]["heroes"][hero_name] = prompt

        # Map prompts
        if era in MAP_DESCRIPTIONS:
            for map_id, map_desc in MAP_DESCRIPTIONS[era]:
                prompt = generate_map_prompt(map_id, map_desc, era)
                all_prompts[era_key]["maps"][map_id] = prompt

    return all_prompts


def save_prompt_pack(output_dir: str):
    """Save all prompts to organized text files."""
    all_prompts = generate_all_prompts()

    for era_key, era_prompts in all_prompts.items():
        # Save tower prompts
        tower_file = f"{output_dir}/prompts_{era_key}_towers.txt"
        with open(tower_file, 'w') as f:
            f.write(f"# Sakartvelo Defenders - Tower Prompts\n")
            f.write(f"# Era: {era_key}\n\n")
            for tower_type, prompt in era_prompts["towers"].items():
                f.write(f"## {tower_type.upper()}\n")
                f.write(f"{prompt}\n\n")

        # Save enemy prompts
        if era_prompts["enemies"]:
            enemy_file = f"{output_dir}/prompts_{era_key}_enemies.txt"
            with open(enemy_file, 'w') as f:
                f.write(f"# Sakartvelo Defenders - Enemy Prompts\n")
                f.write(f"# Era: {era_key}\n\n")
                for enemy_type, prompt in era_prompts["enemies"].items():
                    f.write(f"## {enemy_type.upper()}\n")
                    f.write(f"{prompt}\n\n")

        # Save hero prompts
        if era_prompts["heroes"]:
            hero_file = f"{output_dir}/prompts_{era_key}_heroes.txt"
            with open(hero_file, 'w') as f:
                f.write(f"# Sakartvelo Defenders - Hero Portrait Prompts\n")
                f.write(f"# Era: {era_key}\n\n")
                for hero_name, prompt in era_prompts["heroes"].items():
                    f.write(f"## {hero_name.upper()}\n")
                    f.write(f"{prompt}\n\n")

        # Save map prompts
        if era_prompts["maps"]:
            map_file = f"{output_dir}/prompts_{era_key}_maps.txt"
            with open(map_file, 'w') as f:
                f.write(f"# Sakartvelo Defenders - Map Background Prompts\n")
                f.write(f"# Era: {era_key}\n\n")
                for map_name, prompt in era_prompts["maps"].items():
                    f.write(f"## {map_name.upper()}\n")
                    f.write(f"{prompt}\n\n")

    # Count total prompts
    total = 0
    for era_key, era_prompts in all_prompts.items():
        total += len(era_prompts["towers"])
        total += len(era_prompts["enemies"])
        total += len(era_prompts["heroes"])
        total += len(era_prompts["maps"])

    return total


if __name__ == "__main__":
    output_dir = "/home/socraticblock/hermes-workspace/hermes/development/sakartvelo-defenders/prompts"
    import os
    os.makedirs(output_dir, exist_ok=True)

    total = save_prompt_pack(output_dir)
    print(f"✓ Generated {total} prompts across all 10 eras")
    print(f"  Saved to {output_dir}/")
