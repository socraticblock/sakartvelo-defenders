"""
Sakartvelo Defenders - Tower Upgrade Variant Generator
Generates 3 upgrade levels (L1/L2/L3) for each of 10 tower types.
Each level has distinct visual progression: size, detail, decorations, and glow effects.

Sprite sizes:
  L1: 256x256 centered in 512x512 canvas
  L2: 307x307 centered in 512x512 canvas  (+20%)
  L3: 358x358 centered in 512x512 canvas  (+40%)
"""

import sys
import os
import math

from PIL import Image, ImageDraw, ImageFont

# Import shared utilities from sprite_generator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sprite_generator import (
    hex_to_rgb, rgb_to_hex, desaturate, lighten, TowerGenerator, ERA_PALETTES
)

# ==========================================
# CONSTANTS
# ==========================================

CANVAS_SIZE = 512
SPRITE_SIZES = {1: 256, 2: 307, 3: 358}
OUTLINE_COLOR = "#1A1A1A"
OUTLINE_WIDTH = 2

# Neutral color palette for towers (stone grays, warm browns)
TOWER_PALETTE = {
    "wood_base":    "#8B6914",
    "wood_light":   "#B8860B",
    "wood_dark":    "#5C4A1E",
    "stone_base":   "#808080",
    "stone_light":  "#A9A9A9",
    "stone_dark":   "#4A4A4A",
    "brick_base":   "#8B7355",
    "brick_light":  "#A0926E",
    "brick_dark":   "#5E4D36",
    "metal_base":   "#696969",
    "metal_light":  "#9E9E9E",
    "metal_dark":   "#3C3C3C",
    "accent_gold":  "#DAA520",
    "accent_red":   "#C41E3A",
    "accent_blue":  "#4682B4",
    "accent_green": "#2E8B57",
    "accent_orange":"#E67E22",
    "roof_brown":   "#6B4226",
    "roof_dark":    "#3B2510",
    "straw":        "#C2B280",
    "iron":         "#3A3A3A",
    "concrete":     "#7A7A7A",
    "tech_cyan":    "#00BCD4",
    "tech_green":   "#4CAF50",
    "fire_orange":  "#FF6F00",
    "fire_yellow":  "#FFD600",
    "smoke_gray":   "#9E9E9E",
}

TOWER_TYPES = [
    "archer", "catapult", "wall", "cavalry", "siege_tower",
    "shrine", "gunpowder", "industrial", "bunker", "tech",
]

OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets", "towers", "upgrades"
)


# ==========================================
# DRAWING HELPERS
# ==========================================

def _h(hex_color):
    """Shortcut: hex string -> RGB tuple."""
    return hex_to_rgb(hex_color)


def draw_outline_rect(draw, bbox, fill=None, outline=OUTLINE_COLOR, width=OUTLINE_WIDTH):
    """Draw rectangle with consistent outline."""
    draw.rectangle(bbox, fill=fill, outline=outline, width=width)


def draw_outline_polygon(draw, pts, fill=None, outline=OUTLINE_COLOR):
    """Draw polygon with consistent outline."""
    draw.polygon(pts, fill=fill, outline=outline)


def draw_iso_block(draw, cx, cy, w, h, depth, base_col, light_col, dark_col):
    """Draw a 2D isometric block (front face + top face + right face).
    cx, cy = center-bottom of the block.
    """
    half_w = w // 2
    depth_px = max(int(w * 0.25), 4)
    top_off = int(h * 0.35)

    # Front face
    front = [(cx - half_w, cy - h), (cx + half_w, cy - h),
             (cx + half_w, cy), (cx - half_w, cy)]
    draw_outline_polygon(draw, front, fill=base_col)

    # Top face (parallelogram)
    top = [(cx - half_w, cy - h), (cx + half_w, cy - h),
           (cx + half_w + top_off, cy - h - top_off),
           (cx - half_w + top_off, cy - h - top_off)]
    draw_outline_polygon(draw, top, fill=light_col)

    # Right face
    right = [(cx + half_w, cy - h), (cx + half_w + top_off, cy - h - top_off),
             (cx + half_w + top_off, cy - top_off), (cx + half_w, cy)]
    draw_outline_polygon(draw, right, fill=dark_col)


def draw_iso_flat(draw, cx, cy, w, d, base_col, light_col, dark_col):
    """Draw a flat isometric platform (diamond)."""
    half_w = w // 2
    half_d = d // 2
    top = [(cx, cy - half_d), (cx + half_w, cy),
           (cx, cy + half_d), (cx - half_w, cy)]
    draw_outline_polygon(draw, top, fill=light_col)
    # front-right edge shading
    front_r = [(cx + half_w, cy), (cx, cy + half_d),
               (cx - half_w, cy), (cx, cy - half_d)]
    # thin edge
    draw_outline_polygon(draw, front_r, fill=light_col)


def draw_level_stars(draw, canvas_size, level):
    """Draw small star indicators in the top-right corner for the upgrade level."""
    if level < 1:
        return
    star_color = _h("#FFD700") if level == 3 else _h("#AAAAAA") if level == 2 else _h("#888888")
    outline_c = _h(OUTLINE_COLOR)
    cx = canvas_size - 30
    cy = 20
    for i in range(level):
        sx = cx - i * 22
        # Simple 5-point star
        star_pts = []
        for j in range(10):
            angle = math.radians(j * 36 - 90)
            r = 9 if j % 2 == 0 else 4
            star_pts.append((sx + int(r * math.cos(angle)), cy + int(r * math.sin(angle))))
        draw_outline_polygon(draw, star_pts, fill=star_color, outline=outline_c)


def draw_glow_overlay(img, center, glow_color_hex="#FFD700"):
    """Draw concentric circles with decreasing opacity (pulsing glow) for L3."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    gc = _h(glow_color_hex)
    cx, cy = center
    for i in range(6):
        radius = 140 + i * 25
        alpha = max(30 - i * 5, 5)
        color = (gc[0], gc[1], gc[2], alpha)
        od.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                    outline=color, width=3)
    # Central bright glow
    od.ellipse([cx - 50, cy - 50, cx + 50, cy + 50],
               fill=(gc[0], gc[1], gc[2], 20), outline=None)
    img = Image.alpha_composite(img, overlay)
    return img


def draw_banner(draw, x, y, width, height, color, pole_color="#5C4A1E"):
    """Draw a flag/banner on a pole."""
    # Pole
    draw.rectangle([x, y - height - 10, x + 3, y + 10],
                   fill=_h(pole_color), outline=_h(OUTLINE_COLOR))
    # Flag cloth (wavy triangle)
    pts = [(x + 3, y - height - 10),
           (x + 3 + width, y - height - 5 + height // 4),
           (x + 3 + width - 5, y - 5 - height // 4),
           (x + 3, y - 10)]
    draw_outline_polygon(draw, pts, fill=color)


def draw_georgian_cross(draw, cx, cy, size, color):
    """Draw a Georgian cross (equal-length arms, slightly shorter horizontal)."""
    v_w = max(size // 5, 2)
    h_w = max(size // 5, 2)
    v_len = size // 2
    h_len = size // 3
    c = _h(color)
    o = _h(OUTLINE_COLOR)
    # Vertical bar
    draw.rectangle([cx - v_w, cy - v_len, cx + v_w, cy + v_len], fill=c, outline=o)
    # Horizontal bar
    draw.rectangle([cx - h_len, cy - h_w, cx + h_len, cy + h_w], fill=c, outline=o)


def draw_crenellations(draw, cx, cy, width, count, block_w, block_h, base_col, light_col, dark_col):
    """Draw crenellation blocks along a line."""
    spacing = width / max(count, 1)
    start_x = cx - width // 2
    for i in range(count):
        bx = int(start_x + i * spacing + spacing // 2)
        draw_iso_block(draw, bx, cy, block_w, block_h, 0, base_col, light_col, dark_col)


# ==========================================
# PER-TOWER-TYPE DRAWING FUNCTIONS
# ==========================================
# Each function signature: (draw, cx, cy, level, s) where
#   draw = ImageDraw.Draw
#   cx, cy = center of the sprite area
#   level = 1, 2, or 3
#   s = sprite_size (256, 307, or 358) — used for proportional scaling

def _scale(base, level, s):
    """Scale a base value by level and sprite size. L1=256 is the reference."""
    return int(base * (s / 256) * (0.8 + level * 0.2))


# ---------- 1. ARCHER ----------
def draw_archer(draw, cx, cy, level, s):
    P = TOWER_PALETTE
    # Foundation
    fw, fh = _scale(90, level, s), _scale(25, level, s)
    draw_iso_block(draw, cx, cy, fw, fh, 0,
                   _h(P["stone_base"]), _h(P["stone_light"]), _h(P["stone_dark"]))

    # Tower body
    tw, th = _scale(60, level, s), _scale(110, level, s)
    body_base = P["wood_base"] if level == 1 else P["brick_base"] if level == 2 else P["stone_base"]
    body_light = P["wood_light"] if level == 1 else P["brick_light"] if level == 2 else P["stone_light"]
    body_dark = P["wood_dark"] if level == 1 else P["brick_dark"] if level == 2 else P["stone_dark"]
    draw_iso_block(draw, cx, cy - fh, tw, th, 0,
                   _h(body_base), _h(body_light), _h(body_dark))

    # Top platform
    pw, ph = _scale(75, level, s), _scale(15, level, s)
    draw_iso_block(draw, cx, cy - fh - th, pw, ph, 0,
                   _h(P["stone_base"]), _h(P["stone_light"]), _h(P["stone_dark"]))

    top_y = cy - fh - th - ph

    # Crenellations
    n_cren = 3 + level
    draw_crenellations(draw, cx, top_y, _scale(70, level, s), n_cren,
                       _scale(10, level, s), _scale(14, level, s),
                       _h(body_base), _h(body_light), _h(body_dark))

    # L2+: highlight trim
    if level >= 2:
        trim_y = cy - fh - th // 2
        draw.rectangle([cx - tw // 2 - 2, trim_y - 2, cx + tw // 2 + 2, trim_y + 2],
                       fill=_h(P["accent_gold"]))

    # L3: banner + gold accent
    if level >= 3:
        draw_banner(draw, cx + tw // 2 + 5, cy - fh - th - ph,
                    _scale(30, level, s), _scale(25, level, s),
                    _h(P["accent_red"]))
        draw_georgian_cross(draw, cx, top_y - _scale(8, level, s),
                            _scale(18, level, s), P["accent_gold"])


# ---------- 2. CATAPULT ----------
def draw_catapult(draw, cx, cy, level, s):
    P = TOWER_PALETTE
    # Base platform
    fw, fh = _scale(120, level, s), _scale(20, level, s)
    draw_iso_block(draw, cx, cy, fw, fh, 0,
                   _h(P["stone_base"]), _h(P["stone_light"]), _h(P["stone_dark"]))

    # Frame / support structure
    tw, th = _scale(70, level, s), _scale(60, level, s)
    draw_iso_block(draw, cx, cy - fh, tw, th, 0,
                   _h(P["wood_base"]), _h(P["wood_light"]), _h(P["wood_dark"]))

    arm_y = cy - fh - th
    arm_len = _scale(80, level, s)

    # Throwing arm
    arm_end_x = cx + arm_len
    arm_end_y = arm_y - _scale(50, level, s)
    draw.line([cx - arm_len // 3, arm_y, arm_end_x, arm_end_y],
              fill=_h(P["wood_dark"]), width=max(3, s // 60))

    # Counterweight
    cw_size = _scale(14, level, s)
    draw.ellipse([cx - arm_len // 3 - cw_size, arm_y - cw_size,
                  cx - arm_len // 3 + cw_size, arm_y + cw_size],
                 fill=_h(P["stone_dark"]), outline=_h(OUTLINE_COLOR))

    # Sling/bucket at arm tip
    bucket_size = _scale(8, level, s)
    draw.ellipse([arm_end_x - bucket_size, arm_end_y - bucket_size,
                  arm_end_x + bucket_size, arm_end_y + bucket_size],
                 fill=_h(P["accent_orange"]), outline=_h(OUTLINE_COLOR))

    # L2+: highlight trim + supports
    if level >= 2:
        # A-frame support
        draw.line([cx - tw // 4, cy - fh, cx, arm_y - _scale(20, level, s)],
                  fill=_h(P["wood_dark"]), width=max(2, s // 80))
        draw.line([cx + tw // 4, cy - fh, cx, arm_y - _scale(20, level, s)],
                  fill=_h(P["wood_dark"]), width=max(2, s // 80))

    # L3: fire effect + flag
    if level >= 3:
        # Fire glow on projectile
        for i in range(4):
            r = bucket_size + i * 4
            alpha_col = _h(P["fire_yellow"] if i % 2 == 0 else P["fire_orange"])
            draw.ellipse([arm_end_x - r, arm_end_y - r, arm_end_x + r, arm_end_y + r],
                         outline=alpha_col, width=2)
        # Flag
        draw_banner(draw, cx - tw // 2 - 5, cy - fh - th,
                    _scale(25, level, s), _scale(20, level, s),
                    _h(P["accent_red"]))


# ---------- 3. WALL ----------
def draw_wall(draw, cx, cy, level, s):
    P = TOWER_PALETTE
    wall_w = _scale(140, level, s)
    wall_h = _scale(70, level, s)

    mat_base = P["wood_base"] if level == 1 else P["stone_base"] if level == 2 else P["brick_base"]
    mat_light = P["wood_light"] if level == 1 else P["stone_light"] if level == 2 else P["brick_light"]
    mat_dark = P["wood_dark"] if level == 1 else P["stone_dark"] if level == 2 else P["brick_dark"]

    # Foundation
    draw_iso_block(draw, cx, cy, wall_w, _scale(15, level, s), 0,
                   _h(P["stone_dark"]), _h(P["stone_base"]), _h(P["metal_dark"]))

    # Main wall body
    draw_iso_block(draw, cx, cy - _scale(15, level, s), wall_w, wall_h, 0,
                   _h(mat_base), _h(mat_light), _h(mat_dark))

    top_y = cy - _scale(15, level, s) - wall_h

    # Battlements
    n_batt = 4 + level * 2
    draw_crenellations(draw, cx, top_y, wall_w - 10, n_batt,
                       _scale(10, level, s), _scale(16, level, s),
                       _h(mat_base), _h(mat_light), _h(mat_dark))

    # L2+: highlight color trim on wall mid-line
    if level >= 2:
        mid_y = cy - _scale(15, level, s) - wall_h // 2
        draw.rectangle([cx - wall_w // 2, mid_y - 1, cx + wall_w // 2, mid_y + 1],
                       fill=_h(P["accent_gold"]))

    # L3: iron reinforcement bands + portcullis
    if level >= 3:
        for i in range(3):
            band_y = cy - _scale(15, level, s) - wall_h // 4 * (i + 1)
            draw.rectangle([cx - wall_w // 2 - 3, band_y - 2,
                            cx + wall_w // 2 + 3, band_y + 2],
                           fill=_h(P["iron"]))
        # Portcullis (grid)
        gate_y = cy - _scale(15, level, s)
        for gy in range(5):
            yy = gate_y - gy * _scale(10, level, s)
            draw.line([cx - 12, yy, cx + 12, yy], fill=_h(P["metal_dark"]), width=2)
        draw.line([cx, gate_y, cx, gate_y - wall_h], fill=_h(P["metal_dark"]), width=2)


# ---------- 4. CAVALRY ----------
def draw_cavalry(draw, cx, cy, level, s):
    P = TOWER_PALETTE
    # Stable base
    bw, bh = _scale(110, level, s), _scale(30, level, s)
    draw_iso_block(draw, cx, cy, bw, bh, 0,
                   _h(P["wood_base"]), _h(P["wood_light"]), _h(P["wood_dark"]))

    # Stall body
    sw, sh = _scale(80, level, s), _scale(55, level, s)
    draw_iso_block(draw, cx, cy - bh, sw, sh, 0,
                   _h(P["wood_base"]), _h(P["wood_light"]), _h(P["wood_dark"]))

    # Horse stall opening (arch)
    arch_w = _scale(22, level, s)
    arch_h = _scale(28, level, s)
    arch_cy = cy - bh - sh // 2
    draw.ellipse([cx - arch_w, arch_cy - arch_h, cx + arch_w, arch_cy + arch_h],
                 fill=_h(P["wood_dark"]), outline=_h(OUTLINE_COLOR))

    # Roof
    roof_y = cy - bh - sh
    roof_w = _scale(90, level, s)
    # Sloped roof (triangle-ish)
    draw.polygon([
        (cx, roof_y - _scale(25, level, s)),
        (cx - roof_w // 2, roof_y),
        (cx + roof_w // 2, roof_y),
    ], fill=_h(P["roof_brown"]), outline=_h(OUTLINE_COLOR))

    top_y = roof_y - _scale(25, level, s)

    # L2+: horse emblem + trim
    if level >= 2:
        # Horse emblem circle
        er = _scale(10, level, s)
        draw.ellipse([cx - er, top_y - er - _scale(5, level, s),
                      cx + er, top_y + er - _scale(5, level, s)],
                     fill=_h(P["accent_gold"]), outline=_h(OUTLINE_COLOR))
        # Trim line
        draw.rectangle([cx - sw // 2, cy - bh - 2, cx + sw // 2, cy - bh + 2],
                       fill=_h(P["accent_gold"]))

    # L3: second stall + flag + horse head
    if level >= 3:
        # Second stall (smaller, to the right)
        s2x = cx + _scale(50, level, s)
        draw_iso_block(draw, s2x, cy, _scale(50, level, s), _scale(25, level, s), 0,
                       _h(P["wood_base"]), _h(P["wood_light"]), _h(P["wood_dark"]))
        draw_iso_block(draw, s2x, cy - _scale(25, level, s), _scale(45, level, s),
                       _scale(40, level, s), 0,
                       _h(P["wood_base"]), _h(P["wood_light"]), _h(P["wood_dark"]))
        draw.polygon([
            (s2x, cy - _scale(25, level, s) - _scale(40, level, s) - _scale(15, level, s)),
            (s2x - _scale(25, level, s), cy - _scale(25, level, s) - _scale(40, level, s)),
            (s2x + _scale(25, level, s), cy - _scale(25, level, s) - _scale(40, level, s)),
        ], fill=_h(P["roof_brown"]), outline=_h(OUTLINE_COLOR))
        # Banner
        draw_banner(draw, cx - roof_w // 2 - 3, roof_y,
                    _scale(25, level, s), _scale(22, level, s),
                    _h(P["accent_red"]))


# ---------- 5. SIEGE_TOWER ----------
def draw_siege_tower(draw, cx, cy, level, s):
    P = TOWER_PALETTE
    # Base
    bw, bh = _scale(80, level, s), _scale(20, level, s)
    draw_iso_block(draw, cx, cy, bw, bh, 0,
                   _h(P["stone_base"]), _h(P["stone_light"]), _h(P["stone_dark"]))

    # Tower body
    tw, th = _scale(55, level, s), _scale(100, level, s)
    body_mat = P["wood_base"] if level <= 2 else P["stone_base"]
    body_lit = P["wood_light"] if level <= 2 else P["stone_light"]
    body_drk = P["wood_dark"] if level <= 2 else P["stone_dark"]
    draw_iso_block(draw, cx, cy - bh, tw, th, 0,
                   _h(body_mat), _h(body_lit), _h(body_drk))

    top_y = cy - bh - th

    # Watch platform
    pw, ph = _scale(65, level, s), _scale(10, level, s)
    draw_iso_block(draw, cx, top_y, pw, ph, 0,
                   _h(P["stone_base"]), _h(P["stone_light"]), _h(P["stone_dark"]))

    plat_y = top_y - ph

    # Crenellations
    n_cr = 2 + level
    draw_crenellations(draw, cx, plat_y, _scale(60, level, s), n_cr,
                       _scale(8, level, s), _scale(12, level, s),
                       _h(body_mat), _h(body_lit), _h(body_drk))

    # L2+: gate arch at base
    if level >= 2:
        gate_w = _scale(14, level, s)
        gate_h = _scale(20, level, s)
        draw.ellipse([cx - gate_w, cy - bh - gate_h, cx + gate_w, cy - bh],
                     fill=_h(body_drk), outline=_h(OUTLINE_COLOR))

    # L3: grand battlements + side towers + banner
    if level >= 3:
        # Side turrets
        for dx in [-1, 1]:
            tx = cx + dx * _scale(35, level, s)
            draw_iso_block(draw, tx, cy, _scale(20, level, s), _scale(70, level, s), 0,
                           _h(P["stone_base"]), _h(P["stone_light"]), _h(P["stone_dark"]))
            # Tiny roof
            turret_top = cy - _scale(70, level, s)
            draw.polygon([
                (tx, turret_top - _scale(10, level, s)),
                (tx - _scale(14, level, s), turret_top),
                (tx + _scale(14, level, s), turret_top),
            ], fill=_h(P["roof_brown"]), outline=_h(OUTLINE_COLOR))
        draw_banner(draw, cx, plat_y - _scale(12, level, s),
                    _scale(20, level, s), _scale(18, level, s),
                    _h(P["accent_gold"]))


# ---------- 6. SHRINE ----------
def draw_shrine(draw, cx, cy, level, s):
    P = TOWER_PALETTE
    # Base platform
    bw, bh = _scale(100, level, s), _scale(18, level, s)
    draw_iso_block(draw, cx, cy, bw, bh, 0,
                   _h(P["stone_base"]), _h(P["stone_light"]), _h(P["stone_dark"]))

    # Body
    tw, th = _scale(60, level, s), _scale(70, level, s)
    draw_iso_block(draw, cx, cy - bh, tw, th, 0,
                   _h(P["stone_base"]), _h(P["stone_light"]), _h(P["stone_dark"]))

    body_top = cy - bh - th

    # Roof type depends on level
    if level == 1:
        # Simple flat cap
        rw = _scale(70, level, s)
        draw.polygon([
            (cx, body_top - _scale(15, level, s)),
            (cx - rw // 2, body_top),
            (cx + rw // 2, body_top),
        ], fill=_h(P["roof_brown"]), outline=_h(OUTLINE_COLOR))
        roof_top = body_top - _scale(15, level, s)
    elif level == 2:
        # Church steeple
        rw = _scale(65, level, s)
        draw.polygon([
            (cx, body_top - _scale(35, level, s)),
            (cx - rw // 2, body_top),
            (cx + rw // 2, body_top),
        ], fill=_h(P["roof_brown"]), outline=_h(OUTLINE_COLOR))
        roof_top = body_top - _scale(35, level, s)
        # Cross
        draw_georgian_cross(draw, cx, roof_top - _scale(10, level, s),
                            _scale(16, level, s), P["accent_gold"])
    else:
        # Grand cathedral dome
        dome_r = _scale(35, level, s)
        dome_top = body_top - dome_r
        draw.ellipse([cx - dome_r, dome_top, cx + dome_r, body_top],
                     fill=_h(P["accent_gold"]), outline=_h(OUTLINE_COLOR))
        roof_top = dome_top - _scale(5, level, s)
        # Cross on top
        draw_georgian_cross(draw, cx, roof_top - _scale(8, level, s),
                            _scale(20, level, s), P["accent_gold"])
        # Columns
        for i in range(4):
            col_x = cx + (i - 1.5) * _scale(18, level, s)
            col_bottom = body_top + 2
            col_top_y = body_top - _scale(50, level, s)
            draw.rectangle([col_x - 3, col_top_y, col_x + 3, col_bottom],
                           fill=_h(P["stone_light"]), outline=_h(OUTLINE_COLOR))
        # Banner
        draw_banner(draw, cx + tw // 2 + 3, body_top,
                    _scale(22, level, s), _scale(20, level, s),
                    _h(P["accent_red"]))

    # L2: trim
    if level == 2:
        draw.rectangle([cx - tw // 2 - 1, body_top + 2, cx + tw // 2 + 1, body_top + 5],
                       fill=_h(P["accent_gold"]))


# ---------- 7. GUNPOWDER ----------
def draw_gunpowder(draw, cx, cy, level, s):
    P = TOWER_PALETTE
    # Base
    bw, bh = _scale(110, level, s), _scale(22, level, s)
    draw_iso_block(draw, cx, cy, bw, bh, 0,
                   _h(P["stone_base"]), _h(P["stone_light"]), _h(P["stone_dark"]))

    # Bunker body
    tw, th = _scale(85, level, s), _scale(65, level, s)
    draw_iso_block(draw, cx, cy - bh, tw, th, 0,
                   _h(P["brick_base"]), _h(P["brick_light"]), _h(P["brick_dark"]))

    body_top = cy - bh - th
    cannon_y = cy - bh - th // 2

    # Cannon(s)
    n_cannons = level
    cannon_len = _scale(50, level, s)
    cannon_h = max(3, s // 70)
    for i in range(n_cannons):
        cy_off = (i - (n_cannons - 1) / 2) * _scale(18, level, s)
        c_y = int(cannon_y + cy_off)
        # Barrel
        draw.rectangle([cx - cannon_len, c_y - cannon_h,
                        cx + _scale(15, level, s), c_y + cannon_h],
                       fill=_h(P["metal_base"]), outline=_h(OUTLINE_COLOR))
        # Muzzle ring
        draw.ellipse([cx - cannon_len - 3, c_y - cannon_h - 2,
                      cx - cannon_len + 5, c_y + cannon_h + 2],
                     fill=_h(P["metal_dark"]), outline=_h(OUTLINE_COLOR))
        # Smoke puffs
        for j in range(3):
            sx = cx - cannon_len - 8 - j * _scale(8, level, s)
            sy = c_y - j * _scale(5, level, s)
            sr = _scale(5 + j * 2, level, s)
            draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                         fill=_h(P["smoke_gray"]), outline=None)

    # L2+: gunport openings
    if level >= 2:
        for i in range(2 + level):
            port_x = cx - tw // 3 + i * _scale(15, level, s)
            port_y = cy - bh - th // 4
            draw.rectangle([port_x - 4, port_y - 6, port_x + 4, port_y + 6],
                           fill=_h(P["metal_dark"]), outline=_h(OUTLINE_COLOR))

    # L3: flags + gold trim
    if level >= 3:
        draw.rectangle([cx - tw // 2, body_top - 1, cx + tw // 2, body_top + 3],
                       fill=_h(P["accent_gold"]))
        for side in [-1, 1]:
            draw_banner(draw, cx + side * (tw // 2 + 3), body_top,
                        _scale(20, level, s), _scale(18, level, s),
                        _h(P["accent_red"]))


# ---------- 8. INDUSTRIAL ----------
def draw_industrial(draw, cx, cy, level, s):
    P = TOWER_PALETTE
    # Concrete base
    bw, bh = _scale(120, level, s), _scale(20, level, s)
    draw_iso_block(draw, cx, cy, bw, bh, 0,
                   _h(P["concrete"]), _h(P["stone_light"]), _h(P["stone_dark"]))

    # Structure body
    tw, th = _scale(90, level, s), _scale(70, level, s)
    draw_iso_block(draw, cx, cy - bh, tw, th, 0,
                   _h(P["metal_base"]), _h(P["metal_light"]), _h(P["metal_dark"]))

    body_top = cy - bh - th

    # Machine gun position(s)
    n_guns = level
    for i in range(n_guns):
        gx = cx + (i - (n_guns - 1) / 2) * _scale(30, level, s)
        gy = body_top - _scale(5, level, s)
        # Gun mount
        draw.ellipse([int(gx) - 8, int(gy) - 5, int(gx) + 8, int(gy) + 5],
                     fill=_h(P["metal_dark"]), outline=_h(OUTLINE_COLOR))
        # Barrel
        barrel_len = _scale(35, level, s)
        draw.rectangle([int(gx), int(gy) - 2, int(gx) + barrel_len, int(gy) + 2],
                       fill=_h(P["metal_base"]), outline=_h(OUTLINE_COLOR))

    # Chimney / exhaust
    chimney_h = _scale(40, level, s) + level * _scale(10, level, s)
    chimney_w = _scale(14, level, s)
    draw.rectangle([cx + tw // 4, body_top - chimney_h,
                    cx + tw // 4 + chimney_w, body_top],
                   fill=_h(P["metal_base"]), outline=_h(OUTLINE_COLOR))
    # Smoke
    for i in range(level + 1):
        sx = cx + tw // 4 + chimney_w // 2
        sy = body_top - chimney_h - i * _scale(8, level, s)
        sr = _scale(5 + i * 3, level, s)
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=_h(P["smoke_gray"]), outline=None)

    # L2+: warning stripes
    if level >= 2:
        stripe_y = cy - bh - th // 3
        for i in range(4):
            sx = cx - tw // 2 + i * _scale(20, level, s)
            draw.rectangle([sx, int(stripe_y) - 2, sx + _scale(8, level, s), int(stripe_y) + 2],
                           fill=_h(P["accent_orange"]))

    # L3: bunker top + searchlight
    if level >= 3:
        # Bunker reinforcement
        draw.rectangle([cx - tw // 2 - 3, body_top - 5, cx + tw // 2 + 3, body_top],
                       fill=_h(P["iron"]))
        # Searchlight
        sl_x = cx - tw // 4
        sl_y = body_top - _scale(10, level, s)
        sl_r = _scale(8, level, s)
        draw.ellipse([int(sl_x) - sl_r, int(sl_y) - sl_r,
                      int(sl_x) + sl_r, int(sl_y) + sl_r],
                     fill=_h(P["tech_cyan"]), outline=_h(OUTLINE_COLOR))
        # Light beam
        beam_len = _scale(60, level, s)
        draw.polygon([
            (int(sl_x), int(sl_y) - sl_r // 2),
            (int(sl_x), int(sl_y) + sl_r // 2),
            (int(sl_x) - beam_len, int(sl_y) + sl_r * 2),
            (int(sl_x) - beam_len, int(sl_y) - sl_r * 2),
        ], fill=(0, 188, 212, 40), outline=None)


# ---------- 9. BUNKER ----------
def draw_bunker(draw, cx, cy, level, s):
    P = TOWER_PALETTE
    # Base
    bw, bh = _scale(130, level, s), _scale(25, level, s)
    draw_iso_block(draw, cx, cy, bw, bh, 0,
                   _h(P["concrete"]), _h(P["stone_light"]), _h(P["stone_dark"]))

    # Main body
    tw, th = _scale(100 + level * 10, level, s), _scale(50, level, s)
    draw_iso_block(draw, cx, cy - bh, tw, th, 0,
                   _h(P["concrete"]), _h(P["stone_light"]), _h(P["stone_dark"]))

    body_top = cy - bh - th

    # Sandbag rows
    n_rows = 1 + level
    for r in range(n_rows):
        row_y = body_top + r * _scale(8, level, s)
        row_w = tw - r * _scale(5, level, s)
        for i in range(int(row_w // _scale(12, level, s))):
            bx = cx - int(row_w) // 2 + i * int(_scale(12, level, s))
            draw.rectangle([bx, int(row_y), bx + int(_scale(10, level, s)), int(row_y + _scale(7, level, s))],
                           fill=_h(P["straw"]), outline=_h(OUTLINE_COLOR))

    # Firing slit
    slit_y = cy - bh - th // 2
    slit_w = _scale(25, level, s)
    draw.rectangle([cx - slit_w, int(slit_y) - 3, cx + slit_w, int(slit_y) + 3],
                   fill=_h(P["metal_dark"]), outline=_h(OUTLINE_COLOR))

    # L2+: additional slits + trim
    if level >= 2:
        for side in [-1, 1]:
            sx = cx + side * _scale(35, level, s)
            draw.rectangle([int(sx) - 8, int(slit_y) - 2, int(sx) + 8, int(slit_y) + 2],
                           fill=_h(P["metal_dark"]))

    # L3: massive fortress — extra walls, iron bands, searchlight
    if level >= 3:
        # Side walls
        for dx in [-1, 1]:
            wx = cx + dx * _scale(55, level, s)
            draw_iso_block(draw, wx, cy, _scale(25, level, s), _scale(55, level, s), 0,
                           _h(P["concrete"]), _h(P["stone_light"]), _h(P["stone_dark"]))
        # Iron reinforcement bands
        for i in range(3):
            band_y = cy - bh - th // 4 * (i + 1)
            draw.rectangle([cx - tw // 2 - 2, int(band_y) - 2,
                            cx + tw // 2 + 2, int(band_y) + 2],
                           fill=_h(P["iron"]))
        # Searchlight
        sl_r = _scale(6, level, s)
        draw.ellipse([cx - sl_r, body_top - _scale(12, level, s) - sl_r,
                      cx + sl_r, body_top - _scale(12, level, s) + sl_r],
                     fill=_h(P["tech_cyan"]), outline=_h(OUTLINE_COLOR))


# ---------- 10. TECH ----------
def draw_tech(draw, cx, cy, level, s):
    P = TOWER_PALETTE
    # Circular base
    base_r = _scale(55, level, s)
    draw.ellipse([cx - base_r, cy - base_r // 3, cx + base_r, cy + base_r // 3],
                 fill=_h(P["metal_base"]), outline=_h(OUTLINE_COLOR))

    # Central column
    col_w = _scale(20, level, s)
    col_h = _scale(70, level, s)
    draw.rectangle([cx - col_w // 2, cy - col_h - base_r // 3,
                    cx + col_w // 2, cy - base_r // 3],
                   fill=_h(P["metal_base"]), outline=_h(OUTLINE_COLOR))

    col_top = cy - col_h - base_r // 3

    if level == 1:
        # Basic outpost: small dish on top
        dish_r = _scale(15, level, s)
        draw.arc([cx - dish_r, col_top - dish_r, cx + dish_r, col_top + dish_r // 2],
                 180, 360, fill=_h(P["metal_light"]), width=3)
        # Antenna
        draw.line([cx, col_top, cx, col_top - _scale(25, level, s)],
                  fill=_h(P["metal_dark"]), width=2)
        draw.ellipse([cx - 3, col_top - _scale(28, level, s), cx + 3, col_top - _scale(22, level, s)],
                     fill=_h(P["accent_red"]))

    elif level == 2:
        # Radar station: rotating dish + extra antennas
        dish_r = _scale(25, level, s)
        draw.ellipse([cx - dish_r, col_top - dish_r // 2,
                      cx + dish_r, col_top + dish_r // 2],
                     fill=_h(P["metal_light"]), outline=_h(OUTLINE_COLOR))
        # Support arm
        draw.line([cx, col_top, cx, col_top - _scale(20, level, s)],
                  fill=_h(P["metal_dark"]), width=3)
        # Radar sweep circle
        sweep_r = _scale(35, level, s)
        draw.ellipse([cx - sweep_r, col_top - _scale(20, level, s) - sweep_r,
                      cx + sweep_r, col_top - _scale(20, level, s) + sweep_r],
                     outline=_h(P["tech_green"]), width=2)
        # Side antennas
        for side in [-1, 1]:
            ax = cx + side * _scale(20, level, s)
            draw.line([ax, cy - base_r // 3, ax, col_top - _scale(15, level, s)],
                      fill=_h(P["metal_dark"]), width=2)
        # Trim
        draw.rectangle([cx - col_w // 2 - 1, cy - base_r // 3 - col_h // 2,
                        cx + col_w // 2 + 1, cy - base_r // 3 - col_h // 2 + 3],
                       fill=_h(P["tech_cyan"]))

    else:
        # Drone command center: dome + radar arrays + drone pads
        dome_r = _scale(30, level, s)
        draw.ellipse([cx - dome_r, col_top - dome_r, cx + dome_r, col_top + dome_r // 2],
                     fill=_h(P["metal_light"]), outline=_h(OUTLINE_COLOR))
        dome_top = col_top - dome_r

        # Radar arrays (4 antennas)
        for i in range(4):
            angle = math.radians(i * 90 + 45)
            ax = cx + int(dome_r * 0.8 * math.cos(angle))
            ay = col_top + int(dome_r * 0.4 * math.sin(angle))
            draw.line([ax, ay, ax, ay - _scale(20, level, s)],
                      fill=_h(P["metal_dark"]), width=2)
            draw.ellipse([ax - 3, ay - _scale(23, level, s), ax + 3, ay - _scale(17, level, s)],
                         fill=_h(P["tech_cyan"]))

        # Energy rings
        for i in range(3):
            ring_r = dome_r + _scale(10, level, s) + i * _scale(12, level, s)
            draw.ellipse([cx - ring_r, col_top - ring_r // 2,
                          cx + ring_r, col_top + ring_r // 2],
                         outline=_h(P["tech_cyan"]), width=2)

        # Drone pads (2 small platforms)
        for side in [-1, 1]:
            px = cx + side * _scale(45, level, s)
            py = cy - base_r // 3
            pr = _scale(10, level, s)
            draw.ellipse([int(px) - pr, int(py) - pr // 2,
                          int(px) + pr, int(py) + pr // 2],
                         fill=_h(P["metal_dark"]), outline=_h(OUTLINE_COLOR))
            # Mini drone
            draw.ellipse([int(px) - 5, int(py) - _scale(20, level, s) - 3,
                          int(px) + 5, int(py) - _scale(20, level, s) + 3],
                         fill=_h(P["metal_light"]), outline=_h(OUTLINE_COLOR))
            # Rotor lines
            for r_angle in [0, 90]:
                ra = math.radians(r_angle)
                draw.line([int(px) - int(8 * math.cos(ra)),
                           int(py) - _scale(20, level, s) - int(2 * math.sin(ra)),
                           int(px) + int(8 * math.cos(ra)),
                           int(py) - _scale(20, level, s) + int(2 * math.sin(ra))],
                          fill=_h(P["metal_dark"]), width=1)

        # Banner
        draw_banner(draw, cx - dome_r - 5, col_top,
                    _scale(18, level, s), _scale(16, level, s),
                    _h(P["tech_cyan"]))


# ==========================================
# TOWER DRAW DISPATCH
# ==========================================

TOWER_DRAW_FUNCS = {
    "archer": draw_archer,
    "catapult": draw_catapult,
    "wall": draw_wall,
    "cavalry": draw_cavalry,
    "siege_tower": draw_siege_tower,
    "shrine": draw_shrine,
    "gunpowder": draw_gunpowder,
    "industrial": draw_industrial,
    "bunker": draw_bunker,
    "tech": draw_tech,
}

# Glow colors per tower type for L3
TOWER_GLOW_COLORS = {
    "archer": "#DAA520",
    "catapult": "#FF6F00",
    "wall": "#4682B4",
    "cavalry": "#DAA520",
    "siege_tower": "#C41E3A",
    "shrine": "#FFD700",
    "gunpowder": "#FF6F00",
    "industrial": "#E67E22",
    "bunker": "#00BCD4",
    "tech": "#00BCD4",
}


# ==========================================
# MAIN GENERATOR
# ==========================================

def generate_upgrade_variant(tower_type: str, level: int) -> Image.Image:
    """Generate a single tower upgrade variant.

    Args:
        tower_type: One of the 10 tower type names.
        level: 1, 2, or 3.

    Returns:
        PIL Image (RGBA, 512x512).
    """
    sprite_size = SPRITE_SIZES[level]
    canvas = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    # Center of canvas
    cx = CANVAS_SIZE // 2
    cy = CANVAS_SIZE // 2 + sprite_size // 6  # slightly lower to leave headroom

    # Dispatch to tower-specific draw function
    draw_func = TOWER_DRAW_FUNCS.get(tower_type)
    if draw_func is None:
        raise ValueError(f"Unknown tower type: {tower_type}")

    draw_func(draw, cx, cy, level, sprite_size)

    # Level star indicators
    draw_level_stars(draw, CANVAS_SIZE, level)

    # L3 glow overlay
    if level == 3:
        glow_color = TOWER_GLOW_COLORS.get(tower_type, "#FFD700")
        canvas = draw_glow_overlay(canvas, (cx, cy - sprite_size // 4), glow_color)

    return canvas


def generate_all_upgrades():
    """Generate all 30 tower upgrade variants (10 types x 3 levels)."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    count = 0
    for tower_type in TOWER_TYPES:
        for level in range(1, 4):
            filename = f"tw_{tower_type}_l{level}_v01.png"
            filepath = os.path.join(OUTPUT_DIR, filename)

            img = generate_upgrade_variant(tower_type, level)
            img.save(filepath)
            count += 1
            print(f"  [{count:02d}/30] {filename}")

    print(f"\nDone! Generated {count} tower upgrade sprites in {OUTPUT_DIR}")


def generate_upgrade_sheet(tower_type: str, output_path: str = None):
    """Generate a horizontal sheet showing L1-L2-L3 progression for one tower type."""
    if output_path is None:
        output_path = os.path.join(OUTPUT_DIR, f"sheet_{tower_type}_upgrades.png")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    sheet = Image.new("RGBA", (CANVAS_SIZE * 3, CANVAS_SIZE), (30, 30, 30, 255))
    draw = ImageDraw.Draw(sheet)

    for i, level in enumerate([1, 2, 3]):
        variant = generate_upgrade_variant(tower_type, level)
        sheet.paste(variant, (i * CANVAS_SIZE, 0))
        draw.text((i * CANVAS_SIZE + 10, CANVAS_SIZE - 30),
                  f"Level {level}", fill=(200, 200, 200, 255))

    sheet.save(output_path)
    print(f"Saved upgrade sheet: {output_path}")


def generate_master_sheet(output_path: str = None):
    """Generate a master sheet with all 10 tower types x 3 levels = 30 sprites."""
    if output_path is None:
        output_path = os.path.join(OUTPUT_DIR, "master_upgrade_sheet.png")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    cols = 3  # L1, L2, L3
    rows = len(TOWER_TYPES)
    sheet = Image.new("RGBA", (CANVAS_SIZE * cols, CANVAS_SIZE * rows), (30, 30, 30, 255))
    draw = ImageDraw.Draw(sheet)

    for r, tower_type in enumerate(TOWER_TYPES):
        for c, level in enumerate([1, 2, 3]):
            variant = generate_upgrade_variant(tower_type, level)
            sheet.paste(variant, (c * CANVAS_SIZE, r * CANVAS_SIZE))
            # Labels
            draw.text((c * CANVAS_SIZE + 10, r * CANVAS_SIZE + 10),
                      f"{tower_type} L{level}", fill=(200, 200, 200, 255))

    sheet.save(output_path)
    print(f"Saved master sheet: {output_path}")


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sakartvelo Defenders - Tower Upgrade Generator")
    parser.add_argument("--all", action="store_true", help="Generate all 30 upgrade variants")
    parser.add_argument("--sheet", type=str, default=None,
                        help="Generate upgrade sheet for a specific tower type")
    parser.add_argument("--master", action="store_true",
                        help="Generate master sheet with all towers and levels")
    parser.add_argument("--tower", type=str, default=None,
                        help="Tower type to generate (e.g., archer)")
    parser.add_argument("--level", type=int, default=None,
                        help="Level to generate (1, 2, or 3)")
    args = parser.parse_args()

    if args.all:
        print("Generating all tower upgrade variants...")
        generate_all_upgrades()
    elif args.master:
        print("Generating master upgrade sheet...")
        generate_master_sheet()
    elif args.sheet:
        print(f"Generating upgrade sheet for {args.sheet}...")
        generate_upgrade_sheet(args.sheet)
    elif args.tower and args.level:
        print(f"Generating {args.tower} level {args.level}...")
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        img = generate_upgrade_variant(args.tower, args.level)
        filepath = os.path.join(OUTPUT_DIR, f"tw_{args.tower}_l{args.level}_v01.png")
        img.save(filepath)
        print(f"Saved: {filepath}")
    else:
        # Default: generate everything
        print("Generating all tower upgrade variants...")
        generate_all_upgrades()
        print("\nGenerating master upgrade sheet...")
        generate_master_sheet()
        print("\nGenerating per-tower upgrade sheets...")
        for tt in TOWER_TYPES:
            generate_upgrade_sheet(tt)
