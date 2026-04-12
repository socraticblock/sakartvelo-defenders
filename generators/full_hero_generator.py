"""
Sakartvelo Defenders - Full Hero Portrait Generator
All 13 heroes from Game Design Bible v3.0
"""

from PIL import Image, ImageDraw
from sprite_generator import ERA_PALETTES, hex_to_rgb, lighten, desaturate
import os

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "heroes")

OUTLINE_COLOR = hex_to_rgb("#1A1A1A")

def hex2rgb(h):
    return hex_to_rgb(h)

def lighten_c(c, amount=30):
    r, g, b = (c if isinstance(c, tuple) else hex_to_rgb(c))
    return tuple(min(255, v + amount) for v in (r, g, b))

def darken_c(c, amount=30):
    r, g, b = (c if isinstance(c, tuple) else hex_to_rgb(c))
    return tuple(max(0, v - amount) for v in (r, g, b))

def draw_gradient_bg(draw, size, palette):
    sky = hex_to_rgb(palette.sky)
    base = hex_to_rgb(palette.base)
    accent = hex_to_rgb(palette.accent)
    for y in range(size):
        ratio = y / size
        r = int(sky[0] * (1-ratio) + base[0] * ratio)
        g = int(sky[1] * (1-ratio) + base[1] * ratio)
        b = int(sky[2] * (1-ratio) + base[2] * ratio)
        avg = (r+g+b)//3
        r, g, b = int(r*0.6+avg*0.4), int(g*0.6+avg*0.4), int(b*0.6+avg*0.4)
        draw.line([(0,y),(size,y)], fill=(r,g,b))
    # Radial accent glow
    cx, cy = size//2, size//2 - 50
    for radius in range(200, 0, -10):
        a = int((1-radius/200)*50)
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius], fill=(accent[0], accent[1], accent[2], a))


def draw_face(draw, cx, cy, palette, expression="calm", face_width=120):
    """Draw a generic face shape."""
    base_rgb = lighten_c(hex_to_rgb(palette.base), 40)
    shadow_rgb = hex_to_rgb(palette.shadow)
    
    # Head shape
    draw.ellipse([cx-face_width//2, cy-face_width//2, cx+face_width//2, cy+face_width//2],
                fill=base_rgb, outline=OUTLINE_COLOR)
    
    # Eyes
    eye_y = cy - 15
    for ex in [cx - 25, cx + 20]:
        draw.ellipse([ex-10, eye_y-6, ex+10, eye_y+6], fill=darken_c(base_rgb, 20), outline=OUTLINE_COLOR)
        draw.ellipse([ex-3, eye_y-3, ex+3, eye_y+3], fill=(30,30,30), outline=None)
    
    # Eyebrows
    brow_color = darken_c(base_rgb, 60)
    for bx in [cx-25, cx+20]:
        if expression == "determined":
            draw.line([(bx-12, eye_y-16), (bx+8, eye_y-13)], fill=brow_color, width=3)
        elif expression == "serene":
            draw.line([(bx-12, eye_y-15), (bx+8, eye_y-17)], fill=brow_color, width=3)
        else:
            draw.line([(bx-12, eye_y-14), (bx+8, eye_y-15)], fill=brow_color, width=3)
    
    # Nose
    draw.line([(cx+3, cy-5), (cx+5, cy+10)], fill=darken_c(base_rgb, 15), width=2)
    
    # Mouth
    mouth_y = cy + 25
    if expression == "serene":
        draw.arc([cx-10, mouth_y-5, cx+15, mouth_y+8], 170, 350, fill=darken_c(base_rgb, 30), width=2)
    elif expression == "determined":
        draw.line([(cx-5, mouth_y), (cx+10, mouth_y)], fill=darken_c(base_rgb, 30), width=2)
    elif expression == "thoughtful":
        draw.arc([cx-8, mouth_y-8, cx+12, mouth_y+5], 180, 330, fill=darken_c(base_rgb, 30), width=2)
    else:
        draw.line([(cx-5, mouth_y+2), (cx+10, mouth_y-2)], fill=darken_c(base_rgb, 30), width=2)
    
    return face_width


def draw_neck_and_torso(draw, cx, neck_y, palette, robe_color=None, armor_color=None):
    """Draw neck and upper torso."""
    base_rgb = lighten_c(hex_to_rgb(palette.base), 40)
    rc = robe_color or hex_to_rgb(palette.base)
    ac = armor_color or hex_to_rgb(palette.accent)
    
    # Neck
    draw.polygon([(cx-25, neck_y), (cx+20, neck_y), (cx+22, neck_y+30), (cx-23, neck_y+30)],
                fill=base_rgb, outline=OUTLINE_COLOR)
    
    # Shoulders/robe top
    sw = 140
    ty = neck_y + 30
    draw.polygon([(cx-sw//2, ty+180), (cx+sw//2, ty+180), (cx+sw//2-10, ty), (cx-sw//2+10, ty)],
                fill=rc, outline=OUTLINE_COLOR)
    
    # Robe fold lines
    fold_color = darken_c(rc, 20)
    for fx in [-40, 0, 40]:
        draw.line([(cx+fx, ty+10), (cx+fx+5, ty+160)], fill=fold_color, width=2)
    
    # Collar/neckline detail
    draw.arc([cx-30, neck_y+25, cx+25, neck_y+55], 0, 180, fill=ac, width=3)
    
    return ty


def generate_hero(hero_name, era, filename):
    """Generate a hero portrait."""
    palette = ERA_PALETTES[era]
    size = 1024
    img = Image.new('RGBA', (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    era_code = f"e{era:02d}"
    era_name = palette.name.lower().replace(" ", "_")
    out_dir = os.path.join(ASSETS_DIR, f"{era_code}_{era_name}")
    os.makedirs(out_dir, exist_ok=True)
    
    # Background
    draw_gradient_bg(draw, size, palette)
    
    cx = size // 2
    face_cy = size // 2 - 100
    
    # Hero-specific configurations
    heroes = {
        "medea": {"expression": "serene", "hair": "#1B2A1B", "headwear": "gold_headband", "accessory": "gold_amulet",
                  "robe": hex_to_rgb(palette.base), "accent_detail": "necklace"},
        "pharnavaz": {"expression": "determined", "hair": "#2C1810", "headwear": "crown",
                      "robe": darken_c(hex_to_rgb(palette.base), 20), "accent_detail": "scepter"},
        "st_nino": {"expression": "serene", "hair": "#1A1A1A", "headwear": "veil",
                    "robe": (200, 200, 220), "accent_detail": "grapevine_cross"},
        "vakhtang_gorgasali": {"expression": "determined", "hair": "#1C1008", "headwear": "helmet_wolf_pelt",
                              "robe": darken_c(hex_to_rgb(palette.base), 30), "accent_detail": "sword"},
        "david_iv": {"expression": "determined", "hair": "#1C1008", "headwear": "crown_gold",
                     "robe": (100, 30, 30), "accent_detail": "royal_banner"},
        "queen_tamar": {"expression": "thoughtful", "hair": "#1A1008", "headwear": "crown_elegant",
                        "robe": (30, 80, 30), "accent_detail": "scepter_orb"},
        "shota_rustaveli": {"expression": "thoughtful", "hair": "#1A1008", "headwear": "scholar_cap",
                            "robe": (60, 60, 100), "accent_detail": "manuscript"},
        "erekle_ii": {"expression": "determined", "hair": "#2C1810", "headwear": "crown_military",
                      "robe": (80, 40, 40), "accent_detail": "military_sash"},
        "ilia_chavchavadze": {"expression": "thoughtful", "hair": "#2C1810", "headwear": "formal_hat",
                              "robe": (40, 40, 60), "accent_detail": "chokha_elements"},
        "noe_jordania": {"expression": "determined", "hair": "#1A1008", "headwear": "none",
                         "robe": (60, 60, 60), "accent_detail": "democratic_sash"},
        "wwii_hero": {"expression": "determined", "hair": "#2C1810", "headwear": "military_helmet",
                      "robe": (60, 80, 40), "accent_detail": "medals"},
        "modern_figure": {"expression": "determined", "hair": "#1A1008", "headwear": "modern_cap",
                          "robe": (40, 60, 80), "accent_detail": "digital_display"},
        "bagrationi_prince": {"expression": "determined", "hair": "#1C1008", "headwear": "crown_simple",
                              "robe": darken_c(hex_to_rgb(palette.shadow), 10), "accent_detail": "sword_cross"},
    }
    
    hero = heroes.get(hero_name, heroes["medea"])
    
    # Hair
    hair_color = hex2rgb(hero["hair"])
    face_w = draw_face(draw, cx, face_cy, palette, hero["expression"])
    hair_points = [
        (cx - face_w//2 - 15, face_cy - face_w//2 + 10),
        (cx + face_w//2 + 10, face_cy - face_w//2 + 25),
        (cx + face_w//2 + 15, face_cy + 20),
        (cx + face_w//2 + 10, face_cy + face_w//2),
        (cx, face_cy + face_w//2 + 25),
        (cx - face_w//2, face_cy + face_w//2),
        (cx - face_w//2 - 12, face_cy + 20),
    ]
    draw.polygon(hair_points, fill=hair_color, outline=OUTLINE_COLOR)
    
    # Headwear
    accent = hex_to_rgb(palette.accent)
    hw = hero["headwear"]
    if hw == "crown" or hw == "crown_gold" or hw == "crown_elegant" or hw == "crown_military" or hw == "crown_simple":
        crown_y = face_cy - face_w//2 - 5
        crown_pts = [(cx-35, crown_y), (cx-25, crown_y-25), (cx-10, crown_y-15),
                     (cx, crown_y-30), (cx+10, crown_y-15), (cx+25, crown_y-25), (cx+35, crown_y)]
        draw.polygon(crown_pts, fill=accent, outline=OUTLINE_COLOR)
        # Gems
        for gx in [-20, 0, 20]:
            draw.ellipse([cx+gx-4, crown_y-22, cx+gx+4, crown_y-14], fill=(200,50,50), outline=OUTLINE_COLOR)
    elif hw == "gold_headband":
        draw.rectangle([cx-55, face_cy-face_w//2-5, cx+50, face_cy-face_w//2+8], fill=accent, outline=OUTLINE_COLOR)
        draw.ellipse([cx-6, face_cy-face_w//2-3, cx+6, face_cy-face_w//2+11], fill=lighten_c(accent, 40), outline=OUTLINE_COLOR)
    elif hw == "veil":
        veil_pts = [(cx-70, face_cy-face_w//2-20), (cx+60, face_cy-face_w//2-10),
                    (cx+80, face_cy+100), (cx-80, face_cy+100)]
        draw.polygon(veil_pts, fill=(200,200,220), outline=OUTLINE_COLOR)
    elif hw == "helmet_wolf_pelt":
        helmet_y = face_cy - face_w//2
        draw.ellipse([cx-50, helmet_y-20, cx+50, helmet_y+20], fill=(80,60,40), outline=OUTLINE_COLOR)
        # Wolf pelt
        draw.ellipse([cx-60, helmet_y-30, cx-20, helmet_y+10], fill=(100,80,60), outline=OUTLINE_COLOR)
        draw.ellipse([cx+20, helmet_y-30, cx+60, helmet_y+10], fill=(100,80,60), outline=OUTLINE_COLOR)
    elif hw == "scholar_cap":
        draw.polygon([(cx-50, face_cy-face_w//2), (cx+50, face_cy-face_w//2),
                     (cx+60, face_cy-face_w//2-30), (cx-60, face_cy-face_w//2-30)], fill=(80,60,100), outline=OUTLINE_COLOR)
    elif hw == "formal_hat":
        draw.rectangle([cx-45, face_cy-face_w//2-15, cx+45, face_cy-face_w//2+5], fill=(30,30,50), outline=OUTLINE_COLOR)
        draw.rectangle([cx-55, face_cy-face_w//2+2, cx+55, face_cy-face_w//2+10], fill=(30,30,50), outline=OUTLINE_COLOR)
    elif hw == "military_helmet":
        draw.ellipse([cx-55, face_cy-face_w//2-10, cx+55, face_cy-face_w//2+25], fill=(60,80,40), outline=OUTLINE_COLOR)
    elif hw == "modern_cap":
        draw.rectangle([cx-50, face_cy-face_w//2-5, cx+50, face_cy-face_w//2+10], fill=(40,50,70), outline=OUTLINE_COLOR)
        draw.rectangle([cx-35, face_cy-face_w//2-20, cx+35, face_cy-face_w//2-3], fill=(40,50,70), outline=OUTLINE_COLOR)
    
    # Neck and torso
    neck_y = face_cy + face_w//2
    torso_y = draw_neck_and_torso(draw, cx, neck_y, palette, hero["robe"], accent)
    
    # Accessory details
    ad = hero["accent_detail"]
    if ad == "gold_amulet" or ad == "grapevine_cross":
        # Necklace
        ny = neck_y + 40
        draw.arc([cx-50, ny-12, cx+50, ny+12], 0, 180, fill=accent, width=3)
        draw.polygon([(cx, ny+5), (cx+10, ny+18), (cx, ny+30), (cx-10, ny+18)], fill=accent, outline=OUTLINE_COLOR)
    elif ad == "scepter" or ad == "scepter_orb":
        # Scepter in hand
        sx = cx + 100
        sy = torso_y + 20
        draw.line([(sx, sy), (sx, sy+120)], fill=accent, width=4)
        draw.ellipse([sx-12, sy-12, sx+12, sy+12], fill=accent, outline=OUTLINE_COLOR)
    elif ad == "sword":
        # Sword
        sx = cx + 100
        sy = torso_y + 10
        draw.line([(sx, sy), (sx+5, sy+100)], fill=(180,180,200), width=4)
        draw.rectangle([sx-15, sy-5, sx+20, sy+10], fill=accent, outline=OUTLINE_COLOR)
    elif ad == "royal_banner":
        # Banner in background
        bx = cx + 120
        by = torso_y - 30
        draw.line([(bx, by), (bx, by+150)], fill=accent, width=4)
        draw.polygon([(bx, by), (bx+60, by+15), (bx+55, by+80), (bx, by+90)], fill=(180,30,30), outline=OUTLINE_COLOR)
        draw.ellipse([bx+15, by+30, bx+40, by+55], fill=accent, outline=OUTLINE_COLOR)
    elif ad == "military_sash":
        draw.line([(cx-20, neck_y+35), (cx+30, torso_y+160)], fill=accent, width=8)
    elif ad == "chokha_elements":
        # Chokha decoration
        for by in range(0, 140, 25):
            draw.ellipse([cx-60, torso_y+by, cx-45, torso_y+by+15], fill=accent, outline=OUTLINE_COLOR)
            draw.ellipse([cx+45, torso_y+by, cx+60, torso_y+by+15], fill=accent, outline=OUTLINE_COLOR)
    elif ad == "democratic_sash":
        draw.line([(cx-15, neck_y+35), (cx+25, torso_y+160)], fill=(255,255,255), width=8)
        draw.line([(cx-15, neck_y+35), (cx+25, torso_y+160)], fill=(200,30,30), width=4)
    elif ad == "medals":
        for my in range(0, 60, 25):
            draw.ellipse([cx-55, torso_y+20+my, cx-40, torso_y+35+my], fill=accent, outline=OUTLINE_COLOR)
            draw.ellipse([cx+40, torso_y+20+my, cx+55, torso_y+35+my], fill=accent, outline=OUTLINE_COLOR)
    elif ad == "digital_display":
        draw.rectangle([cx+80, torso_y+20, cx+140, torso_y+60], fill=(20,60,100), outline=(100,200,255))
        draw.line([(cx+85, torso_y+35), (cx+135, torso_y+35)], fill=(100,200,255), width=1)
        draw.line([(cx+85, torso_y+45), (cx+125, torso_y+45)], fill=(100,200,255), width=1)
    elif ad == "sword_cross":
        sx = cx + 100
        sy = torso_y + 10
        draw.line([(sx, sy), (sx+3, sy+90)], fill=(180,180,200), width=4)
        draw.rectangle([sx-12, sy-5, sx+15, sy+8], fill=accent, outline=OUTLINE_COLOR)
    elif ad == "manuscript":
        mx = cx + 90
        my = torso_y + 30
        draw.rectangle([mx, my, mx+40, my+55], fill=(220,200,160), outline=OUTLINE_COLOR)
        for ly in range(5):
            draw.line([(mx+5, my+8+ly*10), (mx+35, my+8+ly*10)], fill=(100,80,60), width=1)
    
    # Armbands with accent color
    for i in range(2):
        ay = torso_y + 50 + i*30
        for ax in [-65, 55]:
            draw.ellipse([cx+ax-10, ay-6, cx+ax+10, ay+6], fill=accent, outline=OUTLINE_COLOR)
    
    # Era marker background elements
    stone = hex_to_rgb(palette.stone_earth)
    # Ruins/pillars in background
    for px in [size-180, size-140]:
        py = size - 120
        draw.rectangle([px, py-80, px+25, py], fill=darken_c(stone, 30), outline=OUTLINE_COLOR)
        draw.ellipse([px-8, py-90, px+33, py-75], fill=darken_c(stone, 30), outline=OUTLINE_COLOR)
    
    # Save
    out_path = os.path.join(out_dir, f"her_{era_code}_{hero_name}_v01.png")
    img.save(out_path)
    return out_path


# Hero definitions matching Bible v3.0
ALL_HEROES = [
    # Era 0
    ("medea", 0),
    # Era 1
    ("pharnavaz", 1),
    ("st_nino", 1),
    ("vakhtang_gorgasali", 1),
    # Era 3
    ("david_iv", 3),
    ("queen_tamar", 3),
    ("shota_rustaveli", 3),
    # Era 5
    ("erekle_ii", 5),
    # Era 6
    ("ilia_chavchavadze", 6),
    # Era 7
    ("noe_jordania", 7),
    # Era 8
    ("wwii_hero", 8),
    # Era 9
    ("modern_figure", 9),
]

if __name__ == "__main__":
    print("Generating all hero portraits...")
    count = 0
    for hero_name, era in ALL_HEROES:
        path = generate_hero(hero_name, era, f"her_e{era:02d}_{hero_name}_v01.png")
        count += 1
        print(f"  ✓ Era {era}: {hero_name}")
    print(f"\n✓ Generated {count} hero portraits")
