"""
Sakartvelo Defenders Scroll Card Generator
Standard scrolls (Section 11.1) and Mastery scrolls (Section 11.2)
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Rarity colors and borders (Section 11.1)
RARITY_CONFIG = {
    "common": {
        "border_color": "#808080",
        "bg_color": "#E8DCC8",
        "text_color": "#4A4A4A",
        "name_color": "#2C1810",
        "glow": None,
    },
    "uncommon": {
        "border_color": "#27AE60",
        "bg_color": "#E8E8D0",
        "text_color": "#3A5A3A",
        "name_color": "#1B5E20",
        "glow": "#27AE60",
    },
    "rare": {
        "border_color": "#3498DB",
        "bg_color": "#D8E8F0",
        "text_color": "#2A4A6A",
        "name_color": "#1A3A5A",
        "glow": "#3498DB",
    },
    "epic": {
        "border_color": "#9B59B6",
        "bg_color": "#E8D8F0",
        "text_color": "#5A3A6A",
        "name_color": "#4A2A5A",
        "glow": "#9B59B6",
    },
}

MASTERY_CONFIG = {
    "border_color": "#D4AF37",
    "bg_color": "#D4C4A0",
    "text_color": "#5C4A2E",
    "name_color": "#3C2A1E",
    "accent": "#D4AF37",
}

# Standard Scroll Definitions (Section 11.1)
STANDARD_SCROLLS = {
    "damage": [
        {"name": "Fire Scroll", "rarity": "common", "desc": "Deal 50 DMG to all\nenemies in range", "icon": "🔥"},
        {"name": "Fire Scroll II", "rarity": "uncommon", "desc": "Deal 100 DMG to all\nenemies in range", "icon": "🔥"},
        {"name": "Inferno Scroll", "rarity": "rare", "desc": "Deal 250 DMG +\nburn for 5 seconds", "icon": "🔥"},
        {"name": "Colchian Fire", "rarity": "epic", "desc": "Ancient flame!\n500 DMG + stun 3s", "icon": "🔥"},
        {"name": "Lightning Scroll", "rarity": "uncommon", "desc": "Strike target for\n150 DMG (single)", "icon": "⚡"},
        {"name": "Thunder Storm", "rarity": "rare", "desc": "Chain lightning to\n5 enemies, 80 DMG", "icon": "⚡"},
    ],
    "utility": [
        {"name": "Gold Scroll", "rarity": "uncommon", "desc": "Gain +200 gold\ninstantly", "icon": "💰"},
        {"name": "Frost Scroll", "rarity": "uncommon", "desc": "Slow all enemies\n50% for 8 seconds", "icon": "❄"},
        {"name": "Heal Scroll", "rarity": "uncommon", "desc": "Restore 200 HP\nto all towers", "icon": "💚"},
        {"name": "Shield Scroll", "rarity": "uncommon", "desc": "All towers immune\nfor 5 seconds", "icon": "🛡"},
        {"name": "Speed Scroll", "rarity": "uncommon", "desc": "Double tower\nattack speed 10s", "icon": "💨"},
        {"name": "Vision Scroll", "rarity": "common", "desc": "Reveal all hidden\nenemies on map", "icon": "👁"},
    ],
    "special": [
        {"name": "SACART Token", "rarity": "epic", "desc": "Blockchain token!\n+500 gold + 50 SAKART", "icon": "🪙"},
        {"name": "Time Warp", "rarity": "rare", "desc": "Freeze all enemies\nfor 3 seconds", "icon": "⏳"},
        {"name": "Blessing", "rarity": "rare", "desc": "All towers +30%\nDMG for 15 seconds", "icon": "✨"},
        {"name": "Earthquake", "rarity": "epic", "desc": "Area damage 400\n+ slow 80% for 6s", "icon": "🌋"},
    ],
}

# Mastery Scroll Definitions (Section 11.2)
MASTERY_SCROLLS = [
    {"tower": "archer", "name": "Archer Mastery", "bonus": "+3%", "desc": "Archer Tower\nDMG boost"},
    {"tower": "catapult", "name": "Catapult Mastery", "bonus": "+6%", "desc": "Catapult Tower\nDMG boost"},
    {"tower": "wall", "name": "Wall Mastery", "bonus": "+5%", "desc": "Wall Tower\nHP boost"},
    {"tower": "shrine", "name": "Shrine Mastery", "bonus": "+9%", "desc": "Shrine Tower\nability boost"},
    {"tower": "cavalry", "name": "Cavalry Mastery", "bonus": "+4%", "desc": "Cavalry Tower\nspeed boost"},
    {"tower": "gunpowder", "name": "Gunpowder Mastery", "bonus": "+7%", "desc": "Gunpowder Tower\nsplash boost"},
    {"tower": "industrial", "name": "Industrial Mastery", "bonus": "+8%", "desc": "Industrial Tower\nAOE boost"},
    {"tower": "bunker", "name": "Bunker Mastery", "bonus": "+6%", "desc": "Bunker Tower\ndefense boost"},
    {"tower": "tech", "name": "Tech Mastery", "bonus": "+10%", "desc": "Tech Tower\nenergy boost"},
    {"tower": "special", "name": "Special Mastery", "bonus": "+12%", "desc": "Special Tower\nultimate boost"},
]

TOWER_SYMBOLS = {
    "archer": "🏹", "catapult": "💣", "wall": "🏰", "shrine": "⛪",
    "cavalry": "♞", "gunpowder": "🔥", "industrial": "🏭", "bunker": "🛡",
    "tech": "🔬", "special": "⭐",
}


def hex_to_rgb(hex_str: str) -> tuple:
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))


def draw_rounded_rect(draw: ImageDraw, xy, radius: int, fill=None, outline=None, width: int = 1):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = xy
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.pieslice([x1, y1, x1 + 2*radius, y1 + 2*radius], 180, 270, fill=fill)
    draw.pieslice([x2 - 2*radius, y1, x2, y1 + 2*radius], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - 2*radius, x1 + 2*radius, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - 2*radius, y2 - 2*radius, x2, y2], 0, 90, fill=fill)
    if outline:
        draw.arc([x1, y1, x1 + 2*radius, y1 + 2*radius], 180, 270, fill=outline, width=width)
        draw.arc([x2 - 2*radius, y1, x2, y1 + 2*radius], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2 - 2*radius, x1 + 2*radius, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2 - 2*radius, y2 - 2*radius, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([x1 + radius, y1, x2 - radius, y1], fill=outline, width=width)
        draw.line([x1 + radius, y2, x2 - radius, y2], fill=outline, width=width)
        draw.line([x1, y1 + radius, x1, y2 - radius], fill=outline, width=width)
        draw.line([x2, y1 + radius, x2, y2 - radius], fill=outline, width=width)


def generate_standard_scroll(scroll_data: dict, size: int = 256) -> Image.Image:
    """Generate a standard scroll card (Section 11.1)."""
    config = RARITY_CONFIG[scroll_data["rarity"]]

    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    border_rgb = hex_to_rgb(config["border_color"])
    bg_rgb = hex_to_rgb(config["bg_color"])
    name_rgb = hex_to_rgb(config["name_color"])
    text_rgb = hex_to_rgb(config["text_color"])

    card_margin = 12
    card_rect = (card_margin, card_margin, size - card_margin, size - card_margin)

    # Glow effect for uncommon+
    if config["glow"]:
        glow_rgb = hex_to_rgb(config["glow"])
        for i in range(15, 0, -3):
            alpha = int(20 * (1 - i / 15))
            glow_rect = (card_margin - i, card_margin - i,
                        size - card_margin + i, size - card_margin + i)
            draw_rounded_rect(draw, glow_rect, 12 + i,
                            fill=(*glow_rgb, alpha))

    # Card background
    draw_rounded_rect(draw, card_rect, 12, fill=(*bg_rgb, 255),
                     outline=border_rgb, width=3)

    # Parchment texture lines (subtle)
    for y in range(card_margin + 20, size - card_margin - 10, 8):
        draw.line([(card_margin + 15, y), (size - card_margin - 15, y)],
                 fill=(*text_rgb, 15), width=1)

    # Icon area (top section)
    icon_size = 56
    icon_center_x = size // 2
    icon_center_y = card_margin + 55

    # Icon background circle
    draw.ellipse([icon_center_x - icon_size//2, icon_center_y - icon_size//2,
                 icon_center_x + icon_size//2, icon_center_y + icon_size//2],
                fill=(*bg_rgb, 200), outline=(*border_rgb, 150), width=2)

    # Icon (text-based placeholder — replace with actual sprite in production)
    try:
        icon_text = scroll_data["icon"]
    except:
        icon_text = "📜"

    # Draw icon text large
    draw.text((icon_center_x - 16, icon_center_y - 16), icon_text,
             fill=text_rgb, font=None)  # Uses default font for emoji

    # Rarity indicator line
    line_y = icon_center_y + icon_size//2 + 10
    draw.line([(card_margin + 20, line_y), (size - card_margin - 20, line_y)],
             fill=(*border_rgb, 100), width=1)

    # Scroll name
    name_y = line_y + 12
    draw.text((card_margin + 20, name_y), scroll_data["name"],
             fill=name_rgb)  # Default font

    # Description text
    desc_y = name_y + 25
    for line in scroll_data["desc"].split("\n"):
        draw.text((card_margin + 20, desc_y), line, fill=text_rgb)
        desc_y += 18

    # Rarity badge (bottom right)
    rarity_text = scroll_data["rarity"].upper()
    badge_x = size - card_margin - 55
    badge_y = size - card_margin - 25
    draw_rounded_rect(draw, (badge_x, badge_y, badge_x + 45, badge_y + 18),
                     radius=4, fill=(*border_rgb, 60))
    draw.text((badge_x + 5, badge_y + 2), rarity_text, fill=(*border_rgb, 200))

    return img


def generate_mastery_scroll(scroll_data: dict, size: int = 256) -> Image.Image:
    """Generate a mastery scroll card (Section 11.2)."""
    config = MASTERY_CONFIG

    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    border_rgb = hex_to_rgb(config["border_color"])
    bg_rgb = hex_to_rgb(config["bg_color"])
    name_rgb = hex_to_rgb(config["name_color"])
    text_rgb = hex_to_rgb(config["text_color"])
    accent_rgb = hex_to_rgb(config["accent"])

    card_margin = 10
    card_rect = (card_margin, card_margin, size - card_margin, size - card_margin)

    # Golden glow
    for i in range(20, 0, -3):
        alpha = int(25 * (1 - i / 20))
        glow_rect = (card_margin - i, card_margin - i,
                    size - card_margin + i, size - card_margin + i)
        draw_rounded_rect(draw, glow_rect, 12 + i,
                        fill=(*accent_rgb, alpha))

    # Card background
    draw_rounded_rect(draw, card_rect, 12, fill=(*bg_rgb, 255),
                     outline=border_rgb, width=4)

    # Diagonal pattern overlay
    for i in range(-size, size * 2, 12):
        draw.line([(card_margin + i, card_margin),
                  (card_margin + i - size, size - card_margin)],
                 fill=(*accent_rgb, 20), width=1)

    # Shield icon (top right)
    shield_size = 22
    shield_x = size - card_margin - 30
    shield_y = card_margin + 12
    draw.polygon([
        (shield_x, shield_y),
        (shield_x + shield_size, shield_y),
        (shield_x + shield_size, shield_y + shield_size * 0.7),
        (shield_x + shield_size // 2, shield_y + shield_size),
        (shield_x, shield_y + shield_size * 0.7),
    ], fill=accent_rgb, outline=(*name_rgb, 200), width=1)
    # Shield cross
    draw.line([(shield_x + shield_size//2, shield_y + 3),
              (shield_x + shield_size//2, shield_y + shield_size - 3)],
             fill=name_rgb, width=2)
    draw.line([(shield_x + 3, shield_y + shield_size//2),
              (shield_x + shield_size - 3, shield_y + shield_size//2)],
             fill=name_rgb, width=2)

    # Tower silhouette area
    sil_size = 44
    sil_center_x = size // 2
    sil_center_y = card_margin + 52

    draw.rectangle([sil_center_x - sil_size//2, sil_center_y - sil_size//2,
                   sil_center_x + sil_size//2, sil_center_y + sil_size//2],
                  fill=(*name_rgb, 30), outline=(*accent_rgb, 100), width=2)

    # Tower symbol
    tower_sym = TOWER_SYMBOLS.get(scroll_data["tower"], "⭐")
    draw.text((sil_center_x - 14, sil_center_y - 14), tower_sym, fill=name_rgb)

    # Tower name
    name_y = sil_center_y + sil_size//2 + 15
    draw.text((card_margin + 18, name_y), scroll_data["name"], fill=name_rgb)

    # Bonus percentage (large, gold)
    bonus_y = name_y + 30
    draw.text((card_margin + 18, bonus_y), scroll_data["bonus"],
             fill=accent_rgb)

    # Description
    desc_y = bonus_y + 30
    for line in scroll_data["desc"].split("\n"):
        draw.text((card_margin + 18, desc_y), line, fill=text_rgb)
        desc_y += 16

    # Mastery badge (bottom)
    badge_y = size - card_margin - 22
    draw_rounded_rect(draw, (card_margin + 15, badge_y, size - card_margin - 15, badge_y + 16),
                     radius=4, fill=(*accent_rgb, 80))
    draw.text((card_margin + 25, badge_y + 1), "MASTERY", fill=(*name_rgb, 220))

    return img


def generate_all_scrolls():
    """Generate all scroll card assets."""
    output_dir = os.path.join(ASSETS_DIR, "scrolls")
    os.makedirs(output_dir, exist_ok=True)

    # Standard scrolls
    std_dir = os.path.join(output_dir, "standard")
    os.makedirs(std_dir, exist_ok=True)

    count = 0
    for category, scrolls in STANDARD_SCROLLS.items():
        for i, scroll in enumerate(scrolls):
            img = generate_standard_scroll(scroll, size=256)
            safe_name = scroll["name"].lower().replace(" ", "_")
            rarity = scroll["rarity"]
            filename = f"scr_standard_{safe_name}_{rarity}_v01.png"
            img.save(os.path.join(std_dir, filename))
            count += 1

    # Mastery scrolls
    mast_dir = os.path.join(output_dir, "mastery")
    os.makedirs(mast_dir, exist_ok=True)

    for scroll in MASTERY_SCROLLS:
        img = generate_mastery_scroll(scroll, size=256)
        tower = scroll["tower"]
        filename = f"scr_mastery_{tower}_v01.png"
        img.save(os.path.join(mast_dir, filename))
        count += 1

    return count


if __name__ == "__main__":
    print("Generating scroll cards...")
    total = generate_all_scrolls()
    print(f"✓ Generated {total} scroll cards")
