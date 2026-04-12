"""
Sakartvelo Defenders - Expanded Enemy Generator
Generates 50 enemy sprites across all 10 eras (Eras 0-9).
Each era: 4 regular types (infantry, cavalry, siege, flying) + 1 boss.
Sprite size: 256x256, 2D isometric-ish perspective.
"""

from PIL import Image, ImageDraw
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sprite_generator import ERA_PALETTES, hex_to_rgb, lighten, desaturate, EraPalette

# ==========================================
# CONSTANTS
# ==========================================

SIZE = 256
OUTLINE_COLOR = hex_to_rgb("#1A1A1A")
OUTLINE_W = 2
UNIT = 24  # proportion unit at 256px resolution

THREAT_COLORS = {
    "infantry": "#27AE60",   # green - low threat
    "cavalry": "#F1C40F",    # yellow - medium threat
    "siege": "#E74C3C",      # red - high threat
    "flying": "#1ABC9C",     # teal - aerial
    "boss": "#9B59B6",       # purple - boss
}

ERA_DEFS = {
    0: {
        "folder": "e00_ancient_colchis",
        "enemies": {
            "infantry": ("tribal_warrior", "Tribal Warrior"),
            "cavalry": ("mounted_raider", "Mounted Raider"),
            "siege": ("stone_thrower", "Stone Thrower"),
            "flying": ("devi", "Devi"),
            "boss": ("colchian_dragon", "Colchian Dragon"),
        },
    },
    1: {
        "folder": "e01_kingdom_of_iberia",
        "enemies": {
            "infantry": ("iberian_infantry", "Iberian Infantry"),
            "cavalry": ("parthian_cavalry", "Parthian Cavalry"),
            "siege": ("roman_siege_engine", "Roman Siege Engine"),
            "flying": ("war_eagle", "War Eagle"),
            "boss": ("sassanid_war_elephant", "Sassanid War Elephant"),
        },
    },
    2: {
        "folder": "e02_age_of_invasions",
        "enemies": {
            "infantry": ("arab_warrior", "Arab Warrior"),
            "cavalry": ("arab_horse_archer", "Arab Horse Archer"),
            "siege": ("siege_ladder", "Siege Ladder"),
            "flying": ("desert_hawk", "Desert Hawk"),
            "boss": ("arab_emir_tbilisi", "Arab Emir of Tbilisi"),
        },
    },
    3: {
        "folder": "e03_georgian_golden_age",
        "enemies": {
            "infantry": ("seljuk_infantry", "Seljuk Infantry"),
            "cavalry": ("turkmen_cavalry", "Turkmen Cavalry"),
            "siege": ("siege_ram", "Siege Ram"),
            "flying": ("falcon", "Falcon"),
            "boss": ("atabeg_azerbaijan", "Atabeg of Azerbaijan"),
        },
    },
    4: {
        "folder": "e04_mongol_catastrophe",
        "enemies": {
            "infantry": ("mongol_warrior", "Mongol Warrior"),
            "cavalry": ("mongol_horse_archer", "Mongol Horse Archer"),
            "siege": ("siege_tower", "Siege Tower"),
            "flying": ("mongol_signal_arrow", "Mongol Signal Arrow"),
            "boss": ("general_subutai_proxy", "General Subutai's Proxy"),
        },
    },
    5: {
        "folder": "e05_between_empires",
        "enemies": {
            "infantry": ("ottoman_janissary", "Ottoman Janissary"),
            "cavalry": ("persian_cavalry", "Persian Cavalry"),
            "siege": ("ottoman_cannon", "Ottoman Cannon"),
            "flying": ("messenger_pigeon", "Messenger Pigeon"),
            "boss": ("agha_mohammad_khan", "Agha Mohammad Khan"),
        },
    },
    6: {
        "folder": "e06_russian_empire",
        "enemies": {
            "infantry": ("russian_infantry", "Russian Infantry"),
            "cavalry": ("cossack_cavalry", "Cossack Cavalry"),
            "siege": ("artillery_piece", "Artillery Piece"),
            "flying": ("observation_balloon", "Observation Balloon"),
            "boss": ("imperial_general", "Imperial General"),
        },
    },
    7: {
        "folder": "e07_first_republic",
        "enemies": {
            "infantry": ("bolshevik_infantry", "Bolshevik Infantry"),
            "cavalry": ("armored_car", "Armored Car"),
            "siege": ("field_gun", "Field Gun"),
            "flying": ("reconnaissance_plane", "Reconnaissance Plane"),
            "boss": ("red_army_commissar", "Red Army Commissar"),
        },
    },
    8: {
        "folder": "e08_soviet_century",
        "enemies": {
            "infantry": ("soviet_conscript", "Soviet Conscript"),
            "cavalry": ("soviet_tank", "Soviet Tank"),
            "siege": ("katyusha_launcher", "Katyusha Launcher"),
            "flying": ("mig_jet", "MiG Jet"),
            "boss": ("soviet_general", "Soviet General"),
        },
    },
    9: {
        "folder": "e09_modern_georgia",
        "enemies": {
            "infantry": ("irregular_militia", "Irregular Militia"),
            "cavalry": ("technical_truck", "Technical Truck"),
            "siege": ("mortar_team", "Mortar Team"),
            "flying": ("surveillance_drone", "Surveillance Drone"),
            "boss": ("warlord_commander", "Warlord Commander"),
        },
    },
}

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "enemies")


# ==========================================
# DRAWING PRIMITIVES
# ==========================================

def new_canvas():
    """Create a new transparent 256x256 canvas."""
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def draw_health_bar(draw):
    """Draw empty health bar outline at bottom of sprite."""
    bx1, bx2 = 24, SIZE - 24
    by1, by2 = SIZE - 18, SIZE - 10
    draw.rectangle([bx1, by1, bx2, by2], outline=OUTLINE_COLOR, width=OUTLINE_W)


def draw_threat_badge(draw, category):
    """Draw threat color indicator diamond in top-right corner."""
    color = hex_to_rgb(THREAT_COLORS[category])
    cx, cy = SIZE - 18, 18
    pts = [(cx, cy - 8), (cx + 8, cy), (cx, cy + 8), (cx - 8, cy)]
    draw.polygon(pts, fill=color, outline=OUTLINE_COLOR)


def draw_ground_shadow(draw, cx, cy, w=36, h=10):
    """Draw a ground shadow ellipse."""
    draw.ellipse([cx - w, cy - h // 2, cx + w, cy + h // 2], fill=(0, 0, 0, 50))


def poly(draw, points, fill, outline=None):
    """Draw a polygon with outline."""
    draw.polygon(points, fill=fill, outline=outline or OUTLINE_COLOR)


def ellipse(draw, bbox, fill, outline=None):
    """Draw an ellipse with outline."""
    draw.ellipse(bbox, fill=fill, outline=outline or OUTLINE_COLOR)


def rect(draw, bbox, fill, outline=None):
    """Draw a rectangle with outline."""
    draw.rectangle(bbox, fill=fill, outline=outline or OUTLINE_COLOR)


def line(draw, p1, p2, fill, width=3):
    """Draw a line."""
    draw.line([p1, p2], fill=fill, width=width)


def darken(color, amount=0.35):
    """Darken a hex color."""
    r, g, b = hex_to_rgb(color)
    return "#{:02x}{:02x}{:02x}".format(
        max(0, int(r * (1 - amount))),
        max(0, int(g * (1 - amount))),
        max(0, int(b * (1 - amount))),
    )


def tint(color, target, amount=0.3):
    """Tint a hex color toward a target."""
    r, g, b = hex_to_rgb(color)
    tr, tg, tb = hex_to_rgb(target)
    return "#{:02x}{:02x}{:02x}".format(
        int(r * (1 - amount) + tr * amount),
        int(g * (1 - amount) + tg * amount),
        int(b * (1 - amount) + tb * amount),
    )


# ==========================================
# HUMANOID BASE
# ==========================================

def draw_humanoid(draw, cx, base_y, pal: EraPalette,
                  body_color=None, armor_color=None,
                  head_detail=None, weapon=None, shield=None,
                  scale=1.0):
    """
    Draw a humanoid figure facing slightly right (isometric-ish).
    10-unit proportion system scaled for 256px.
    """
    s = scale
    u = UNIT * s

    bc = hex_to_rgb(body_color or pal.shadow)
    ac = hex_to_rgb(armor_color or pal.shadow)
    hc = hex_to_rgb(lighten(pal.shadow))
    accent = hex_to_rgb(pal.accent)

    feet_y = base_y
    hip_y = int(base_y - 2.5 * u)
    shoulder_y = int(hip_y - 2.5 * u)
    head_bot_y = shoulder_y
    head_top_y = int(head_bot_y - 1.8 * u)

    # Legs (striding, slightly right-facing)
    back_leg = [
        (cx - int(8 * s), hip_y),
        (cx - int(14 * s), int(hip_y - 1.2 * u)),
        (cx - int(18 * s), feet_y),
        (cx - int(4 * s), feet_y),
        (cx - int(2 * s), hip_y),
    ]
    poly(draw, back_leg, darken(body_color or pal.shadow), OUTLINE_COLOR)

    front_leg = [
        (cx + int(2 * s), hip_y),
        (cx + int(12 * s), int(hip_y - 1.2 * u)),
        (cx + int(18 * s), feet_y),
        (cx + int(4 * s), feet_y),
        (cx - int(2 * s), hip_y),
    ]
    poly(draw, front_leg, hex_to_rgb(lighten(body_color or pal.shadow)), OUTLINE_COLOR)

    # Torso
    tw = int(1.2 * u)
    torso = [
        (cx - tw, hip_y),
        (cx + tw, hip_y),
        (cx + tw - int(4 * s), shoulder_y),
        (cx - tw + int(4 * s), shoulder_y),
    ]
    poly(draw, torso, bc, OUTLINE_COLOR)

    # Back arm
    back_arm = [
        (cx - tw + int(4 * s), shoulder_y),
        (cx - tw - int(8 * s), int(shoulder_y + 0.8 * u)),
        (cx - tw - int(4 * s), int(shoulder_y + 1.8 * u)),
        (cx - tw + int(4 * s), int(shoulder_y + 1.8 * u)),
    ]
    poly(draw, back_arm, darken(body_color or pal.shadow), OUTLINE_COLOR)

    # Front arm
    front_arm = [
        (cx + tw - int(4 * s), shoulder_y),
        (cx + tw + int(8 * s), int(shoulder_y + 0.8 * u)),
        (cx + tw + int(10 * s), int(shoulder_y + 1.8 * u)),
        (cx + tw + int(2 * s), int(shoulder_y + 1.8 * u)),
    ]
    poly(draw, front_arm, hex_to_rgb(lighten(body_color or pal.shadow)), OUTLINE_COLOR)

    # Head
    hw = int(0.9 * u)
    head_rect = [cx - hw, head_top_y, cx + hw, head_bot_y]
    ellipse(draw, head_rect, hc, OUTLINE_COLOR)

    # Head detail (helmet, hat, turban, etc.)
    if head_detail == "helmet_simple":
        hr = [cx - hw - 2, head_top_y - int(6 * s), cx + hw + 2, head_top_y + int(10 * s)]
        ellipse(draw, hr, ac, OUTLINE_COLOR)
    elif head_detail == "helmet_crest":
        hr = [cx - hw - 2, head_top_y - int(6 * s), cx + hw + 2, head_top_y + int(10 * s)]
        ellipse(draw, hr, ac, OUTLINE_COLOR)
        # Crest
        crest_pts = [(cx, head_top_y - int(6 * s) - int(10 * s)),
                     (cx + int(6 * s), head_top_y - int(4 * s)),
                     (cx - int(6 * s), head_top_y - int(4 * s))]
        poly(draw, crest_pts, accent, OUTLINE_COLOR)
    elif head_detail == "turban":
        tr = [cx - hw - int(4 * s), head_top_y - int(8 * s), cx + hw + int(4 * s), head_top_y + int(6 * s)]
        ellipse(draw, tr, hex_to_rgb(pal.accent), OUTLINE_COLOR)
        # Tail
        pts = [(cx - hw - int(4 * s), head_top_y),
               (cx - hw - int(12 * s), head_top_y + int(10 * s)),
               (cx - hw - int(4 * s), head_top_y + int(6 * s))]
        poly(draw, pts, hex_to_rgb(pal.accent), OUTLINE_COLOR)
    elif head_detail == "mongol_helmet":
        hr = [cx - hw - 2, head_top_y - int(6 * s), cx + hw + 2, head_top_y + int(10 * s)]
        ellipse(draw, hr, ac, OUTLINE_COLOR)
        # Top spike
        line(draw, (cx, head_top_y - int(6 * s)), (cx, head_top_y - int(16 * s)), ac, int(3 * s))
    elif head_detail == "janissary_hat":
        # Tall cylindrical hat
        hat_w = int(hw * 0.8)
        rect(draw, [cx - hat_w, head_top_y - int(18 * s), cx + hat_w, head_top_y + int(2 * s)],
             hex_to_rgb(pal.accent), OUTLINE_COLOR)
    elif head_detail == "fur_hat":
        hr = [cx - hw - int(6 * s), head_top_y - int(10 * s), cx + hw + int(6 * s), head_top_y + int(8 * s)]
        ellipse(draw, hr, hex_to_rgb(pal.vegetation), OUTLINE_COLOR)
    elif head_detail == "greatcoat_hat":
        # Military cap / peaked cap
        cap_pts = [
            (cx - hw, head_top_y),
            (cx + hw + int(8 * s), head_top_y + int(4 * s)),
            (cx + hw, head_top_y + int(6 * s)),
            (cx - hw, head_top_y + int(6 * s)),
        ]
        poly(draw, cap_pts, hex_to_rgb(darken(pal.base, 0.2)), OUTLINE_COLOR)
    elif head_detail == "leather_cap":
        hr = [cx - hw - 1, head_top_y - int(4 * s), cx + hw + 1, head_top_y + int(8 * s)]
        ellipse(draw, hr, hex_to_rgb(pal.stone_earth), OUTLINE_COLOR)
    elif head_detail == "military_cap":
        cap_pts = [
            (cx - hw - int(2 * s), head_top_y + int(2 * s)),
            (cx + hw + int(4 * s), head_top_y + int(4 * s)),
            (cx + hw + int(2 * s), head_top_y + int(6 * s)),
            (cx - hw - int(4 * s), head_top_y + int(6 * s)),
        ]
        poly(draw, cap_pts, hex_to_rgb(pal.base), OUTLINE_COLOR)
        # Star/insignia
        star_cx = cx
        star_cy = head_top_y + int(4 * s)
        draw.ellipse([star_cx - 3, star_cy - 3, star_cx + 3, star_cy + 3],
                     fill=accent, outline=OUTLINE_COLOR)
    elif head_detail == "modern_helmet":
        hr = [cx - hw - int(2 * s), head_top_y - int(6 * s), cx + hw + int(2 * s), head_top_y + int(8 * s)]
        ellipse(draw, hr, hex_to_rgb(darken(pal.base, 0.3)), OUTLINE_COLOR)
        # NVG bump
        rect(draw, [cx - int(4 * s), head_top_y - int(4 * s), cx + int(4 * s), head_top_y],
             hex_to_rgb(darken(pal.base, 0.5)))
    elif head_detail == "crown":
        # Crown / royal headpiece
        crown_base = [cx - hw, head_top_y - int(2 * s), cx + hw, head_top_y + int(4 * s)]
        rect(draw, crown_base, accent, OUTLINE_COLOR)
        for i in range(3):
            px = cx - int(6 * s) + i * int(6 * s)
            pts = [(px - int(3 * s), head_top_y - int(2 * s)),
                   (px, head_top_y - int(10 * s)),
                   (px + int(3 * s), head_top_y - int(2 * s))]
            poly(draw, pts, accent, OUTLINE_COLOR)
    elif head_detail == "horns":
        # Demon horns (for devi)
        for side in [-1, 1]:
            horn_base_x = cx + side * hw
            pts = [
                (horn_base_x, head_top_y + int(4 * s)),
                (horn_base_x + side * int(12 * s), head_top_y - int(14 * s)),
                (horn_base_x + side * int(6 * s), head_top_y),
            ]
            poly(draw, pts, hex_to_rgb("#8B0000"), OUTLINE_COLOR)

    # Weapon
    if weapon == "spear":
        sx, sy = cx - tw - int(8 * s), int(shoulder_y + 0.8 * u)
        ex, ey = sx - int(20 * s), sy + int(30 * s)
        line(draw, (sx, sy), (ex, ey), hex_to_rgb(pal.stone_earth), int(3 * s))
        # Spearhead
        poly(draw, [(ex, ey), (ex - int(12 * s), ey - int(4 * s)), (ex - int(12 * s), ey + int(4 * s))],
             accent, OUTLINE_COLOR)
    elif weapon == "sword":
        sx, sy = cx + tw + int(8 * s), int(shoulder_y + 1.0 * u)
        line(draw, (sx, sy), (sx + int(18 * s), sy + int(22 * s)), accent, int(3 * s))
        # Hilt
        line(draw, (sx - int(5 * s), sy + int(2 * s)), (sx + int(5 * s), sy + int(2 * s)),
             hex_to_rgb(pal.stone_earth), int(2 * s))
    elif weapon == "scimitar":
        sx, sy = cx + tw + int(8 * s), int(shoulder_y + 1.0 * u)
        # Curved blade
        pts = [
            (sx, sy),
            (sx + int(22 * s), sy + int(16 * s)),
            (sx + int(18 * s), sy + int(26 * s)),
            (sx + int(4 * s), sy + int(8 * s)),
        ]
        poly(draw, pts, accent, OUTLINE_COLOR)
    elif weapon == "bow":
        bx, by = cx - tw - int(12 * s), int(shoulder_y + 0.4 * u)
        draw.arc([bx - int(10 * s), by - int(16 * s), bx + int(10 * s), by + int(16 * s)],
                 30, 330, fill=hex_to_rgb(pal.stone_earth), width=int(2 * s))
        # String
        line(draw, (bx, by - int(14 * s)), (bx, by + int(14 * s)),
             hex_to_rgb(pal.shadow), int(1 * s))
    elif weapon == "musket":
        mx, my = cx + tw + int(4 * s), int(shoulder_y + 0.6 * u)
        line(draw, (mx, my), (mx + int(24 * s), my + int(6 * s)),
             hex_to_rgb(pal.stone_earth), int(3 * s))
        # Stock
        line(draw, (mx - int(8 * s), my + int(2 * s)), (mx + int(4 * s), my),
             hex_to_rgb(pal.stone_earth), int(4 * s))
    elif weapon == "rifle":
        rx, ry = cx + tw + int(4 * s), int(shoulder_y + 0.6 * u)
        line(draw, (rx, ry), (rx + int(28 * s), ry + int(4 * s)),
             hex_to_rgb(darken(pal.stone_earth, 0.4)), int(2 * s))
    elif weapon == "axe":
        ax, ay = cx + tw + int(10 * s), int(shoulder_y + 1.2 * u)
        line(draw, (ax, ay), (ax + int(4 * s), ay + int(20 * s)),
             hex_to_rgb(pal.stone_earth), int(3 * s))
        # Axe head
        poly(draw, [(ax + int(4 * s), ay + int(14 * s)),
                    (ax + int(14 * s), ay + int(10 * s)),
                    (ax + int(14 * s), ay + int(20 * s))],
             accent, OUTLINE_COLOR)
    elif weapon == "pike":
        sx, sy = cx - tw - int(8 * s), int(shoulder_y + 0.6 * u)
        ex, ey = sx - int(10 * s), sy + int(34 * s)
        line(draw, (sx, sy), (ex, ey), hex_to_rgb(pal.stone_earth), int(2 * s))
        poly(draw, [(ex, ey), (ex - int(10 * s), ey - int(3 * s)), (ex - int(10 * s), ey + int(3 * s))],
             accent, OUTLINE_COLOR)

    # Shield
    if shield == "round":
        sx, sy = cx + tw + int(10 * s), int(shoulder_y + 1.2 * u)
        r = int(12 * s)
        ellipse(draw, [sx - r, sy - r, sx + r, sy + r], ac, OUTLINE_COLOR)
        ellipse(draw, [sx - int(5 * s), sy - int(5 * s), sx + int(5 * s), sy + int(5 * s)],
                accent, OUTLINE_COLOR)
    elif shield == "rectangular":
        sx, sy = cx + tw + int(10 * s), int(shoulder_y + 0.8 * u)
        sw, sh = int(10 * s), int(16 * s)
        rect(draw, [sx, sy - sh // 2, sx + sw, sy + sh // 2], ac, OUTLINE_COLOR)
        rect(draw, [sx + sw // 2 - 1, sy - sh // 2 + 2, sx + sw // 2 + 1, sy + sh // 2 - 2],
             accent, None)
    elif shield == "kite":
        sx, sy = cx + tw + int(10 * s), int(shoulder_y + 0.6 * u)
        pts = [(sx, sy - int(14 * s)), (sx + int(10 * s), sy - int(4 * s)),
               (sx + int(8 * s), sy + int(14 * s)), (sx, sy + int(16 * s)),
               (sx - int(4 * s), sy + int(4 * s))]
        poly(draw, pts, ac, OUTLINE_COLOR)


# ==========================================
# HORSE / MOUNT BASE
# ==========================================

def draw_horse(draw, cx, base_y, pal: EraPalette, scale=1.0):
    """Draw a horse facing slightly right."""
    s = scale
    body_c = hex_to_rgb(pal.shadow)
    dark_c = hex_to_rgb(darken(pal.shadow, 0.25))
    light_c = hex_to_rgb(lighten(pal.shadow))

    by = base_y
    # Body
    body_pts = [
        (cx - int(24 * s), by - int(20 * s)),
        (cx + int(24 * s), by - int(22 * s)),
        (cx + int(28 * s), by - int(14 * s)),
        (cx + int(20 * s), by - int(8 * s)),
        (cx - int(20 * s), by - int(6 * s)),
    ]
    poly(draw, body_pts, body_c, OUTLINE_COLOR)

    # Neck
    neck_pts = [
        (cx + int(20 * s), by - int(22 * s)),
        (cx + int(30 * s), by - int(36 * s)),
        (cx + int(36 * s), by - int(34 * s)),
        (cx + int(28 * s), by - int(18 * s)),
    ]
    poly(draw, neck_pts, light_c, OUTLINE_COLOR)

    # Head
    head_pts = [
        (cx + int(30 * s), by - int(36 * s)),
        (cx + int(44 * s), by - int(34 * s)),
        (cx + int(42 * s), by - int(30 * s)),
        (cx + int(36 * s), by - int(34 * s)),
    ]
    poly(draw, head_pts, light_c, OUTLINE_COLOR)

    # Ear
    poly(draw, [(cx + int(34 * s), by - int(36 * s)),
                (cx + int(36 * s), by - int(42 * s)),
                (cx + int(38 * s), by - int(36 * s))],
         light_c, OUTLINE_COLOR)

    # Legs
    for lx_off, lean in [(-16, -2), (-6, 2), (10, -2), (20, 2)]:
        leg_top = (cx + int(lx_off * s), by - int(8 * s))
        leg_bot = (cx + int((lx_off + lean) * s), by)
        line(draw, leg_top, leg_bot, dark_c, int(4 * s))

    # Tail
    pts = [(cx - int(24 * s), by - int(18 * s)),
           (cx - int(34 * s), by - int(12 * s)),
           (cx - int(30 * s), by - int(8 * s)),
           (cx - int(22 * s), by - int(10 * s))]
    poly(draw, pts, dark_c, OUTLINE_COLOR)

    # Mane
    for i in range(3):
        my = by - int((24 + i * 4) * s)
        mx = cx + int((22 + i * 3) * s)
        line(draw, (mx, my), (mx + int(4 * s), my - int(4 * s)), dark_c, int(2 * s))

    return by - int(22 * s)  # Return rider base Y


def draw_saddle(draw, cx, base_y, pal: EraPalette, scale=1.0):
    """Draw a saddle on the horse."""
    s = scale
    sy = base_y - int(22 * s)
    sw, sh = int(14 * s), int(4 * s)
    rect(draw, [cx - sw, sy - sh, cx + sw, sy + sh],
         hex_to_rgb(pal.accent), OUTLINE_COLOR)
    return sy - sh


# ==========================================
# WHEELED BASE (for siege units)
# ==========================================

def draw_wheels(draw, cx, base_y, pal: EraPalette, wheel_count=2, spacing=30, scale=1.0):
    """Draw wheels at the bottom of a siege unit."""
    s = scale
    wy = base_y - int(8 * s)
    r = int(10 * s)
    wheel_positions = []
    for i in range(wheel_count):
        wx = cx + int((i - (wheel_count - 1) / 2) * spacing * s)
        ellipse(draw, [wx - r, wy - r, wx + r, wy + r],
                hex_to_rgb(darken(pal.stone_earth, 0.3)), OUTLINE_COLOR)
        # Hub
        ellipse(draw, [wx - int(3 * s), wy - int(3 * s), wx + int(3 * s), wy + int(3 * s)],
                hex_to_rgb(pal.stone_earth), OUTLINE_COLOR)
        # Spokes
        for angle in range(0, 360, 90):
            import math
            ex = wx + int(r * 0.7 * math.cos(math.radians(angle)))
            ey = wy + int(r * 0.7 * math.sin(math.radians(angle)))
            line(draw, (wx, wy), (ex, ey), hex_to_rgb(pal.stone_earth), max(1, int(s)))
        wheel_positions.append((wx, wy))
    return wy - r  # Return top of wheel area


# ==========================================
# WING BASE (for flying units)
# ==========================================

def draw_wings(draw, cx, cy, pal: EraPalette, wing_span=50, wing_height=16, scale=1.0):
    """Draw outstretched wings."""
    s = scale
    ws = int(wing_span * s)
    wh = int(wing_height * s)
    wing_c = hex_to_rgb(tint(pal.shadow, pal.sky, 0.3))
    wing_dark = hex_to_rgb(darken(pal.shadow, 0.2))

    # Left wing
    lw_pts = [
        (cx - int(4 * s), cy),
        (cx - ws, cy - wh),
        (cx - ws + int(8 * s), cy + int(4 * s)),
        (cx - int(4 * s), cy + int(6 * s)),
    ]
    poly(draw, lw_pts, wing_c, OUTLINE_COLOR)

    # Right wing
    rw_pts = [
        (cx + int(4 * s), cy),
        (cx + ws, cy - wh),
        (cx + ws - int(8 * s), cy + int(4 * s)),
        (cx + int(4 * s), cy + int(6 * s)),
    ]
    poly(draw, rw_pts, wing_dark, OUTLINE_COLOR)

    # Wing feather lines
    for i in range(3):
        frac = (i + 1) / 4
        lx = cx - int(4 * s) - int(ws * frac * 0.8)
        rx = cx + int(4 * s) + int(ws * frac * 0.8)
        ly = cy - int(wh * frac * 0.7)
        ry = cy - int(wh * frac * 0.7)
        line(draw, (cx - int(4 * s), cy), (lx, ly), wing_dark, max(1, int(s)))
        line(draw, (cx + int(4 * s), cy), (rx, ry), hex_to_rgb(lighten(pal.shadow)), max(1, int(s)))


def draw_bat_wings(draw, cx, cy, scale=1.0):
    """Draw bat-like wings (for demons/dragons)."""
    s = scale
    ws = int(44 * s)
    wh = int(22 * s)
    wc = hex_to_rgb("#4A1A2E")
    wd = hex_to_rgb("#2A0A1E")

    # Left wing - scalloped
    lw = [
        (cx - int(4 * s), cy),
        (cx - int(ws * 0.4), cy - int(wh * 0.8)),
        (cx - int(ws * 0.6), cy - int(wh * 0.5)),
        (cx - int(ws * 0.8), cy - int(wh * 0.9)),
        (cx - ws, cy - int(wh * 0.3)),
        (cx - ws + int(6 * s), cy + int(4 * s)),
        (cx - int(4 * s), cy + int(6 * s)),
    ]
    poly(draw, lw, wc, OUTLINE_COLOR)

    # Right wing
    rw = [
        (cx + int(4 * s), cy),
        (cx + int(ws * 0.4), cy - int(wh * 0.8)),
        (cx + int(ws * 0.6), cy - int(wh * 0.5)),
        (cx + int(ws * 0.8), cy - int(wh * 0.9)),
        (cx + ws, cy - int(wh * 0.3)),
        (cx + ws - int(6 * s), cy + int(4 * s)),
        (cx + int(4 * s), cy + int(6 * s)),
    ]
    poly(draw, rw, wd, OUTLINE_COLOR)


def draw_mechanical_wings(draw, cx, cy, pal: EraPalette, scale=1.0):
    """Draw mechanical/airplane wings."""
    s = scale
    ws = int(48 * s)
    wc = hex_to_rgb(pal.shadow)
    wl = hex_to_rgb(lighten(pal.shadow))

    # Left wing
    lw = [
        (cx - int(6 * s), cy),
        (cx - ws, cy - int(6 * s)),
        (cx - ws, cy + int(2 * s)),
        (cx - int(6 * s), cy + int(6 * s)),
    ]
    poly(draw, lw, wc, OUTLINE_COLOR)

    # Right wing
    rw = [
        (cx + int(6 * s), cy),
        (cx + ws, cy - int(6 * s)),
        (cx + ws, cy + int(2 * s)),
        (cx + int(6 * s), cy + int(6 * s)),
    ]
    poly(draw, rw, wl, OUTLINE_COLOR)

    # Struts
    for frac in [0.3, 0.6]:
        lx = cx - int(6 * s) - int(ws * frac)
        rx = cx + int(6 * s) + int(ws * frac)
        line(draw, (cx, cy), (lx, cy - int(3 * s)), hex_to_rgb(pal.stone_earth), max(1, int(s)))
        line(draw, (cx, cy), (rx, cy - int(3 * s)), hex_to_rgb(pal.stone_earth), max(1, int(s)))


# ==========================================
# ERA-SPECIFIC ENEMY GENERATORS
# ==========================================

def generate_infantry(era, pal):
    """Generate infantry sprite for given era."""
    img = new_canvas()
    draw = ImageDraw.Draw(img)
    cx = SIZE // 2 + 8  # slightly right-facing
    by = SIZE - 32

    draw_ground_shadow(draw, cx, by)

    cfg = {
        0: dict(body_color=pal.shadow, head_detail="helmet_simple", weapon="spear", shield="round",
                armor_color=pal.stone_earth),
        1: dict(body_color=pal.shadow, head_detail="helmet_crest", weapon="sword", shield="rectangular",
                armor_color=pal.shadow),
        2: dict(body_color=pal.base, head_detail="turban", weapon="scimitar", shield=None,
                armor_color=pal.shadow),
        3: dict(body_color=pal.shadow, head_detail="helmet_simple", weapon="sword", shield="round",
                armor_color=pal.shadow),
        4: dict(body_color=pal.shadow, head_detail="mongol_helmet", weapon="bow", shield=None,
                armor_color=pal.shadow),
        5: dict(body_color=pal.shadow, head_detail="janissary_hat", weapon="musket", shield=None,
                armor_color=pal.base),
        6: dict(body_color=pal.base, head_detail="greatcoat_hat", weapon="rifle", shield=None,
                armor_color=pal.shadow),
        7: dict(body_color=pal.base, head_detail="leather_cap", weapon="rifle", shield=None,
                armor_color=pal.stone_earth),
        8: dict(body_color=pal.base, head_detail="military_cap", weapon="rifle", shield=None,
                armor_color=pal.shadow),
        9: dict(body_color=pal.shadow, head_detail="modern_helmet", weapon="rifle", shield=None,
                armor_color=pal.shadow),
    }

    c = cfg[era]
    draw_humanoid(draw, cx, by, pal, **c)

    # Era-specific extra details
    if era == 0:
        # Fur collar for tribal
        draw.arc([cx - 18, by - int(5.5 * UNIT), cx + 18, by - int(4.5 * UNIT)],
                 0, 180, fill=hex_to_rgb(pal.vegetation), width=4)
    elif era == 2:
        # Robe drape
        poly(draw, [(cx - 20, by - int(2 * UNIT)), (cx - 26, by),
                    (cx - 10, by), (cx - 14, by - int(2 * UNIT))],
             hex_to_rgb(pal.accent), OUTLINE_COLOR)
    elif era == 5:
        # Janissary sash
        sy = by - int(5 * UNIT)
        rect(draw, [cx - 16, sy, cx + 16, sy + 6], hex_to_rgb(pal.accent))
    elif era == 6:
        # Greatcoat skirt
        poly(draw, [(cx - 20, by - int(2.5 * UNIT)), (cx - 24, by),
                    (cx + 24, by), (cx + 20, by - int(2.5 * UNIT))],
             hex_to_rgb(pal.base), OUTLINE_COLOR)
    elif era == 7:
        # Bolshevik leather belt
        sy = by - int(3.5 * UNIT)
        rect(draw, [cx - 16, sy, cx + 16, sy + 4], hex_to_rgb(pal.stone_earth))
    elif era == 8:
        # Soviet belt + ammo pouches
        sy = by - int(3.5 * UNIT)
        rect(draw, [cx - 16, sy, cx + 16, sy + 4], hex_to_rgb(pal.stone_earth))
        rect(draw, [cx - 20, sy, cx - 14, sy + 8], hex_to_rgb(pal.shadow))
        rect(draw, [cx + 14, sy, cx + 20, sy + 8], hex_to_rgb(pal.shadow))
    elif era == 9:
        # Militia bandolier
        sy = by - int(5 * UNIT)
        line(draw, (cx - 18, sy), (cx + 10, by - int(2 * UNIT)),
             hex_to_rgb(pal.stone_earth), 3)
        line(draw, (cx + 18, sy), (cx - 10, by - int(2 * UNIT)),
             hex_to_rgb(pal.stone_earth), 3)

    draw_threat_badge(draw, "infantry")
    draw_health_bar(draw)
    return img


def generate_cavalry(era, pal):
    """Generate cavalry sprite for given era."""
    img = new_canvas()
    draw = ImageDraw.Draw(img)
    cx = SIZE // 2 - 4
    by = SIZE - 32

    draw_ground_shadow(draw, cx, by, w=50)

    # Draw horse
    horse_color = pal.shadow
    rider_y = draw_horse(draw, cx, by, pal)
    draw_saddle(draw, cx, by, pal)
    rider_base_y = by - int(26 * 1.0)

    # Rider on top
    rider_cfg = {
        0: dict(head_detail="helmet_simple", weapon="spear", shield=None, scale=0.75),
        1: dict(head_detail="helmet_crest", weapon="bow", shield=None, scale=0.75),
        2: dict(head_detail="turban", weapon="bow", shield=None, scale=0.75),
        3: dict(head_detail="helmet_simple", weapon="sword", shield=None, scale=0.75),
        4: dict(head_detail="mongol_helmet", weapon="bow", shield=None, scale=0.75),
        5: dict(head_detail="helmet_simple", weapon="sword", shield=None, scale=0.75),
        6: dict(head_detail="fur_hat", weapon="sword", shield=None, scale=0.75),
    }

    if era in rider_cfg:
        cfg = rider_cfg[era]
        draw_humanoid(draw, cx + 4, rider_base_y, pal,
                      body_color=pal.shadow, armor_color=pal.shadow,
                      **cfg)
    elif era == 7:
        # Armored car instead of horse
        _draw_armored_car(draw, cx, by, pal)
    elif era == 8:
        # Soviet tank
        _draw_tank(draw, cx, by, pal)
    elif era == 9:
        # Technical truck
        _draw_technical_truck(draw, cx, by, pal)

    # Era-specific decorations
    if era == 1:
        # Parthian horse armor
        rect(draw, [cx - 18, by - 28, cx + 18, by - 20], hex_to_rgb(pal.accent), OUTLINE_COLOR)
    elif era == 3:
        # Turkmen banner
        bx = cx + 30
        line(draw, (bx, rider_base_y - int(1.5 * UNIT * 0.75)), (bx, rider_base_y - int(4 * UNIT * 0.75)),
             hex_to_rgb(pal.stone_earth), 2)
        poly(draw, [(bx, rider_base_y - int(4 * UNIT * 0.75)),
                    (bx + 14, rider_base_y - int(3.5 * UNIT * 0.75)),
                    (bx, rider_base_y - int(3 * UNIT * 0.75))],
             hex_to_rgb(pal.accent), OUTLINE_COLOR)
    elif era == 4:
        # Mongol horse tail decoration
        poly(draw, [(cx - 28, by - 16), (cx - 38, by - 8), (cx - 32, by - 4), (cx - 24, by - 10)],
             hex_to_rgb(pal.accent), OUTLINE_COLOR)
    elif era == 5:
        # Persian horse armor
        rect(draw, [cx - 20, by - 30, cx + 20, by - 18],
             hex_to_rgb(lighten(pal.shadow)), OUTLINE_COLOR)

    draw_threat_badge(draw, "cavalry")
    draw_health_bar(draw)
    return img


def _draw_armored_car(draw, cx, by, pal):
    """Draw an armored car (Era 7 cavalry)."""
    # Body
    body_pts = [
        (cx - 32, by - 20), (cx + 32, by - 22),
        (cx + 36, by - 14), (cx + 30, by - 6),
        (cx - 28, by - 6), (cx - 34, by - 14),
    ]
    poly(draw, body_pts, hex_to_rgb(pal.shadow), OUTLINE_COLOR)

    # Turret
    ellipse(draw, [cx - 10, by - 32, cx + 14, by - 18],
            hex_to_rgb(darken(pal.shadow, 0.2)), OUTLINE_COLOR)

    # Gun barrel
    line(draw, (cx + 14, by - 26), (cx + 36, by - 30),
         hex_to_rgb(darken(pal.stone_earth, 0.4)), 3)

    # Wheels
    for wx in [cx - 18, cx + 18]:
        ellipse(draw, [wx - 8, by - 10, wx + 8, by + 2],
                hex_to_rgb(darken(pal.stone_earth, 0.3)), OUTLINE_COLOR)


def _draw_tank(draw, cx, by, pal):
    """Draw a Soviet tank (Era 8 cavalry)."""
    # Treads
    rect(draw, [cx - 36, by - 14, cx + 36, by],
         hex_to_rgb(darken(pal.shadow, 0.4)), OUTLINE_COLOR)
    # Tread detail
    for i in range(-30, 32, 8):
        line(draw, (cx + i, by - 14), (cx + i, by),
             hex_to_rgb(darken(pal.shadow, 0.6)), 1)

    # Hull
    hull_pts = [
        (cx - 30, by - 14), (cx + 30, by - 16),
        (cx + 32, by - 26), (cx - 28, by - 24),
    ]
    poly(draw, hull_pts, hex_to_rgb(pal.shadow), OUTLINE_COLOR)

    # Turret
    ellipse(draw, [cx - 12, by - 36, cx + 16, by - 22],
            hex_to_rgb(darken(pal.shadow, 0.15)), OUTLINE_COLOR)

    # Gun barrel
    line(draw, (cx + 16, by - 30), (cx + 42, by - 32),
         hex_to_rgb(darken(pal.stone_earth, 0.3)), 4)

    # Star emblem
    draw.ellipse([cx - 4, by - 30, cx + 4, by - 22],
                 fill=hex_to_rgb(pal.accent))


def _draw_technical_truck(draw, cx, by, pal):
    """Draw a technical truck with mounted gun (Era 9 cavalry)."""
    # Truck bed
    bed_pts = [
        (cx - 30, by - 18), (cx + 28, by - 20),
        (cx + 30, by - 12), (cx - 28, by - 10),
    ]
    poly(draw, bed_pts, hex_to_rgb(pal.shadow), OUTLINE_COLOR)

    # Cab
    cab_pts = [
        (cx + 20, by - 20), (cx + 38, by - 22),
        (cx + 40, by - 10), (cx + 28, by - 10),
    ]
    poly(draw, cab_pts, hex_to_rgb(lighten(pal.shadow)), OUTLINE_COLOR)

    # Windshield
    poly(draw, [(cx + 34, by - 20), (cx + 38, by - 20), (cx + 39, by - 14), (cx + 33, by - 14)],
         hex_to_rgb(pal.sky), OUTLINE_COLOR)

    # Mounted gun
    line(draw, (cx - 10, by - 20), (cx - 10, by - 36),
         hex_to_rgb(pal.stone_earth), 3)
    line(draw, (cx - 10, by - 34), (cx + 20, by - 38),
         hex_to_rgb(darken(pal.stone_earth, 0.3)), 4)

    # Wheels
    for wx in [cx - 18, cx + 10, cx + 30]:
        ellipse(draw, [wx - 7, by - 10, wx + 7, by + 2],
                hex_to_rgb("#222222"), OUTLINE_COLOR)


def generate_siege(era, pal):
    """Generate siege unit sprite for given era."""
    img = new_canvas()
    draw = ImageDraw.Draw(img)
    cx = SIZE // 2
    by = SIZE - 32

    draw_ground_shadow(draw, cx, by, w=44, h=14)

    wheel_top = draw_wheels(draw, cx, by, pal, wheel_count=2, spacing=36)

    siege_configs = {
        0: _draw_stone_thrower,
        1: _draw_roman_siege_engine,
        2: _draw_siege_ladder_unit,
        3: _draw_siege_ram_unit,
        4: _draw_siege_tower_unit,
        5: _draw_cannon_unit,
        6: _draw_artillery_piece,
        7: _draw_field_gun_unit,
        8: _draw_katyusha_unit,
        9: _draw_mortar_team_unit,
    }

    siege_configs[era](draw, cx, wheel_top, pal)

    draw_threat_badge(draw, "siege")
    draw_health_bar(draw)
    return img


def _draw_stone_thrower(draw, cx, wy, pal):
    """Era 0: Wooden frame with sling."""
    # Frame
    line(draw, (cx - 20, wy), (cx - 16, wy - 40), hex_to_rgb(pal.stone_earth), 4)
    line(draw, (cx + 20, wy), (cx + 16, wy - 40), hex_to_rgb(pal.stone_earth), 4)
    # Crossbar
    line(draw, (cx - 18, wy - 20), (cx + 18, wy - 20), hex_to_rgb(pal.stone_earth), 3)
    # Throwing arm
    line(draw, (cx, wy - 20), (cx + 30, wy - 50), hex_to_rgb(pal.stone_earth), 4)
    # Sling cup
    ellipse(draw, [cx + 24, wy - 56, cx + 38, wy - 46],
            hex_to_rgb(pal.stone_earth), OUTLINE_COLOR)
    # Counterweight
    rect(draw, [cx - 14, wy - 28, cx - 4, wy - 20],
         hex_to_rgb(pal.stone_earth), OUTLINE_COLOR)
    # Stone
    ellipse(draw, [cx + 28, wy - 54, cx + 34, wy - 48],
            hex_to_rgb(pal.stone_earth), OUTLINE_COLOR)


def _draw_roman_siege_engine(draw, cx, wy, pal):
    """Era 1: Roman-style siege tower/battering ram."""
    # Base platform
    rect(draw, [cx - 28, wy - 6, cx + 28, wy], hex_to_rgb(pal.stone_earth), OUTLINE_COLOR)
    # Frame
    rect(draw, [cx - 24, wy - 44, cx + 24, wy - 6], hex_to_rgb(pal.stone_earth), OUTLINE_COLOR)
    # Roof
    poly(draw, [(cx - 28, wy - 44), (cx + 28, wy - 44),
                (cx + 22, wy - 52), (cx - 22, wy - 52)],
         hex_to_rgb(pal.accent), OUTLINE_COLOR)
    # Ram
    line(draw, (cx - 24, wy - 26), (cx - 42, wy - 26),
         hex_to_rgb(darken(pal.stone_earth, 0.3)), 6)
    # Ram head
    poly(draw, [(cx - 42, wy - 32), (cx - 50, wy - 26), (cx - 42, wy - 20)],
         hex_to_rgb(pal.accent), OUTLINE_COLOR)


def _draw_siege_ladder_unit(draw, cx, wy, pal):
    """Era 2: Siege ladder."""
    # Two rails
    line(draw, (cx - 8, wy), (cx - 6, wy - 64), hex_to_rgb(pal.stone_earth), 3)
    line(draw, (cx + 8, wy), (cx + 6, wy - 64), hex_to_rgb(pal.stone_earth), 3)
    # Rungs
    for i in range(7):
        ry = wy - i * 9
        rx_l = cx - 8 + int(i * 0.3)
        rx_r = cx + 8 - int(i * 0.3)
        line(draw, (rx_l, ry), (rx_r, ry), hex_to_rgb(pal.stone_earth), 2)
    # Hook at top
    poly(draw, [(cx - 6, wy - 64), (cx - 12, wy - 68), (cx - 4, wy - 60)],
         hex_to_rgb(pal.accent), OUTLINE_COLOR)


def _draw_siege_ram_unit(draw, cx, wy, pal):
    """Era 3: Battering ram."""
    # Shelter
    pts = [
        (cx - 28, wy - 4), (cx + 28, wy - 4),
        (cx + 22, wy - 36), (cx - 22, wy - 36),
    ]
    poly(draw, pts, hex_to_rgb(pal.stone_earth), OUTLINE_COLOR)
    # Roof
    poly(draw, [(cx - 24, wy - 36), (cx + 24, wy - 36),
                (cx + 18, wy - 44), (cx - 18, wy - 44)],
         hex_to_rgb(pal.accent), OUTLINE_COLOR)
    # Ram beam
    line(draw, (cx - 22, wy - 20), (cx - 44, wy - 20),
         hex_to_rgb(pal.shadow), 6)
    # Ram head (iron)
    poly(draw, [(cx - 44, wy - 26), (cx - 52, wy - 20), (cx - 44, wy - 14)],
         hex_to_rgb(pal.accent), OUTLINE_COLOR)


def _draw_siege_tower_unit(draw, cx, wy, pal):
    """Era 4: Siege tower."""
    # Base
    rect(draw, [cx - 30, wy - 8, cx + 30, wy], hex_to_rgb(pal.stone_earth), OUTLINE_COLOR)
    # Tower body
    rect(draw, [cx - 24, wy - 56, cx + 24, wy - 8], hex_to_rgb(pal.shadow), OUTLINE_COLOR)
    # Platform levels
    for i in range(3):
        ly = wy - 8 - i * 16
        line(draw, (cx - 24, ly), (cx + 24, ly), hex_to_rgb(pal.stone_earth), 2)
    # Battlements
    for i in range(5):
        bx = cx - 20 + i * 10
        rect(draw, [bx, wy - 64, bx + 6, wy - 56],
             hex_to_rgb(pal.shadow), OUTLINE_COLOR)
    # Door
    rect(draw, [cx - 6, wy - 24, cx + 6, wy - 8],
         hex_to_rgb(darken(pal.shadow, 0.3)), OUTLINE_COLOR)
    # Ladder
    line(draw, (cx + 18, wy), (cx + 18, wy - 56), hex_to_rgb(pal.stone_earth), 2)


def _draw_cannon_unit(draw, cx, wy, pal):
    """Era 5: Ottoman cannon."""
    # Barrel
    line(draw, (cx - 16, wy - 16), (cx + 28, wy - 20),
         hex_to_rgb(darken(pal.stone_earth, 0.3)), 8)
    # Muzzle
    ellipse(draw, [cx + 24, wy - 26, cx + 34, wy - 14],
            hex_to_rgb(darken(pal.stone_earth, 0.2)), OUTLINE_COLOR)
    # Carriage
    pts = [(cx - 20, wy - 12), (cx + 16, wy - 12),
           (cx + 12, wy - 4), (cx - 16, wy - 4)]
    poly(draw, pts, hex_to_rgb(pal.stone_earth), OUTLINE_COLOR)
    # Decorative Ottoman accent
    rect(draw, [cx - 8, wy - 20, cx + 8, wy - 16],
         hex_to_rgb(pal.accent), OUTLINE_COLOR)


def _draw_artillery_piece(draw, cx, wy, pal):
    """Era 6: Russian Empire artillery."""
    # Barrel
    line(draw, (cx - 14, wy - 18), (cx + 30, wy - 22),
         hex_to_rgb(darken(pal.stone_earth, 0.2)), 7)
    # Muzzle ring
    ellipse(draw, [cx + 26, wy - 28, cx + 36, wy - 16],
            hex_to_rgb(darken(pal.stone_earth, 0.15)), OUTLINE_COLOR)
    # Carriage
    pts = [(cx - 18, wy - 14), (cx + 14, wy - 14),
           (cx + 10, wy - 4), (cx - 14, wy - 4)]
    poly(draw, pts, hex_to_rgb(pal.stone_earth), OUTLINE_COLOR)
    # Trail
    line(draw, (cx - 18, wy - 14), (cx - 36, wy - 4),
         hex_to_rgb(pal.stone_earth), 4)


def _draw_field_gun_unit(draw, cx, wy, pal):
    """Era 7: Field gun."""
    # Barrel
    line(draw, (cx - 10, wy - 14), (cx + 26, wy - 16),
         hex_to_rgb(darken(pal.stone_earth, 0.3)), 6)
    # Shield
    poly(draw, [(cx - 6, wy - 24), (cx + 6, wy - 24),
                (cx + 8, wy - 8), (cx - 8, wy - 8)],
         hex_to_rgb(pal.shadow), OUTLINE_COLOR)
    # Barrel through shield
    line(draw, (cx + 6, wy - 16), (cx + 26, wy - 16),
         hex_to_rgb(darken(pal.stone_earth, 0.3)), 5)
    # Carriage
    pts = [(cx - 14, wy - 8), (cx + 10, wy - 8),
           (cx + 8, wy - 2), (cx - 12, wy - 2)]
    poly(draw, pts, hex_to_rgb(pal.stone_earth), OUTLINE_COLOR)


def _draw_katyusha_unit(draw, cx, wy, pal):
    """Era 8: Katyusha rocket launcher."""
    # Truck bed
    rect(draw, [cx - 30, wy - 18, cx + 30, wy - 2],
         hex_to_rgb(pal.shadow), OUTLINE_COLOR)
    # Cab
    rect(draw, [cx + 22, wy - 20, cx + 38, wy - 6],
         hex_to_rgb(pal.base), OUTLINE_COLOR)
    # Rocket rails (angled)
    for i in range(8):
        rx = cx - 24 + i * 7
        line(draw, (rx, wy - 18), (rx + 4, wy - 42),
             hex_to_rgb(pal.stone_earth), 2)
    # Rockets
    for i in range(8):
        rx = cx - 24 + i * 7
        rect(draw, [rx + 1, wy - 44, rx + 6, wy - 36],
             hex_to_rgb(pal.accent), OUTLINE_COLOR)


def _draw_mortar_team_unit(draw, cx, wy, pal):
    """Era 9: Mortar team."""
    # Base plate
    rect(draw, [cx - 20, wy - 4, cx + 20, wy],
         hex_to_rgb(pal.stone_earth), OUTLINE_COLOR)
    # Bipod legs
    line(draw, (cx, wy - 4), (cx - 16, wy - 36), hex_to_rgb(pal.stone_earth), 3)
    line(draw, (cx, wy - 4), (cx + 16, wy - 36), hex_to_rgb(pal.stone_earth), 3)
    # Mortar tube
    line(draw, (cx, wy - 30), (cx, wy - 52), hex_to_rgb(darken(pal.stone_earth, 0.3)), 6)
    # Muzzle
    ellipse(draw, [cx - 6, wy - 56, cx + 6, wy - 50],
            hex_to_rgb(darken(pal.stone_earth, 0.2)), OUTLINE_COLOR)
    # Ammo crate
    rect(draw, [cx + 18, wy - 16, cx + 30, wy - 6],
         hex_to_rgb(pal.stone_earth), OUTLINE_COLOR)


def generate_flying(era, pal):
    """Generate flying unit sprite for given era."""
    img = new_canvas()
    draw = ImageDraw.Draw(img)
    cx = SIZE // 2
    cy = SIZE // 2 + 10  # Centered vertically (flying)

    flying_configs = {
        0: _draw_devi,
        1: _draw_war_eagle,
        2: _draw_desert_hawk,
        3: _draw_falcon,
        4: _draw_signal_arrow,
        5: _draw_messenger_pigeon,
        6: _draw_observation_balloon,
        7: _draw_recon_plane,
        8: _draw_mig_jet,
        9: _draw_surveillance_drone,
    }

    flying_configs[era](draw, cx, cy, pal)

    draw_threat_badge(draw, "flying")
    draw_health_bar(draw)
    return img


def _draw_bird_body(draw, cx, cy, pal, scale=1.0, tail_len=20):
    """Draw a bird body."""
    s = scale
    # Body
    body_pts = [
        (cx - int(16 * s), cy),
        (cx + int(12 * s), cy - int(6 * s)),
        (cx + int(18 * s), cy),
        (cx + int(12 * s), cy + int(6 * s)),
    ]
    poly(draw, body_pts, hex_to_rgb(pal.shadow), OUTLINE_COLOR)
    # Head
    head_x = cx + int(20 * s)
    ellipse(draw, [head_x - int(6 * s), cy - int(6 * s), head_x + int(6 * s), cy + int(6 * s)],
            hex_to_rgb(pal.shadow), OUTLINE_COLOR)
    # Beak
    beak_pts = [(head_x + int(6 * s), cy - int(2 * s)),
                (head_x + int(14 * s), cy),
                (head_x + int(6 * s), cy + int(2 * s))]
    poly(draw, beak_pts, hex_to_rgb(pal.accent), OUTLINE_COLOR)
    # Eye
    draw.ellipse([head_x + int(1 * s), cy - int(3 * s), head_x + int(4 * s), cy],
                 fill=hex_to_rgb("#000000"))
    # Tail
    tail_pts = [
        (cx - int(16 * s), cy),
        (cx - int(16 * s) - int(tail_len * s), cy - int(4 * s)),
        (cx - int(16 * s) - int(tail_len * s) + int(4 * s), cy),
        (cx - int(16 * s) - int(tail_len * s), cy + int(4 * s)),
    ]
    poly(draw, tail_pts, hex_to_rgb(darken(pal.shadow, 0.2)), OUTLINE_COLOR)


def _draw_devi(draw, cx, cy, pal):
    """Era 0: Mythical flying demon."""
    # Wings
    draw_bat_wings(draw, cx, cy, scale=1.2)
    # Body
    body_pts = [
        (cx - 14, cy - 10), (cx + 14, cy - 10),
        (cx + 18, cy + 14), (cx - 18, cy + 14),
    ]
    poly(draw, body_pts, hex_to_rgb("#5C1A1A"), OUTLINE_COLOR)
    # Head
    ellipse(draw, [cx - 10, cy - 24, cx + 10, cy - 8],
            hex_to_rgb("#7A2A2A"), OUTLINE_COLOR)
    # Horns
    for side in [-1, 1]:
        pts = [(cx + side * 8, cy - 18),
               (cx + side * 16, cy - 34),
               (cx + side * 10, cy - 14)]
        poly(draw, pts, hex_to_rgb("#8B0000"), OUTLINE_COLOR)
    # Glowing eyes
    draw.ellipse([cx - 6, cy - 20, cx - 2, cy - 16], fill=hex_to_rgb("#FF4444"))
    draw.ellipse([cx + 2, cy - 20, cx + 6, cy - 16], fill=hex_to_rgb("#FF4444"))
    # Claws
    for side in [-1, 1]:
        for j in range(3):
            claw_x = cx + side * 12 + j * int(side * 4)
            poly(draw, [(claw_x, cy + 14), (claw_x + side * 4, cy + 22),
                        (claw_x - side * 2, cy + 14)],
                 hex_to_rgb("#4A0A0A"), OUTLINE_COLOR)


def _draw_war_eagle(draw, cx, cy, pal):
    """Era 1: Large war eagle."""
    draw_wings(draw, cx, cy, pal, wing_span=60, wing_height=22)
    _draw_bird_body(draw, cx, cy, pal, scale=1.2, tail_len=24)


def _draw_desert_hawk(draw, cx, cy, pal):
    """Era 2: Desert hawk."""
    draw_wings(draw, cx, cy, pal, wing_span=48, wing_height=18)
    _draw_bird_body(draw, cx, cy, pal, scale=1.0, tail_len=18)
    # Desert markings
    line(draw, (cx - 6, cy - 2), (cx + 8, cy - 2), hex_to_rgb(pal.accent), 2)


def _draw_falcon(draw, cx, cy, pal):
    """Era 3: Falcon."""
    draw_wings(draw, cx, cy, pal, wing_span=44, wing_height=16)
    _draw_bird_body(draw, cx, cy, pal, scale=0.9, tail_len=16)
    # Gold jess (leash)
    line(draw, (cx - 4, cy + 6), (cx - 10, cy + 20), hex_to_rgb(pal.accent), 2)


def _draw_signal_arrow(draw, cx, cy, pal):
    """Era 4: Mongol signal arrow (flaming arrow)."""
    # Arrow shaft
    line(draw, (cx - 30, cy + 10), (cx + 20, cy - 6),
         hex_to_rgb(pal.stone_earth), 3)
    # Arrowhead
    poly(draw, [(cx + 20, cy - 6), (cx + 28, cy - 10), (cx + 28, cy - 2)],
         hex_to_rgb(pal.accent), OUTLINE_COLOR)
    # Fletching
    poly(draw, [(cx - 30, cy + 10), (cx - 36, cy + 4), (cx - 26, cy + 6)],
         hex_to_rgb(pal.shadow), OUTLINE_COLOR)
    poly(draw, [(cx - 30, cy + 10), (cx - 36, cy + 16), (cx - 26, cy + 14)],
         hex_to_rgb(pal.shadow), OUTLINE_COLOR)
    # Fire glow at tip
    for r, c in [(12, "#FF6600"), (8, "#FFAA00"), (4, "#FFDD00")]:
        ellipse(draw, [cx + 20 - r, cy - 6 - r, cx + 20 + r, cy - 6 + r],
                hex_to_rgb(c))
    # Smoke trail
    for i in range(4):
        sx = cx + 20 - i * 12
        sy = cy - 6 - i * 6
        ellipse(draw, [sx - 4, sy - 4, sx + 4, sy + 4],
                hex_to_rgb("#666666"))


def _draw_messenger_pigeon(draw, cx, cy, pal):
    """Era 5: Messenger pigeon with scroll."""
    draw_wings(draw, cx, cy, pal, wing_span=36, wing_height=14)
    _draw_bird_body(draw, cx, cy, pal, scale=0.7, tail_len=10)
    # Scroll on leg
    scroll_x = cx - 6
    scroll_y = cy + 8
    rect(draw, [scroll_x - 4, scroll_y - 2, scroll_x + 4, scroll_y + 6],
         hex_to_rgb("#F5DEB3"), OUTLINE_COLOR)
    # Scroll ends
    ellipse(draw, [scroll_x - 5, scroll_y - 4, scroll_x + 5, scroll_y],
            hex_to_rgb("#DEB887"), OUTLINE_COLOR)


def _draw_observation_balloon(draw, cx, cy, pal):
    """Era 6: Observation balloon."""
    # Balloon envelope
    ellipse(draw, [cx - 30, cy - 40, cx + 30, cy + 10],
            hex_to_rgb(pal.highlight), OUTLINE_COLOR)
    # Highlight stripe
    ellipse(draw, [cx - 10, cy - 32, cx + 10, cy - 4],
            hex_to_rgb(lighten(pal.highlight, 0.2)), None)
    # Ropes
    for rx in [-12, 0, 12]:
        line(draw, (cx + rx, cy + 10), (cx + rx, cy + 34),
             hex_to_rgb(pal.stone_earth), 1)
    # Basket
    rect(draw, [cx - 14, cy + 30, cx + 14, cy + 42],
         hex_to_rgb(pal.stone_earth), OUTLINE_COLOR)


def _draw_recon_plane(draw, cx, cy, pal):
    """Era 7: Reconnaissance biplane."""
    draw_mechanical_wings(draw, cx, cy, pal)
    # Second wing set (biplane)
    draw_mechanical_wings(draw, cx, cy + 10, pal)
    # Fuselage
    body_pts = [
        (cx - 28, cy + 2), (cx + 24, cy),
        (cx + 30, cy + 6), (cx - 30, cy + 8),
    ]
    poly(draw, body_pts, hex_to_rgb(pal.shadow), OUTLINE_COLOR)
    # Propeller
    line(draw, (cx + 30, cy + 3), (cx + 38, cy + 3),
         hex_to_rgb(pal.stone_earth), 2)
    # Tail
    poly(draw, [(cx - 28, cy + 2), (cx - 38, cy - 4), (cx - 36, cy + 6), (cx - 28, cy + 8)],
         hex_to_rgb(pal.shadow), OUTLINE_COLOR)
    # Cockpit
    ellipse(draw, [cx + 4, cy - 2, cx + 16, cy + 8],
            hex_to_rgb(pal.sky), OUTLINE_COLOR)


def _draw_mig_jet(draw, cx, cy, pal):
    """Era 8: MiG jet fighter."""
    # Fuselage
    body_pts = [
        (cx - 32, cy + 4), (cx + 28, cy - 2),
        (cx + 36, cy + 2), (cx + 32, cy + 8),
        (cx - 28, cy + 8),
    ]
    poly(draw, body_pts, hex_to_rgb(pal.shadow), OUTLINE_COLOR)
    # Nose cone
    poly(draw, [(cx + 28, cy - 2), (cx + 40, cy + 3), (cx + 36, cy + 2)],
         hex_to_rgb(darken(pal.shadow, 0.2)), OUTLINE_COLOR)
    # Wings (swept)
    wing_l = [(cx - 4, cy + 4), (cx - 20, cy - 16), (cx - 14, cy - 12), (cx + 4, cy + 2)]
    wing_r = [(cx - 4, cy + 6), (cx - 20, cy + 24), (cx - 14, cy + 20), (cx + 4, cy + 8)]
    poly(draw, wing_l, hex_to_rgb(pal.base), OUTLINE_COLOR)
    poly(draw, wing_r, hex_to_rgb(darken(pal.base, 0.15)), OUTLINE_COLOR)
    # Tail fin
    poly(draw, [(cx - 28, cy + 2), (cx - 36, cy - 10), (cx - 30, cy - 6), (cx - 24, cy + 6)],
         hex_to_rgb(pal.accent), OUTLINE_COLOR)
    # Cockpit
    ellipse(draw, [cx + 10, cy, cx + 22, cy + 6],
            hex_to_rgb(pal.sky), OUTLINE_COLOR)
    # Exhaust
    for r, a in [(8, 40), (5, 60), (3, 80)]:
        c = hex_to_rgb(pal.accent)
        ellipse(draw, [cx - 32 - r, cy + 2, cx - 32 + r, cy + 6],
                (c[0], c[1], c[2], a))


def _draw_surveillance_drone(draw, cx, cy, pal):
    """Era 9: Surveillance drone (quadcopter)."""
    # Central body
    rect(draw, [cx - 10, cy - 6, cx + 10, cy + 6],
         hex_to_rgb(pal.shadow), OUTLINE_COLOR)
    # Camera dome
    ellipse(draw, [cx - 6, cy + 2, cx + 6, cy + 12],
            hex_to_rgb(pal.sky), OUTLINE_COLOR)
    # Arms
    arm_len = 24
    for angle in [45, 135, 225, 315]:
        import math
        rad = math.radians(angle)
        ex = cx + int(arm_len * math.cos(rad))
        ey = cy + int(arm_len * math.sin(rad))
        line(draw, (cx, cy), (ex, ey), hex_to_rgb(pal.stone_earth), 2)
        # Rotor
        rotor_w = 10
        line(draw, (ex - rotor_w, ey), (ex + rotor_w, ey),
             hex_to_rgb(pal.base), 2)
    # LED lights
    draw.ellipse([cx - 2, cy - 4, cx + 2, cy], fill=hex_to_rgb("#00FF00"))
    draw.ellipse([cx - 2, cy, cx + 2, cy + 4], fill=hex_to_rgb("#FF0000"))


# ==========================================
# BOSS GENERATORS
# ==========================================

def generate_boss(era, pal):
    """Generate boss sprite for given era."""
    img = new_canvas()
    draw = ImageDraw.Draw(img)
    cx = SIZE // 2
    by = SIZE - 32

    draw_ground_shadow(draw, cx, by, w=50, h=14)

    boss_configs = {
        0: _draw_colchian_dragon,
        1: _draw_sassanid_elephant,
        2: _draw_arab_emir,
        3: _draw_atabeg,
        4: _draw_subutai_proxy,
        5: _draw_agha_khan,
        6: _draw_imperial_general,
        7: _draw_commissar,
        8: _draw_soviet_general_boss,
        9: _draw_warlord_commander,
    }

    boss_configs[era](draw, cx, by, pal)

    draw_threat_badge(draw, "boss")
    draw_health_bar(draw)
    return img


def _draw_boss_aura(draw, cx, cy, pal, radius=50):
    """Draw a purple/golden aura around boss."""
    accent = hex_to_rgb(pal.accent)
    for r in range(radius, 0, -4):
        alpha = int(30 * (r / radius))
        color = (accent[0], accent[1], accent[2], alpha)
        ellipse(draw, [cx - r, cy - r, cx + r, cy + r], fill=color)


def _draw_colchian_dragon(draw, cx, by, pal):
    """Era 0 BOSS: Colchian Dragon."""
    cy = by - 60
    _draw_boss_aura(draw, cx, cy, pal, radius=56)

    # Wings
    draw_bat_wings(draw, cx, cy - 10, scale=1.5)

    # Serpentine body
    body_pts = [
        (cx - 30, cy + 10), (cx - 20, cy + 20), (cx, cy + 18),
        (cx + 20, cy + 10), (cx + 30, cy + 20),
    ]
    poly(draw, body_pts, hex_to_rgb("#2D6B1E"), OUTLINE_COLOR)

    # Belly scales
    belly_pts = [
        (cx - 20, cy + 16), (cx, cy + 14), (cx + 20, cy + 10),
        (cx + 20, cy + 18), (cx, cy + 22), (cx - 20, cy + 22),
    ]
    poly(draw, belly_pts, hex_to_rgb(pal.accent), OUTLINE_COLOR)

    # Neck and head
    neck_pts = [
        (cx + 20, cy + 10), (cx + 30, cy - 4),
        (cx + 40, cy - 6), (cx + 34, cy + 6),
    ]
    poly(draw, neck_pts, hex_to_rgb("#2D6B1E"), OUTLINE_COLOR)

    # Head
    head_pts = [
        (cx + 34, cy - 6), (cx + 52, cy - 8),
        (cx + 54, cy - 2), (cx + 48, cy + 2),
        (cx + 34, cy + 2),
    ]
    poly(draw, head_pts, hex_to_rgb("#3A8B2E"), OUTLINE_COLOR)

    # Eye
    draw.ellipse([cx + 42, cy - 7, cx + 48, cy - 3],
                 fill=hex_to_rgb("#FF0000"))
    # Horns
    for dy in [-2, 4]:
        poly(draw, [(cx + 38, cy + dy - 2), (cx + 44, cy + dy - 14), (cx + 42, cy + dy)],
             hex_to_rgb(pal.accent), OUTLINE_COLOR)

    # Tail
    tail_pts = [
        (cx - 30, cy + 10), (cx - 44, cy + 16),
        (cx - 52, cy + 8), (cx - 48, cy + 18),
    ]
    poly(draw, tail_pts, hex_to_rgb("#1E5A14"), OUTLINE_COLOR)

    # Legs
    for lx in [-10, 14]:
        leg_pts = [
            (cx + lx, cy + 18), (cx + lx - 4, by - 4),
            (cx + lx + 6, by - 4), (cx + lx + 2, cy + 20),
        ]
        poly(draw, leg_pts, hex_to_rgb("#1E5A14"), OUTLINE_COLOR)

    # Fire breath particles
    for i in range(3):
        fx = cx + 54 + i * 6
        fy = cy - 4 + (i % 2) * 4
        r = 4 + i
        ellipse(draw, [fx - r, fy - r, fx + r, fy + r],
                hex_to_rgb("#FF6600" if i < 2 else "#FFDD00"))


def _draw_sassanid_elephant(draw, cx, by, pal):
    """Era 1 BOSS: Sassanid War Elephant."""
    _draw_boss_aura(draw, cx, by - 60, pal, radius=60)

    # Elephant body
    body_pts = [
        (cx - 34, by - 30), (cx + 34, by - 34),
        (cx + 38, by - 20), (cx - 30, by - 18),
    ]
    poly(draw, body_pts, hex_to_rgb(pal.shadow), OUTLINE_COLOR)

    # Head
    head_pts = [
        (cx + 30, by - 34), (cx + 46, by - 40),
        (cx + 48, by - 26), (cx + 36, by - 22),
    ]
    poly(draw, head_pts, hex_to_rgb(lighten(pal.shadow)), OUTLINE_COLOR)

    # Ear
    poly(draw, [(cx + 32, by - 36), (cx + 40, by - 44),
                (cx + 44, by - 36), (cx + 36, by - 32)],
         hex_to_rgb(darken(pal.shadow, 0.15)), OUTLINE_COLOR)

    # Trunk
    trunk_pts = [
        (cx + 44, by - 28), (cx + 50, by - 18),
        (cx + 46, by - 8), (cx + 40, by - 12),
    ]
    poly(draw, trunk_pts, hex_to_rgb(pal.shadow), OUTLINE_COLOR)

    # Tusk
    poly(draw, [(cx + 44, by - 28), (cx + 52, by - 20), (cx + 48, by - 18)],
         hex_to_rgb("#FFFFF0"), OUTLINE_COLOR)

    # Howdah (tower on back)
    rect(draw, [cx - 20, by - 52, cx + 20, by - 30],
         hex_to_rgb(pal.accent), OUTLINE_COLOR)
    # Howdah roof
    poly(draw, [(cx - 24, by - 52), (cx + 24, by - 52),
                (cx + 20, by - 60), (cx - 20, by - 60)],
         hex_to_rgb(pal.accent), OUTLINE_COLOR)
    # Howdah details
    rect(draw, [cx - 16, by - 48, cx + 16, by - 46],
         hex_to_rgb(pal.shadow), OUTLINE_COLOR)

    # Legs
    for lx in [-20, -4, 12, 26]:
        rect(draw, [cx + lx - 5, by - 18, cx + lx + 5, by - 2],
             hex_to_rgb(pal.shadow), OUTLINE_COLOR)
    # Feet
    for lx in [-20, -4, 12, 26]:
        ellipse(draw, [cx + lx - 6, by - 4, cx + lx + 6, by + 2],
                hex_to_rgb(darken(pal.shadow, 0.15)), OUTLINE_COLOR)

    # Tail
    line(draw, (cx - 34, by - 30), (cx - 42, by - 22),
         hex_to_rgb(pal.shadow), 3)
    poly(draw, [(cx - 42, by - 22), (cx - 48, by - 18), (cx - 44, by - 16)],
         hex_to_rgb(darken(pal.shadow, 0.15)), OUTLINE_COLOR)


def _draw_arab_emir(draw, cx, by, pal):
    """Era 2 BOSS: Arab Emir of Tbilisi."""
    _draw_boss_aura(draw, cx, by - 50, pal, radius=48)

    # Larger humanoid (boss scale)
    draw_humanoid(draw, cx, by, pal,
                  body_color=pal.accent, armor_color=pal.accent,
                  head_detail="turban", weapon=None, shield=None, scale=1.15)

    # Royal robes (longer)
    poly(draw, [(cx - 24, by - int(2.5 * UNIT)), (cx - 28, by),
                (cx + 28, by), (cx + 24, by - int(2.5 * UNIT))],
         hex_to_rgb(pal.accent), OUTLINE_COLOR)
    # Robe trim
    line(draw, (cx - 26, by - 4), (cx + 26, by - 4), hex_to_rgb(pal.shadow), 2)

    # Staff of command
    line(draw, (cx - 28, by - int(4 * UNIT)), (cx - 28, by - int(8 * UNIT)),
         hex_to_rgb(pal.accent), 4)
    # Orb on top
    ellipse(draw, [cx - 34, by - int(8.5 * UNIT), cx - 22, by - int(7.5 * UNIT)],
            hex_to_rgb(pal.accent), OUTLINE_COLOR)

    # Reinforcement symbols (small figures around)
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        import math
        rad = math.radians(angle)
        rx = cx + int(40 * math.cos(rad))
        ry = by - int(4 * UNIT) + int(30 * math.sin(rad))
        ellipse(draw, [rx - 2, ry - 2, rx + 2, ry + 2],
                fill=hex_to_rgb(pal.accent))


def _draw_atabeg(draw, cx, by, pal):
    """Era 3 BOSS: Atabeg of Azerbaijan."""
    _draw_boss_aura(draw, cx, by - 50, pal, radius=50)

    # Armored humanoid (boss scale)
    draw_humanoid(draw, cx, by, pal,
                  body_color=pal.shadow, armor_color=pal.shadow,
                  head_detail="helmet_crest", weapon="sword", shield="kite", scale=1.15)

    # Extra armor plates
    rect(draw, [cx - 22, by - int(5 * UNIT), cx + 22, by - int(4.5 * UNIT)],
         hex_to_rgb(pal.accent), OUTLINE_COLOR)
    # Shoulder pauldrons
    for side in [-1, 1]:
        ellipse(draw, [cx + side * 26 - 8, by - int(5.8 * UNIT),
                       cx + side * 26 + 8, by - int(5.2 * UNIT)],
                hex_to_rgb(pal.accent), OUTLINE_COLOR)

    # Commander's banner
    bx = cx + 32
    line(draw, (bx, by - int(5 * UNIT)), (bx, by - int(9 * UNIT)),
         hex_to_rgb(pal.stone_earth), 3)
    poly(draw, [(bx, by - int(9 * UNIT)), (bx + 20, by - int(8.5 * UNIT)),
                (bx, by - int(8 * UNIT))],
         hex_to_rgb(pal.accent), OUTLINE_COLOR)


def _draw_subutai_proxy(draw, cx, by, pal):
    """Era 4 BOSS: General Subutai's Proxy."""
    _draw_boss_aura(draw, cx, by - 50, pal, radius=50)

    # Mongol commander (boss scale)
    draw_humanoid(draw, cx, by, pal,
                  body_color=pal.shadow, armor_color=pal.accent,
                  head_detail="mongol_helmet", weapon="bow", shield=None, scale=1.15)

    # Lamellar armor overlay
    for i in range(5):
        ay = by - int((3.5 + i * 0.8) * UNIT)
        rect(draw, [cx - 20, ay, cx + 20, ay + int(0.5 * UNIT)],
             hex_to_rgb(pal.accent), OUTLINE_COLOR)

    # Commander's standard
    bx = cx + 30
    line(draw, (bx, by - int(5 * UNIT)), (bx, by - int(9.5 * UNIT)),
         hex_to_rgb(pal.stone_earth), 3)
    # Banner (Mongol style)
    poly(draw, [(bx, by - int(9.5 * UNIT)), (bx + 22, by - int(9 * UNIT)),
                (bx + 20, by - int(7 * UNIT)), (bx, by - int(7.5 * UNIT))],
         hex_to_rgb(pal.accent), OUTLINE_COLOR)

    # Speed aura lines
    for i in range(3):
        ly = by - int((2 + i) * UNIT)
        line(draw, (cx - 36, ly), (cx - 46, ly - 6),
             hex_to_rgb(pal.accent), 2)


def _draw_agha_khan(draw, cx, by, pal):
    """Era 5 BOSS: Agha Mohammad Khan."""
    _draw_boss_aura(draw, cx, by - 50, pal, radius=52)

    # Persian commander (boss scale)
    draw_humanoid(draw, cx, by, pal,
                  body_color=pal.base, armor_color=pal.accent,
                  head_detail="crown", weapon="sword", shield=None, scale=1.15)

    # Royal robes
    poly(draw, [(cx - 26, by - int(2.5 * UNIT)), (cx - 30, by),
                (cx + 30, by), (cx + 26, by - int(2.5 * UNIT))],
         hex_to_rgb(pal.base), OUTLINE_COLOR)
    # Gold trim
    line(draw, (cx - 28, by - 4), (cx + 28, by - 4), hex_to_rgb(pal.accent), 2)

    # Area damage effect (radiating rings)
    for r in [30, 40, 50]:
        rect_pts = [
            (cx - r, by - int(1.5 * UNIT)),
            (cx + r, by - int(1.5 * UNIT)),
            (cx + r, by + 4), (cx - r, by + 4),
        ]
        # Draw as dotted effect
        c = hex_to_rgb(pal.accent)
        for angle in range(0, 360, 15):
            import math
            rad = math.radians(angle)
            px = cx + int(r * math.cos(rad))
            py = by - int(0.7 * UNIT) + int(int(1.5 * UNIT) * math.sin(rad))
            draw.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(c[0], c[1], c[2], 120))


def _draw_imperial_general(draw, cx, by, pal):
    """Era 6 BOSS: Imperial General."""
    _draw_boss_aura(draw, cx, by - 50, pal, radius=48)

    # Russian general (boss scale)
    draw_humanoid(draw, cx, by, pal,
                  body_color=pal.base, armor_color=pal.base,
                  head_detail="greatcoat_hat", weapon="sword", shield=None, scale=1.15)

    # Greatcoat
    poly(draw, [(cx - 24, by - int(2.5 * UNIT)), (cx - 28, by + 2),
                (cx + 28, by + 2), (cx + 24, by - int(2.5 * UNIT))],
         hex_to_rgb(pal.base), OUTLINE_COLOR)

    # Epaulettes
    for side in [-1, 1]:
        ep_x = cx + side * 24
        ep_y = by - int(5.5 * UNIT)
        rect(draw, [ep_x - 8, ep_y - 4, ep_x + 8, ep_y + 4],
             hex_to_rgb(pal.accent), OUTLINE_COLOR)
        # Fringe
        for i in range(4):
            fx = ep_x - 6 + i * 4
            line(draw, (fx, ep_y + 4), (fx, ep_y + 10), hex_to_rgb(pal.accent), 1)

    # Medals
    for i in range(3):
        my = by - int(4 * UNIT) + i * 8
        ellipse(draw, [cx - 8 + i * 4, my, cx - 4 + i * 4, my + 6],
                fill=hex_to_rgb(pal.accent), outline=OUTLINE_COLOR)

    # Sash
    line(draw, (cx - 20, by - int(5 * UNIT)), (cx + 20, by - int(2 * UNIT)),
         hex_to_rgb(pal.accent), 3)


def _draw_commissar(draw, cx, by, pal):
    """Era 7 BOSS: Red Army Commissar."""
    _draw_boss_aura(draw, cx, by - 50, pal, radius=48)

    # Bolshevik commissar (boss scale)
    draw_humanoid(draw, cx, by, pal,
                  body_color=pal.base, armor_color=pal.stone_earth,
                  head_detail="leather_cap", weapon="rifle", shield=None, scale=1.15)

    # Long leather coat
    poly(draw, [(cx - 24, by - int(2.5 * UNIT)), (cx - 28, by + 2),
                (cx + 28, by + 2), (cx + 24, by - int(2.5 * UNIT))],
         hex_to_rgb(pal.stone_earth), OUTLINE_COLOR)

    # Red star on chest
    star_cx, star_cy = cx, by - int(4.5 * UNIT)
    for angle in range(0, 360, 72):
        import math
        rad = math.radians(angle)
        px = star_cx + int(8 * math.cos(rad))
        py = star_cy + int(8 * math.sin(rad))
        draw.ellipse([px - 2, py - 2, px + 2, py + 2],
                     fill=hex_to_rgb(pal.accent))
    draw.ellipse([star_cx - 3, star_cy - 3, star_cx + 3, star_cy + 3],
                 fill=hex_to_rgb(pal.accent))

    # Belt with pistol holster
    rect(draw, [cx - 18, by - int(3.5 * UNIT), cx + 18, by - int(3.3 * UNIT)],
         hex_to_rgb("#222222"))
    rect(draw, [cx + 10, by - int(3.5 * UNIT), cx + 18, by - int(2.5 * UNIT)],
         hex_to_rgb("#333333"), OUTLINE_COLOR)


def _draw_soviet_general_boss(draw, cx, by, pal):
    """Era 8 BOSS: Soviet General (multi-phase)."""
    _draw_boss_aura(draw, cx, by - 50, pal, radius=52)

    # Soviet general (boss scale)
    draw_humanoid(draw, cx, by, pal,
                  body_color=pal.base, armor_color=pal.shadow,
                  head_detail="military_cap", weapon="sword", shield=None, scale=1.15)

    # Greatcoat
    poly(draw, [(cx - 24, by - int(2.5 * UNIT)), (cx - 26, by + 2),
                (cx + 26, by + 2), (cx + 24, by - int(2.5 * UNIT))],
         hex_to_rgb(pal.base), OUTLINE_COLOR)

    # Epaulettes with stars
    for side in [-1, 1]:
        ep_x = cx + side * 22
        ep_y = by - int(5.5 * UNIT)
        rect(draw, [ep_x - 10, ep_y - 4, ep_x + 10, ep_y + 4],
             hex_to_rgb(pal.accent), OUTLINE_COLOR)
        # Stars
        draw.ellipse([ep_x - 3, ep_y - 1, ep_x + 3, ep_y + 3],
                     fill=hex_to_rgb("#FFD700"))

    # Multiple medal rows
    for row in range(3):
        for col in range(4):
            mx = cx - 10 + col * 6
            my = by - int(4 * UNIT) + row * 8
            rect(draw, [mx, my, mx + 4, my + 6],
                 hex_to_rgb(pal.accent), OUTLINE_COLOR)

    # Multi-phase indicators (3 glowing orbs)
    for i in range(3):
        ox = cx - 12 + i * 12
        oy = by - int(7 * UNIT)
        c = hex_to_rgb(pal.accent)
        ellipse(draw, [ox - 4, oy - 4, ox + 4, oy + 4],
                fill=(c[0], c[1], c[2], 180), outline=OUTLINE_COLOR)

    # Star on cap (larger)
    star_x, star_y = cx + 4, by - int(7.2 * UNIT)
    draw.ellipse([star_x - 4, star_y - 4, star_x + 4, star_y + 4],
                 fill=hex_to_rgb(pal.accent))


def _draw_warlord_commander(draw, cx, by, pal):
    """Era 9 BOSS: Warlord Commander."""
    _draw_boss_aura(draw, cx, by - 50, pal, radius=50)

    # Modern warlord (boss scale)
    draw_humanoid(draw, cx, by, pal,
                  body_color=pal.shadow, armor_color=pal.shadow,
                  head_detail="modern_helmet", weapon="rifle", shield=None, scale=1.15)

    # Tactical vest
    rect(draw, [cx - 20, by - int(5.2 * UNIT), cx + 20, by - int(3 * UNIT)],
         hex_to_rgb(darken(pal.shadow, 0.3)), OUTLINE_COLOR)
    # Pouches
    for i in range(4):
        px = cx - 14 + i * 8
        rect(draw, [px, by - int(4.5 * UNIT), px + 6, by - int(4 * UNIT)],
             hex_to_rgb(pal.stone_earth), OUTLINE_COLOR)

    # Bandolier
    line(draw, (cx - 18, by - int(5.5 * UNIT)), (cx + 14, by - int(2 * UNIT)),
         hex_to_rgb(pal.stone_earth), 3)
    line(draw, (cx + 18, by - int(5.5 * UNIT)), (cx - 14, by - int(2 * UNIT)),
         hex_to_rgb(pal.stone_earth), 3)

    # Shoulder marks (rank)
    for side in [-1, 1]:
        sx = cx + side * 22
        sy = by - int(5.5 * UNIT)
        rect(draw, [sx - 6, sy - 2, sx + 6, sy + 2],
             hex_to_rgb(pal.accent))

    # Command radio on back
    rect(draw, [cx - 14, by - int(5.8 * UNIT), cx - 4, by - int(4.8 * UNIT)],
         hex_to_rgb("#333333"), OUTLINE_COLOR)
    # Antenna
    line(draw, (cx - 10, by - int(5.8 * UNIT)), (cx - 10, by - int(7 * UNIT)),
         hex_to_rgb("#555555"), 2)


# ==========================================
# MAIN GENERATION
# ==========================================

def generate_all(base_output_dir=None):
    """Generate all 50 enemy sprites across all 10 eras."""
    output_dir = base_output_dir or BASE_DIR

    generators = {
        "infantry": generate_infantry,
        "cavalry": generate_cavalry,
        "siege": generate_siege,
        "flying": generate_flying,
        "boss": generate_boss,
    }

    total = 0
    for era_num in range(10):
        era_def = ERA_DEFS[era_num]
        pal = ERA_PALETTES[era_num]
        era_folder = era_def["folder"]
        era_dir = os.path.join(output_dir, era_folder)
        os.makedirs(era_dir, exist_ok=True)

        print(f"\n=== Era {era_num}: {pal.name} ===")

        for category, (slug, display_name) in era_def["enemies"].items():
            filename = f"en_e{era_num:02d}_{slug}_v01.png"
            filepath = os.path.join(era_dir, filename)

            gen_func = generators[category]
            sprite = gen_func(era_num, pal)
            sprite.save(filepath)
            total += 1
            print(f"  [{category.upper():>8}] {display_name:<30s} -> {filename}")

    print(f"\n=== Generated {total} enemy sprites ===")
    return total


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate enemy sprites for Sakartvelo Defenders")
    parser.add_argument("--output-dir", default=None, help="Custom output directory")
    parser.add_argument("--era", type=int, default=None, help="Generate only specific era (0-9)")
    args = parser.parse_args()

    if args.era is not None:
        # Generate single era
        era_num = args.era
        era_def = ERA_DEFS[era_num]
        pal = ERA_PALETTES[era_num]
        era_folder = era_def["folder"]
        era_dir = os.path.join(args.output_dir or BASE_DIR, era_folder)
        os.makedirs(era_dir, exist_ok=True)

        generators = {
            "infantry": generate_infantry,
            "cavalry": generate_cavalry,
            "siege": generate_siege,
            "flying": generate_flying,
            "boss": generate_boss,
        }

        print(f"\n=== Era {era_num}: {pal.name} ===")
        for category, (slug, display_name) in era_def["enemies"].items():
            filename = f"en_e{era_num:02d}_{slug}_v01.png"
            filepath = os.path.join(era_dir, filename)
            sprite = generators[category](era_num, pal)
            sprite.save(filepath)
            print(f"  [{category.upper():>8}] {display_name:<30s} -> {filename}")
        print(f"\n=== Generated 5 sprites for Era {era_num} ===")
    else:
        generate_all(args.output_dir)
