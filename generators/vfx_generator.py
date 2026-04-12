#!/usr/bin/env python3
"""
VFX / Particle Sprite Sheet Generator for Sakartvelo Defenders
Generates 10 sprite sheets (8 frames each, 128x128 per frame) plus a preview grid.
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

# --- Configuration ---
FRAME_SIZE = 128
NUM_FRAMES = 8
SHEET_WIDTH = FRAME_SIZE * NUM_FRAMES  # 1024
SHEET_HEIGHT = FRAME_SIZE  # 128
OUTLINE_COLOR = (26, 26, 26, 255)
GLOW_RADIUS = 6

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "assets", "vfx")
os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)  # Reproducibility


# --- Utility helpers ---

def new_frame():
    """Return a transparent RGBA 128x128 image."""
    return Image.new("RGBA", (FRAME_SIZE, FRAME_SIZE), (0, 0, 0, 0))


def apply_glow(img, color, radius=GLOW_RADIUS, intensity=0.45):
    """Add a soft glow around non-transparent pixels of *img*."""
    mask = img.split()[3]  # alpha channel
    glow_mask = mask.filter(ImageFilter.GaussianBlur(radius))
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            a = glow_mask.getpixel((x, y))
            if a > 4:
                glow.putpixel((x, y), (*color[:3], int(a * intensity)))
    return Image.alpha_composite(img, glow)


def fast_glow(img, color, radius=GLOW_RADIUS, intensity=0.5):
    """Faster glow using solid-layer compositing instead of per-pixel."""
    mask = img.split()[3]
    glow_mask = mask.filter(ImageFilter.GaussianBlur(radius))
    glow_layer = Image.new("RGBA", img.size, (*color[:3], 0))
    glow_layer.putalpha(glow_mask)
    # Scale intensity by creating a dimmed version
    glow_layer = glow_layer.point(lambda p: int(p * intensity) if p > 0 else 0, "RGBA")
    return Image.alpha_composite(img, glow_layer)


def draw_circle(draw, cx, cy, r, color, outline=None, width=1):
    """Draw a filled circle with optional outline."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color, outline=outline, width=width)


def lerp_color(c1, c2, t):
    """Linearly interpolate between two RGBA colors."""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(4))


def ease_out(t):
    return 1 - (1 - t) ** 3


def ease_in(t):
    return t ** 3


def progress(frame):
    """Return 0..1 progress for frame index (0-7)."""
    return frame / (NUM_FRAMES - 1)


# ===================================================================
# EFFECT GENERATORS
# Each returns a list of 8 PIL Image objects (128x128 RGBA).
# ===================================================================

def gen_explosion():
    """Orange/red expanding burst: spark → full explosion → fade."""
    frames = []
    for i in range(NUM_FRAMES):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        t = progress(i)
        cx, cy = 64, 64

        if t < 0.35:
            # Spark phase: small bright core expanding
            p = t / 0.35
            core_r = int(3 + 18 * p)
            outer_r = int(core_r * 2.2)
            alpha_core = int(255)
            alpha_outer = int(180 * p)
            draw_circle(draw, cx, cy, outer_r, (255, 140, 0, alpha_outer))
            draw_circle(draw, cx, cy, core_r, (255, 240, 100, alpha_core))
            # Sparks
            for _ in range(int(4 * p)):
                angle = random.uniform(0, 2 * math.pi)
                dist = random.uniform(core_r, outer_r * 1.3)
                sx = cx + int(dist * math.cos(angle))
                sy = cy + int(dist * math.sin(angle))
                sr = random.randint(1, 3)
                draw_circle(draw, sx, sy, sr, (255, 255, 150, int(220 * p)))
        elif t < 0.7:
            # Full explosion
            p = (t - 0.35) / 0.35
            max_r = int(38 + 8 * math.sin(p * math.pi))
            for layer in range(5, 0, -1):
                r = int(max_r * layer / 5)
                a = int(200 - layer * 30)
                c = lerp_color((255, 60, 0, a), (255, 200, 50, a), layer / 5)
                draw_circle(draw, cx, cy, r, c)
            # Bright center
            draw_circle(draw, cx, cy, int(12 - 4 * p), (255, 255, 200, int(255 - 80 * p)))
            # Debris / sparks
            for _ in range(14):
                angle = random.uniform(0, 2 * math.pi)
                dist = max_r * random.uniform(0.6, 1.4)
                sx = cx + int(dist * math.cos(angle))
                sy = cy + int(dist * math.sin(angle))
                sr = random.randint(1, 3)
                draw_circle(draw, sx, sy, sr, (255, random.randint(100, 200), 0, int(200 * (1 - p * 0.5))))
        else:
            # Fade
            p = (t - 0.7) / 0.3
            max_r = int(42 + 10 * p)
            for layer in range(4, 0, -1):
                r = int(max_r * layer / 4)
                a = int((160 - layer * 35) * (1 - p))
                c = lerp_color((180, 40, 0, a), (100, 20, 0, a), layer / 4)
                draw_circle(draw, cx, cy, r, c)
            # Smoke wisps
            for _ in range(6):
                angle = random.uniform(0, 2 * math.pi)
                dist = random.uniform(15, max_r * 0.8)
                sx = cx + int(dist * math.cos(angle))
                sy = cy + int(dist * math.sin(angle)) - int(5 * p)
                sr = random.randint(2, 5)
                draw_circle(draw, sx, sy, sr, (80, 80, 80, int(60 * (1 - p))))

        frames.append(fast_glow(img, (255, 160, 0), radius=8, intensity=0.35))
    return frames


def gen_fire():
    """Flame effect: small → full flame → small flicker."""
    frames = []
    for i in range(NUM_FRAMES):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        t = progress(i)
        cx, cy = 64, 68  # slightly below center

        # Flame envelope size
        if t < 0.5:
            env = 0.4 + 0.6 * ease_out(t / 0.5)
        else:
            env = 1.0 - 0.3 * math.sin((t - 0.5) / 0.5 * math.pi * 2)

        flame_h = int(40 * env)
        flame_w = int(22 * env)

        # Draw flame layers (bottom to top, dark to bright)
        layers = [
            (flame_h, flame_w, (180, 30, 0, 120)),
            (int(flame_h * 0.85), int(flame_w * 0.8), (220, 80, 0, 160)),
            (int(flame_h * 0.7), int(flame_w * 0.6), (255, 160, 0, 200)),
            (int(flame_h * 0.5), int(flame_w * 0.4), (255, 220, 50, 230)),
            (int(flame_h * 0.25), int(flame_w * 0.2), (255, 255, 180, 255)),
        ]

        for lh, lw, lc in layers:
            # Flame as upward-pointing ellipse-ish shape
            flicker_x = random.randint(-3, 3)
            flicker_h = random.randint(-3, 3)
            top = cy - lh + flicker_h
            left = cx - lw + flicker_x
            right = cx + lw + flicker_x
            draw.polygon([
                (cx, top),
                (left, cy),
                (cx - lw + 4, cy - int(lh * 0.3)),
                (cx, cy),
                (cx + lw - 4, cy - int(lh * 0.3)),
                (right, cy),
            ], fill=lc)

        # Embers
        for _ in range(int(3 * env)):
            ex = cx + random.randint(-flame_w, flame_w)
            ey = cy - random.randint(0, flame_h)
            er = random.randint(1, 2)
            ea = random.randint(100, 220)
            draw_circle(draw, ex, ey, er, (255, 200, 50, ea))

        frames.append(fast_glow(img, (255, 120, 0), radius=7, intensity=0.3))
    return frames


def gen_frost():
    """Ice/blue crystalline: crystal form → full frost → shatter."""
    frames = []
    for i in range(NUM_FRAMES):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        t = progress(i)
        cx, cy = 64, 64

        if t < 0.4:
            # Crystal forming
            p = t / 0.4
            n_arms = 6
            max_len = int(45 * ease_out(p))
            for a_idx in range(n_arms):
                angle = a_idx * math.pi / 3 - math.pi / 2
                ex = cx + int(max_len * math.cos(angle))
                ey = cy + int(max_len * math.sin(angle))
                alpha = int(255 * p)
                draw.line([(cx, cy), (ex, ey)], fill=(140, 200, 255, alpha), width=2)
                # Branch
                if max_len > 15:
                    for b in range(1, 3):
                        bx = cx + int(max_len * b / 3 * math.cos(angle))
                        by = cy + int(max_len * b / 3 * math.sin(angle))
                        for sign in (-1, 1):
                            bangle = angle + sign * math.pi / 4
                            bex = bx + int(max_len * 0.25 * math.cos(bangle))
                            bey = by + int(max_len * 0.25 * math.sin(bangle))
                            draw.line([(bx, by), (bex, bey)], fill=(160, 220, 255, int(alpha * 0.7)), width=1)
            # Center crystal
            draw_circle(draw, cx, cy, int(6 * p), (200, 230, 255, int(200 * p)))
        elif t < 0.7:
            # Full frost - pulsing crystalline
            p = (t - 0.4) / 0.3
            pulse = 1.0 + 0.08 * math.sin(p * math.pi * 3)
            n_arms = 6
            max_len = int(45 * pulse)
            for a_idx in range(n_arms):
                angle = a_idx * math.pi / 3 - math.pi / 2
                ex = cx + int(max_len * math.cos(angle))
                ey = cy + int(max_len * math.sin(angle))
                draw.line([(cx, cy), (ex, ey)], fill=(140, 200, 255, 255), width=2)
                for b in range(1, 4):
                    bx = cx + int(max_len * b / 4 * math.cos(angle))
                    by = cy + int(max_len * b / 4 * math.sin(angle))
                    for sign in (-1, 1):
                        bangle = angle + sign * math.pi / 4
                        bex = bx + int(max_len * 0.3 * math.cos(bangle))
                        bey = by + int(max_len * 0.3 * math.sin(bangle))
                        draw.line([(bx, by), (bex, bey)], fill=(170, 225, 255, 200), width=1)
            # Outer halo
            draw_circle(draw, cx, cy, int(48 * pulse), (100, 180, 255, 30))
            draw_circle(draw, cx, cy, 7, (210, 235, 255, 240))
            # Sparkle particles
            for _ in range(8):
                sa = random.uniform(0, 2 * math.pi)
                sd = random.uniform(10, max_len)
                sx = cx + int(sd * math.cos(sa))
                sy = cy + int(sd * math.sin(sa))
                draw_circle(draw, sx, sy, 1, (220, 240, 255, random.randint(120, 255)))
        else:
            # Shatter
            p = (t - 0.7) / 0.3
            # Fading crystal at center
            alpha_c = int(255 * (1 - p))
            n_arms = 6
            max_len = int(45 * (1 - p * 0.5))
            for a_idx in range(n_arms):
                angle = a_idx * math.pi / 3 - math.pi / 2
                ex = cx + int(max_len * math.cos(angle))
                ey = cy + int(max_len * math.sin(angle))
                draw.line([(cx, cy), (ex, ey)], fill=(140, 200, 255, alpha_c), width=2)
            draw_circle(draw, cx, cy, int(7 * (1 - p)), (210, 235, 255, alpha_c))
            # Shards flying outward
            for _ in range(12):
                sa = random.uniform(0, 2 * math.pi)
                sd = 10 + int(50 * p)
                sx = cx + int(sd * math.cos(sa))
                sy = cy + int(sd * math.sin(sa))
                shard_size = random.randint(2, 5)
                sa2 = random.randint(int(alpha_c * 0.6), alpha_c)
                draw.polygon([
                    (sx, sy - shard_size),
                    (sx + shard_size, sy),
                    (sx, sy + shard_size),
                    (sx - shard_size, sy),
                ], fill=(180, 220, 255, sa2))

        frames.append(fast_glow(img, (120, 180, 255), radius=7, intensity=0.35))
    return frames


def gen_gold_sparkle():
    """Gold coin sparkle: single spark → burst → fade."""
    frames = []
    for i in range(NUM_FRAMES):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        t = progress(i)
        cx, cy = 64, 64

        if t < 0.3:
            # Single spark appearing
            p = t / 0.3
            r = int(4 + 6 * p)
            draw_circle(draw, cx, cy, r, (255, 215, 0, int(200 * p)))
            draw_circle(draw, cx, cy, int(r * 0.5), (255, 255, 180, int(255 * p)))
            # Cross sparkle
            slen = int(10 * p)
            draw.line([(cx - slen, cy), (cx + slen, cy)], fill=(255, 235, 100, int(180 * p)), width=2)
            draw.line([(cx, cy - slen), (cx, cy + slen)], fill=(255, 235, 100, int(180 * p)), width=2)
        elif t < 0.65:
            # Burst phase
            p = (t - 0.3) / 0.35
            n_particles = int(20 * ease_out(p))
            for _ in range(n_particles):
                angle = random.uniform(0, 2 * math.pi)
                dist = random.uniform(5, 40 * p)
                sx = cx + int(dist * math.cos(angle))
                sy = cy + int(dist * math.sin(angle))
                sr = random.randint(1, 3)
                alpha = int(255 * (1 - p * 0.3))
                c = random.choice([
                    (255, 215, 0, alpha),
                    (255, 235, 80, alpha),
                    (255, 255, 180, alpha),
                ])
                draw_circle(draw, sx, sy, sr, c)
            # Center bright
            draw_circle(draw, cx, cy, int(8 - 3 * p), (255, 255, 200, int(255 - 100 * p)))
            # Star rays
            for a in range(4):
                angle = a * math.pi / 2 + p * 0.3
                rlen = int(30 * (1 - p * 0.5))
                ex = cx + int(rlen * math.cos(angle))
                ey = cy + int(rlen * math.sin(angle))
                draw.line([(cx, cy), (ex, ey)], fill=(255, 230, 100, int(150 * (1 - p))), width=1)
        else:
            # Fade
            p = (t - 0.65) / 0.35
            for _ in range(int(15 * (1 - p))):
                angle = random.uniform(0, 2 * math.pi)
                dist = random.uniform(10, 50)
                sx = cx + int(dist * math.cos(angle))
                sy = cy + int(dist * math.sin(angle)) - int(5 * p)
                sr = random.randint(1, 2)
                alpha = int(200 * (1 - p))
                draw_circle(draw, sx, sy, sr, (255, 215, 0, alpha))
            draw_circle(draw, cx, cy, int(4 * (1 - p)), (255, 255, 200, int(180 * (1 - p))))

        frames.append(fast_glow(img, (255, 200, 0), radius=8, intensity=0.4))
    return frames


def gen_shield():
    """Blue force field: appear → pulse → fade."""
    frames = []
    for i in range(NUM_FRAMES):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        t = progress(i)
        cx, cy = 64, 64

        if t < 0.3:
            # Appear
            p = t / 0.3
            r = int(40 * ease_out(p))
            alpha = int(120 * p)
            # Outer ring
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(80, 160, 255, alpha), width=3)
            # Inner fill
            ir = max(1, r - 3)
            draw.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], fill=(40, 100, 200, int(alpha * 0.3)))
            # Bright edge
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(140, 200, 255, int(alpha * 0.7)), width=1)
        elif t < 0.75:
            # Pulse
            p = (t - 0.3) / 0.45
            pulse = 1.0 + 0.06 * math.sin(p * math.pi * 4)
            r = int(40 * pulse)
            base_alpha = 140
            # Hexagonal shield shape
            points = []
            for s in range(6):
                angle = s * math.pi / 3 - math.pi / 6
                px = cx + int(r * math.cos(angle))
                py = cy + int(r * math.sin(angle))
                points.append((px, py))
            draw.polygon(points, fill=(30, 80, 180, int(base_alpha * 0.35)), outline=(80, 160, 255, base_alpha))
            # Inner hexagon
            inner_r = int(r * 0.6)
            inner_pts = []
            for s in range(6):
                angle = s * math.pi / 3
                px = cx + int(inner_r * math.cos(angle))
                py = cy + int(inner_r * math.sin(angle))
                inner_pts.append((px, py))
            draw.polygon(inner_pts, outline=(120, 190, 255, int(base_alpha * 0.5)))
            # Energy particles on edge
            for _ in range(6):
                angle = random.uniform(0, 2 * math.pi)
                px = cx + int(r * math.cos(angle))
                py = cy + int(r * math.sin(angle))
                draw_circle(draw, px, py, 2, (160, 210, 255, 200))
        else:
            # Fade
            p = (t - 0.75) / 0.25
            r = int(40 * (1 + 0.1 * p))
            alpha = int(140 * (1 - p))
            points = []
            for s in range(6):
                angle = s * math.pi / 3 - math.pi / 6
                px = cx + int(r * math.cos(angle))
                py = cy + int(r * math.sin(angle))
                points.append((px, py))
            draw.polygon(points, fill=(30, 80, 180, int(alpha * 0.35)), outline=(80, 160, 255, alpha))

        frames.append(fast_glow(img, (60, 140, 255), radius=6, intensity=0.3))
    return frames


def gen_poison():
    """Green toxic cloud: small → full cloud → dissipate."""
    frames = []
    for i in range(NUM_FRAMES):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        t = progress(i)
        cx, cy = 64, 64

        if t < 0.45:
            # Grow
            p = t / 0.45
            max_r = int(35 * ease_out(p))
            # Multiple overlapping circles for cloud shape
            offsets = [(0, 0), (-12, -5), (10, -8), (-8, 8), (12, 5), (0, -14)]
            for ox, oy in offsets:
                r = int(max_r * random.uniform(0.4, 0.7))
                alpha = int(100 * p)
                draw_circle(draw, cx + int(ox * p), cy + int(oy * p), r, (50, 160, 30, alpha))
            # Darker core
            draw_circle(draw, cx, cy, int(max_r * 0.4), (30, 120, 20, int(130 * p)))
            # Bubbles
            for _ in range(int(5 * p)):
                bx = cx + random.randint(-max_r, max_r)
                by = cy + random.randint(-max_r, max_r)
                br = random.randint(2, 5)
                draw_circle(draw, bx, by, br, (100, 220, 60, int(80 * p)))
        elif t < 0.7:
            # Full cloud
            p = (t - 0.45) / 0.25
            max_r = 35
            offsets = [(0, 0), (-12, -5), (10, -8), (-8, 8), (12, 5), (0, -14), (-5, -10), (7, 10)]
            for ox, oy in offsets:
                r = int(max_r * random.uniform(0.35, 0.65))
                draw_circle(draw, cx + ox, cy + oy, r, (50, 160, 30, 100))
            draw_circle(draw, cx, cy, 14, (30, 120, 20, 130))
            # Bubbles rising
            for _ in range(6):
                bx = cx + random.randint(-25, 25)
                by = cy + random.randint(-25, 25) - int(8 * p)
                br = random.randint(2, 5)
                draw_circle(draw, bx, by, br, (100, 220, 60, 90))
            # Toxic drips
            for _ in range(3):
                dx = cx + random.randint(-15, 15)
                dy = cy + random.randint(10, 25) + int(5 * p)
                draw_circle(draw, dx, dy, random.randint(2, 4), (80, 180, 40, 110))
        else:
            # Dissipate
            p = (t - 0.7) / 0.3
            max_r = int(35 + 15 * p)
            alpha = int(100 * (1 - p))
            offsets = [(0, 0), (-12, -5), (10, -8), (-8, 8), (12, 5)]
            for ox, oy in offsets:
                r = int(max_r * random.uniform(0.3, 0.55))
                draw_circle(draw, cx + int(ox * (1 + p * 0.5)), cy + int(oy * (1 + p * 0.5)), r, (50, 160, 30, alpha))
            # Fading particles upward
            for _ in range(8):
                px = cx + random.randint(-30, 30)
                py = cy - random.randint(0, int(30 * p))
                pr = random.randint(1, 3)
                draw_circle(draw, px, py, pr, (80, 200, 50, int(80 * (1 - p))))

        frames.append(fast_glow(img, (40, 160, 20), radius=5, intensity=0.2))
    return frames


def gen_arrow_volley():
    """Multiple arrow trails: launch → arc → impact."""
    frames = []
    # Pre-generate arrow paths
    arrows = []
    for _ in range(7):
        start_x = random.randint(5, 25)
        start_y = random.randint(85, 105)
        end_x = random.randint(90, 120)
        end_y = random.randint(15, 45)
        mid_y = random.randint(-10, 20)
        arrows.append((start_x, start_y, end_x, end_y, mid_y))

    for i in range(NUM_FRAMES):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        t = progress(i)

        for sx, sy, ex, ey, my in arrows:
            # Quadratic bezier: launch → peak → impact
            if t < 0.15:
                p = t / 0.15
                # Arrow at start
                ax = sx
                ay = sy - int(5 * p)
                # Trail
                trail_len = int(8 * p)
                draw.line([(ax, ay), (ax - trail_len, ay + trail_len // 2)], fill=(139, 90, 43, int(200 * p)), width=2)
                # Arrowhead
                draw.polygon([(ax, ay - 3), (ax - 2, ay + 1), (ax + 2, ay + 1)], fill=(200, 200, 200, int(200 * p)))
            elif t < 0.85:
                p = (t - 0.15) / 0.7
                # Position along arc
                # Quadratic bezier
                ctrl_x = (sx + ex) / 2
                ctrl_y = my
                ax = int((1 - p) ** 2 * sx + 2 * (1 - p) * p * ctrl_x + p ** 2 * ex)
                ay = int((1 - p) ** 2 * sy + 2 * (1 - p) * p * ctrl_y + p ** 2 * ey)
                # Direction for rotation
                dx = 2 * (1 - p) * (ctrl_x - sx) + 2 * p * (ex - ctrl_x)
                dy = 2 * (1 - p) * (ctrl_y - sy) + 2 * p * (ey - ctrl_y)
                length = max(1, math.sqrt(dx * dx + dy * dy))
                ndx, ndy = dx / length, dy / length
                # Trail
                trail_len = 12
                tx = ax - int(ndx * trail_len)
                ty = ay - int(ndy * trail_len)
                draw.line([(ax, ay), (tx, ty)], fill=(139, 90, 43, 200), width=2)
                # Motion blur trail
                tx2 = ax - int(ndx * trail_len * 2)
                ty2 = ay - int(ndy * trail_len * 2)
                draw.line([(tx, ty), (tx2, ty2)], fill=(139, 90, 43, 60), width=1)
                # Arrowhead
                perp_x, perp_y = -ndy, ndx
                head_size = 3
                tip_x, tip_y = ax + int(ndx * 4), ay + int(ndy * 4)
                draw.polygon([
                    (tip_x, tip_y),
                    (ax + int(perp_x * head_size), ay + int(perp_y * head_size)),
                    (ax - int(perp_x * head_size), ay - int(perp_y * head_size)),
                ], fill=(200, 200, 200, 220))
            else:
                # Impact
                p = (t - 0.85) / 0.15
                # Impact flash
                impact_r = int(8 * p)
                alpha = int(200 * (1 - p))
                draw_circle(draw, ex, ey, impact_r, (255, 200, 100, alpha))
                draw_circle(draw, ex, ey, max(1, impact_r // 2), (255, 255, 200, int(alpha * 0.8)))
                # Arrow stuck
                draw.line([(ex, ey), (ex - 8, ey + 8)], fill=(139, 90, 43, int(150 * (1 - p))), width=2)
                # Debris
                for _ in range(3):
                    da = random.uniform(0, 2 * math.pi)
                    dd = random.uniform(2, impact_r * 1.5)
                    dpx = ex + int(dd * math.cos(da))
                    dpy = ey + int(dd * math.sin(da))
                    draw_circle(draw, dpx, dpy, 1, (180, 160, 100, alpha))

        frames.append(fast_glow(img, (255, 200, 100), radius=4, intensity=0.2))
    return frames


def gen_cannon_smoke():
    """Gray smoke puff: small → full smoke → dissipate."""
    frames = []
    for i in range(NUM_FRAMES):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        t = progress(i)
        cx, cy = 64, 64

        if t < 0.4:
            # Grow
            p = t / 0.4
            max_r = int(30 * ease_out(p))
            alpha = int(160 * p)
            # Layered smoke puffs
            puffs = [(0, 0), (-10, -3), (8, -6), (-6, 7), (11, 4), (0, -12)]
            for ox, oy in puffs:
                r = int(max_r * random.uniform(0.4, 0.75))
                c_val = random.randint(80, 140)
                draw_circle(draw, cx + int(ox * p), cy + int(oy * p), r, (c_val, c_val, c_val, int(alpha * 0.7)))
            # Dense core
            draw_circle(draw, cx, cy, int(max_r * 0.45), (60, 60, 60, int(alpha * 0.8)))
        elif t < 0.7:
            # Full smoke - billowing
            p = (t - 0.4) / 0.3
            max_r = 30
            alpha = 160
            drift = int(5 * p)
            puffs = [(0, 0), (-12, -3), (9, -7), (-7, 8), (12, 4), (0, -13), (-4, -9), (6, 11)]
            for ox, oy in puffs:
                r = int(max_r * random.uniform(0.35, 0.7))
                c_val = random.randint(70, 130)
                draw_circle(draw, cx + ox + drift, cy + oy - int(3 * p), r, (c_val, c_val, c_val, int(alpha * 0.65)))
            draw_circle(draw, cx + drift, cy - int(3 * p), 13, (50, 50, 50, int(alpha * 0.6)))
        else:
            # Dissipate
            p = (t - 0.7) / 0.3
            max_r = int(30 + 20 * p)
            alpha = int(160 * (1 - p))
            drift = int(5 + 8 * p)
            rise = int(8 * p)
            puffs = [(0, 0), (-10, -3), (8, -6), (-6, 7), (11, 4)]
            for ox, oy in puffs:
                r = int(max_r * random.uniform(0.3, 0.6))
                c_val = random.randint(80, 140)
                draw_circle(draw, cx + int(ox * (1 + p * 0.3)) + drift, cy + int(oy * (1 + p * 0.3)) - rise, r, (c_val, c_val, c_val, int(alpha * 0.6)))

        frames.append(img)  # No glow for smoke
    return frames


def gen_lightning():
    """Electric bolt: appear → zigzag → flash → fade."""
    frames = []
    for i in range(NUM_FRAMES):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        t = progress(i)
        cx, cy = 64, 64

        def zigzag(start_x, start_y, end_x, end_y, segments=6, jitter=18, width=2, color=(180, 200, 255, 255)):
            points = [(start_x, start_y)]
            for s in range(1, segments):
                sx = start_x + (end_x - start_x) * s / segments + random.randint(-jitter, jitter)
                sy = start_y + (end_y - start_y) * s / segments + random.randint(-jitter, jitter)
                points.append((sx, sy))
            points.append((end_x, end_y))
            for s in range(len(points) - 1):
                draw.line([points[s], points[s + 1]], fill=color, width=width)
            return points

        if t < 0.25:
            # Appear - bolt materializes
            p = t / 0.25
            alpha = int(255 * p)
            zigzag(cx, 10, cx + random.randint(-10, 10), cy + 30, segments=5, jitter=15, width=3, color=(180, 200, 255, alpha))
            zigzag(cx + random.randint(-5, 5), 10, cx - 15 + random.randint(-10, 10), cy + 20, segments=4, jitter=12, width=1, color=(120, 160, 255, int(alpha * 0.6)))
            # Flash at origin
            draw_circle(draw, cx, 10, int(8 * p), (220, 230, 255, int(150 * p)))
        elif t < 0.5:
            # Full zigzag
            p = (t - 0.25) / 0.25
            # Main bolt
            zigzag(cx, 10, cx + random.randint(-15, 15), cy + 35, segments=7, jitter=20, width=3, color=(200, 210, 255, 255))
            # Branches
            zigzag(cx - 5, 30, cx - 25, cy + 15, segments=3, jitter=10, width=2, color=(160, 180, 255, 200))
            zigzag(cx + 8, 40, cx + 30, cy + 30, segments=3, jitter=10, width=2, color=(160, 180, 255, 180))
            zigzag(cx, 50, cx - 10, cy + 40, segments=2, jitter=8, width=1, color=(140, 170, 255, 150))
            # Impact flash
            draw_circle(draw, cx, cy + 35, 12, (200, 220, 255, int(200 * (1 - p * 0.5))))
            draw_circle(draw, cx, cy + 35, 5, (255, 255, 255, 255))
        elif t < 0.75:
            # Flash
            p = (t - 0.5) / 0.25
            # Screen flash
            flash_alpha = int(100 * math.sin(p * math.pi))
            draw.rectangle([0, 0, FRAME_SIZE, FRAME_SIZE], fill=(200, 210, 255, flash_alpha))
            # Bright bolt silhouette
            zigzag(cx, 10, cx + 5, cy + 35, segments=6, jitter=8, width=2, color=(240, 245, 255, int(255 * (1 - p * 0.5))))
            # Impact glow
            draw_circle(draw, cx, cy + 35, int(15 + 5 * p), (180, 200, 255, int(120 * (1 - p))))
        else:
            # Fade
            p = (t - 0.75) / 0.25
            alpha = int(200 * (1 - p))
            zigzag(cx, 10, cx, cy + 35, segments=5, jitter=5, width=2, color=(160, 180, 255, alpha))
            # Residual sparks
            for _ in range(8):
                sx = cx + random.randint(-20, 20)
                sy = random.randint(10, cy + 40)
                draw_circle(draw, sx, sy, 1, (200, 210, 255, int(alpha * 0.5)))

        frames.append(fast_glow(img, (150, 180, 255), radius=8, intensity=0.5))
    return frames


def gen_heal():
    """Green cross/rays: appear → pulse → fade."""
    frames = []
    for i in range(NUM_FRAMES):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        t = progress(i)
        cx, cy = 64, 64

        if t < 0.3:
            # Appear
            p = t / 0.3
            alpha = int(220 * p)
            cross_size = int(18 * ease_out(p))
            cross_w = int(6 * p)
            # Vertical bar
            draw.rectangle([cx - cross_w // 2, cy - cross_size, cx + cross_w // 2, cy + cross_size], fill=(50, 200, 80, alpha))
            # Horizontal bar
            draw.rectangle([cx - cross_size, cy - cross_w // 2, cx + cross_size, cy + cross_w // 2], fill=(50, 200, 80, alpha))
            # Bright center
            draw_circle(draw, cx, cy, int(5 * p), (150, 255, 150, int(200 * p)))
        elif t < 0.7:
            # Pulse
            p = (t - 0.3) / 0.4
            pulse = 1.0 + 0.1 * math.sin(p * math.pi * 3)
            cross_size = int(18 * pulse)
            cross_w = 6
            alpha = 220
            # Glow ring
            ring_r = int(25 + 10 * p)
            draw.ellipse([cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r], outline=(80, 220, 100, int(100 * (1 - p * 0.3))), width=2)
            # Rays
            n_rays = 8
            for r_idx in range(n_rays):
                angle = r_idx * 2 * math.pi / n_rays + p * 0.5
                inner_r = int(cross_size + 5)
                outer_r = int(inner_r + 12 + 5 * math.sin(p * math.pi * 2 + r_idx))
                x1 = cx + int(inner_r * math.cos(angle))
                y1 = cy + int(inner_r * math.sin(angle))
                x2 = cx + int(outer_r * math.cos(angle))
                y2 = cy + int(outer_r * math.sin(angle))
                draw.line([(x1, y1), (x2, y2)], fill=(100, 230, 120, int(180 * (1 - p * 0.3))), width=1)
            # Cross
            draw.rectangle([cx - cross_w // 2, cy - cross_size, cx + cross_w // 2, cy + cross_size], fill=(50, 200, 80, alpha))
            draw.rectangle([cx - cross_size, cy - cross_w // 2, cx + cross_size, cy + cross_w // 2], fill=(50, 200, 80, alpha))
            # Bright center
            draw_circle(draw, cx, cy, 5, (180, 255, 180, 230))
            # Rising particles
            for _ in range(int(6 * p)):
                px = cx + random.randint(-cross_size, cross_size)
                py = cy - random.randint(cross_size, cross_size + int(20 * p))
                draw_circle(draw, px, py, random.randint(1, 2), (120, 255, 140, random.randint(100, 200)))
        else:
            # Fade
            p = (t - 0.7) / 0.3
            alpha = int(220 * (1 - p))
            cross_size = int(18 * (1 - p * 0.3))
            cross_w = max(1, int(6 * (1 - p)))
            draw.rectangle([cx - cross_w // 2, cy - cross_size, cx + cross_w // 2, cy + cross_size], fill=(50, 200, 80, alpha))
            draw.rectangle([cx - cross_size, cy - cross_w // 2, cx + cross_size, cy + cross_w // 2], fill=(50, 200, 80, alpha))
            draw_circle(draw, cx, cy, max(1, int(5 * (1 - p))), (180, 255, 180, int(230 * (1 - p))))
            # Rising particles fading
            for _ in range(8):
                px = cx + random.randint(-20, 20)
                py = cy - random.randint(15, 45) - int(10 * p)
                draw_circle(draw, px, py, 1, (120, 255, 140, int(150 * (1 - p))))

        frames.append(fast_glow(img, (50, 200, 80), radius=7, intensity=0.35))
    return frames


# ===================================================================
# SHEET & PREVIEW GENERATION
# ===================================================================

EFFECTS = {
    "explosion": gen_explosion,
    "fire": gen_fire,
    "frost": gen_frost,
    "gold_sparkle": gen_gold_sparkle,
    "shield": gen_shield,
    "poison": gen_poison,
    "arrow_volley": gen_arrow_volley,
    "cannon_smoke": gen_cannon_smoke,
    "lightning": gen_lightning,
    "heal": gen_heal,
}

# Pick a representative frame index for the preview (typically frame 3 or 4 = peak)
PREVIEW_FRAME = 4


def build_sheet(frames):
    """Compose 8 frames into a 1024x128 horizontal strip."""
    sheet = Image.new("RGBA", (SHEET_WIDTH, SHEET_HEIGHT), (0, 0, 0, 0))
    for i, frame in enumerate(frames):
        sheet.paste(frame, (i * FRAME_SIZE, 0))
    return sheet


def build_preview(all_frames):
    """2x5 grid of representative frames, 512x512."""
    cell = 256  # each cell is 256x256 in the preview
    preview = Image.new("RGBA", (512, 512), (20, 20, 30, 255))
    draw = ImageDraw.Draw(preview)
    items = list(all_frames.items())
    for idx, (name, frames) in enumerate(items):
        col = idx % 5
        row = idx // 5
        x = col * cell
        y = row * cell
        # Dark background cell
        draw.rectangle([x, y, x + cell - 2, y + cell - 2], fill=(30, 30, 40, 255))
        # Scale frame up to fill cell
        frame = frames[PREVIEW_FRAME]
        frame_scaled = frame.resize((cell - 4, cell - 4), Image.LANCZOS)
        preview.paste(frame_scaled, (x + 2, y + 2), frame_scaled)
        # Label
        try:
            label = name.replace("_", " ").title()
            draw.text((x + 4, y + cell - 18), label, fill=(220, 220, 220, 220))
        except Exception:
            pass
    return preview


def main():
    print(f"Output directory: {OUTPUT_DIR}")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_frames = {}
    for name, gen_func in EFFECTS.items():
        print(f"Generating {name}...", end=" ", flush=True)
        frames = gen_func()
        sheet = build_sheet(frames)
        path = os.path.join(OUTPUT_DIR, f"{name}.png")
        sheet.save(path)
        all_frames[name] = frames
        print(f"saved {path} ({sheet.size[0]}x{sheet.size[1]})")

    # Preview grid
    print("Generating vfx_preview.png...", end=" ", flush=True)
    preview = build_preview(all_frames)
    preview_path = os.path.join(OUTPUT_DIR, "vfx_preview.png")
    preview.save(preview_path)
    print(f"saved {preview_path} ({preview.size[0]}x{preview.size[1]})")

    print("\nDone! All VFX sprite sheets generated.")


if __name__ == "__main__":
    main()
