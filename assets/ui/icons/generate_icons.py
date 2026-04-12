#!/usr/bin/env python3
"""Generate all 33 SVG icon files for Sakartvelo Defenders UI."""

import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Style constants
VB = "0 0 64 64"
STROKE = "#1A1A1A"
SW = "2"
FILL_NONE = "none"
GOLD = "#D4A017"
DANGER = "#E74C3C"
SUCCESS = "#27AE60"
INFO_BLUE = "#3498DB"
BASE = "#2D5A3D"
HIGHLIGHT = "#4CAF50"
SHADOW = "#1B3A26"
SKY = "#87CEEB"
WHITE = "#FFFFFF"
LIGHT_GOLD = "#F0D060"
PURPLE = "#9B59B6"
GRAY = "#95A5A6"
DARK_GRAY = "#7F8C8D"
LIGHT_GRAY = "#BDC3C7"
ORANGE = "#F39C12"
TEAL = "#1ABC9C"


def svg(inner: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}" '
        f'width="64" height="64" fill="none">\n{inner}\n</svg>'
    )


def path(d: str, fill: str = FILL_NONE, stroke: str = STROKE, sw: str = SW) -> str:
    return f'  <path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'


def circle(cx, cy, r, fill: str = FILL_NONE, stroke: str = STROKE, sw: str = SW) -> str:
    return f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def line(x1, y1, x2, y2, stroke: str = STROKE, sw: str = SW) -> str:
    return f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"/>'


def rect(x, y, w, h, fill: str = FILL_NONE, stroke: str = STROKE, sw: str = SW, rx: str = "2") -> str:
    return f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def polygon(points: str, fill: str = FILL_NONE, stroke: str = STROKE, sw: str = SW) -> str:
    return f'  <polygon points="{points}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'


def write(name: str, content: str):
    path_out = os.path.join(OUTPUT_DIR, name)
    with open(path_out, "w") as f:
        f.write(content)
    print(f"  Created {name}")


# ============================================================
# TOWER ICONS (10)
# ============================================================

def make_archer():
    """Bow tower - isometric tower with arrow."""
    inner = (
        # Tower body (isometric rectangle)
        path("M32 8 L22 16 L22 52 L32 60 L42 52 L42 16 Z", fill=BASE)
        + path("M22 16 L32 24 L42 16", fill=SHADOW)  # dark top face
        + path("M32 24 L32 60", stroke=SHADOW)  # center line
        # Arrow on top
        + line("32", "2", "32", "12", stroke=GOLD)
        + path("M28 6 L32 2 L36 6", fill=GOLD, stroke=GOLD)
        # Battlements
        + rect("18", "13", "4", "5", fill=HIGHLIGHT)
        + rect("42", "13", "4", "5", fill=HIGHLIGHT)
        + rect("28", "5", "8", "4", fill=HIGHLIGHT)
    )
    write("archer.svg", svg(inner))


def make_catapult():
    """Catapult - wooden frame with throwing arm."""
    inner = (
        # Base
        path("M12 54 L20 48 L44 48 L52 54 L44 60 L20 60 Z", fill=BASE)
        # Frame / A-frame support
        + line("20", "48", "32", "24", stroke=HIGHLIGHT)
        + line("44", "48", "32", "24", stroke=HIGHLIGHT)
        # Throwing arm
        + line("18", "32", "50", "16", stroke=GOLD, sw="3")
        # Bucket / sling
        + path("M46 14 L54 10 L54 18 Z", fill=DANGER)
        # Wheels
        + circle("18", "58", "4", fill=DARK_GRAY)
        + circle("46", "58", "4", fill=DARK_GRAY)
    )
    write("catapult.svg", svg(inner))


def make_wall():
    """Stone wall - isometric barrier."""
    inner = (
        # Main wall body
        rect("8", "16", "48", "36", fill=BASE)
        # Brick lines
        + line("8", "28", "56", "28", stroke=SHADOW)
        + line("8", "40", "56", "40", stroke=SHADOW)
        + line("24", "16", "24", "28", stroke=SHADOW)
        + line("40", "16", "40", "28", stroke=SHADOW)
        + line("16", "28", "16", "40", stroke=SHADOW)
        + line("32", "28", "32", "40", stroke=SHADOW)
        + line("48", "28", "48", "40", stroke=SHADOW)
        + line("24", "40", "24", "52", stroke=SHADOW)
        + line("40", "40", "40", "52", stroke=SHADOW)
        # Battlements on top
        + rect("8", "10", "8", "8", fill=HIGHLIGHT)
        + rect("20", "10", "8", "8", fill=HIGHLIGHT)
        + rect("36", "10", "8", "8", fill=HIGHLIGHT)
        + rect("48", "10", "8", "8", fill=HIGHLIGHT)
    )
    write("wall.svg", svg(inner))


def make_shrine():
    """Shrine / temple - dome structure."""
    inner = (
        # Base platform
        path("M10 50 L32 42 L54 50 L32 58 Z", fill=SHADOW)
        # Pillars
        + rect("16", "28", "5", "22", fill=LIGHT_GRAY)
        + rect("43", "28", "5", "22", fill=LIGHT_GRAY)
        # Dome
        + path("M12 30 Q12 10 32 10 Q52 10 52 30 Z", fill=HIGHLIGHT)
        + path("M12 30 L52 30", stroke=SHADOW)
        # Golden ornament on top
        + circle("32", "10", "3", fill=GOLD)
        + circle("32", "10", "1.5", fill=LIGHT_GOLD)
        # Glow lines
        + line("26", "6", "24", "2", stroke=GOLD, sw="1.5")
        + line("38", "6", "40", "2", stroke=GOLD, sw="1.5")
        + line("32", "4", "32", "1", stroke=GOLD, sw="1.5")
    )
    write("shrine.svg", svg(inner))


def make_cavalry():
    """Cavalry tower - horse head on shield."""
    inner = (
        # Shield shape
        path("M32 6 L52 16 L52 38 Q52 54 32 60 Q12 54 12 38 L12 16 Z", fill=BASE)
        # Horse head silhouette (simplified geometric)
        + path("M24 22 L28 18 L36 18 L38 22 L40 20 L42 24 L40 28 L38 32 L36 38 L32 42 L28 38 L26 32 L24 28 Z",
               fill=HIGHLIGHT)
        # Mane lines
        + line("28", "18", "26", "14", stroke=GOLD)
        + line("32", "18", "32", "13", stroke=GOLD)
        + line("36", "18", "38", "14", stroke=GOLD)
        # Eye
        + circle("36", "24", "1.5", fill=STROKE)
    )
    write("cavalry.svg", svg(inner))


def make_gunpowder():
    """Gunpowder tower - cannon."""
    inner = (
        # Tower base (isometric)
        path("M22 20 L32 14 L42 20 L42 50 L32 56 L22 50 Z", fill=BASE)
        # Cannon barrel
        + path("M24 28 L14 24 L14 32 L24 36 Z", fill=DARK_GRAY)
        # Cannon opening
        + circle("14", "28", "5", fill=GRAY)
        + circle("14", "28", "3", fill="#333")
        # Cannon balls stack
        + circle("32", "46", "3", fill=DARK_GRAY)
        + circle("28", "50", "3", fill=DARK_GRAY)
        + circle("36", "50", "3", fill=DARK_GRAY)
        # Fuse spark
        + path("M10 24 L8 20 L6 24", fill=GOLD, stroke=GOLD, sw="1.5")
    )
    write("gunpowder.svg", svg(inner))


def make_industrial():
    """Industrial tower - factory with chimney."""
    inner = (
        # Factory building
        rect("8", "24", "40", "32", fill=BASE)
        # Roof
        + path("M6 24 L28 14 L50 24", fill=HIGHLIGHT)
        # Chimney
        + rect("38", "10", "8", "14", fill=DARK_GRAY)
        # Smoke puffs
        + circle("42", "6", "3", fill=LIGHT_GRAY, stroke=LIGHT_GRAY)
        + circle("46", "4", "2.5", fill=GRAY, stroke=GRAY)
        + circle("39", "3", "2", fill=LIGHT_GRAY, stroke=LIGHT_GRAY)
        # Gear symbol
        + circle("28", "40", "6", fill=GOLD)
        + circle("28", "40", "2.5", fill=BASE)
        # Gear teeth (simplified)
        + line("28", "33", "28", "31", stroke=GOLD, sw="3")
        + line("28", "47", "28", "49", stroke=GOLD, sw="3")
        + line("21", "40", "19", "40", stroke=GOLD, sw="3")
        + line("35", "40", "37", "40", stroke=GOLD, sw="3")
    )
    write("industrial.svg", svg(inner))


def make_bunker():
    """Bunker - reinforced concrete structure."""
    inner = (
        # Main bunker body
        rect("10", "28", "44", "28", fill=DARK_GRAY)
        # Top slab (thicker)
        + rect("6", "24", "52", "8", fill=GRAY)
        # Slit opening
        + rect("22", "28", "20", "4", fill="#333")
        # Reinforcement lines
        + line("10", "40", "54", "40", stroke=STROKE)
        + line("32", "28", "32", "56", stroke=STROKE)
        # Sandbags on sides
        + path("M6 32 Q10 30 14 32 Q18 34 14 36 Q10 34 6 36 Z", fill=HIGHLIGHT)
        + path("M50 32 Q54 30 58 32 Q58 36 54 36 Q50 34 50 32 Z", fill=HIGHLIGHT)
    )
    write("bunker.svg", svg(inner))


def make_tech():
    """Tech tower - futuristic antenna/dish."""
    inner = (
        # Base structure
        rect("20", "36", "24", "24", fill=DARK_GRAY)
        + path("M18 36 L32 28 L46 36", fill=GRAY)
        # Satellite dish
        + path("M20 20 Q32 4 44 20", fill=INFO_BLUE)
        + path("M24 22 Q32 10 40 22", fill=WHITE, stroke=INFO_BLUE)
        # Antenna
        + line("32", "20", "32", "8", stroke=INFO_BLUE, sw="2.5")
        + circle("32", "6", "2.5", fill=INFO_BLUE)
        # Signal waves
        + path("M38 12 Q42 8 38 4", stroke=INFO_BLUE, sw="1.5")
        + path("M42 14 Q48 8 42 2", stroke=INFO_BLUE, sw="1.5")
        # Circuit lines on base
        + line("24", "44", "40", "44", stroke=INFO_BLUE, sw="1")
        + line("28", "48", "36", "48", stroke=INFO_BLUE, sw="1")
        + line("26", "52", "38", "52", stroke=INFO_BLUE, sw="1")
    )
    write("tech.svg", svg(inner))


def make_special():
    """Special tower - star with mystical energy."""
    inner = (
        # Star shape (5-pointed)
        polygon(
            "32,4 38,22 58,22 42,34 48,52 32,42 16,52 22,34 6,22 26,22",
            fill=GOLD, stroke=SHADOW
        )
        # Inner star
        + polygon(
            "32,14 35,24 46,24 38,30 40,40 32,34 24,40 26,30 18,24 29,24",
            fill=LIGHT_GOLD, stroke=GOLD
        )
        # Energy ring
        + circle("32", "30", "22", fill=FILL_NONE, stroke=GOLD, sw="1")
        # Sparkle dots
        + circle("10", "10", "2", fill=GOLD, stroke=GOLD)
        + circle("54", "10", "2", fill=GOLD, stroke=GOLD)
        + circle("32", "60", "2", fill=GOLD, stroke=GOLD)
        + circle("8", "44", "1.5", fill=GOLD, stroke=GOLD)
        + circle("56", "44", "1.5", fill=GOLD, stroke=GOLD)
    )
    write("special.svg", svg(inner))


# ============================================================
# RESOURCE ICONS (3)
# ============================================================

def make_gold():
    """Gold coin with G."""
    inner = (
        # Outer coin
        circle("32", "32", "24", fill=GOLD)
        # Inner ring
        + circle("32", "32", "18", fill=LIGHT_GOLD, stroke=GOLD)
        # Inner circle
        + circle("32", "32", "14", fill=GOLD)
        # G letter (drawn as path)
        + path("M26 22 L38 22 L38 26 L30 26 L30 29 L36 29 L36 33 L30 33 L30 38 L26 38 Z",
               fill=LIGHT_GOLD, stroke=LIGHT_GOLD, sw="1")
        # Shine
        + path("M20 16 L24 14 L22 20 Z", fill=WHITE, stroke=WHITE, sw="1")
    )
    write("gold.svg", svg(inner))


def make_blue_token():
    """Blue crystal token."""
    inner = (
        # Crystal diamond shape
        polygon("32,4 56,24 32,60 8,24", fill=INFO_BLUE)
        # Facet lines
        + line("8", "24", "32", "34", stroke=WHITE, sw="1")
        + line("56", "24", "32", "34", stroke=WHITE, sw="1")
        + line("32", "4", "32", "34", stroke=WHITE, sw="1")
        # Upper facets
        + polygon("32,4 8,24 32,34", fill=INFO_BLUE, stroke=WHITE, sw="0.5")
        + polygon("32,4 56,24 32,34", fill="#5DADE2", stroke=WHITE, sw="0.5")
        # Lower facets
        + polygon("32,34 8,24 32,60", fill="#2E86C1", stroke=WHITE, sw="0.5")
        + polygon("32,34 56,24 32,60", fill="#2471A3", stroke=WHITE, sw="0.5")
        # Shine
        + path("M24 14 L28 12 L26 18 Z", fill=WHITE, stroke=WHITE, sw="1")
    )
    write("blue_token.svg", svg(inner))


def make_heart():
    """Heart / lives icon."""
    inner = (
        # Heart shape
        path(
            "M32 56 L10 34 Q2 24 10 16 Q18 8 32 22 Q46 8 54 16 Q62 24 54 34 Z",
            fill=DANGER
        )
        # Shine
        + path("M18 18 L22 14 L20 22 Z", fill=WHITE, stroke=WHITE, sw="1")
        # Outline for definition
        + path(
            "M32 56 L10 34 Q2 24 10 16 Q18 8 32 22 Q46 8 54 16 Q62 24 54 34 Z",
            stroke="#C0392B"
        )
    )
    write("heart.svg", svg(inner))


# ============================================================
# ABILITY ICONS (4)
# ============================================================

def make_lightning():
    """Lightning bolt - damage ability."""
    inner = (
        # Lightning bolt
        polygon("36,2 18,32 28,32 24,62 46,26 34,26", fill=GOLD, stroke=SHADOW)
        # Inner highlight
        + polygon("34,10 24,30 30,30 28,50 40,28 34,28", fill=LIGHT_GOLD, stroke=LIGHT_GOLD, sw="1")
        # Spark lines
        + line("12", "18", "8", "14", stroke=GOLD, sw="1.5")
        + line("50", "40", "56", "44", stroke=GOLD, sw="1.5")
        + line("14", "44", "8", "48", stroke=GOLD, sw="1.5")
    )
    write("lightning.svg", svg(inner))


def make_shield():
    """Shield - protect ability."""
    inner = (
        # Shield body
        path("M32 6 L54 16 L54 36 Q54 54 32 62 Q10 54 10 36 L10 16 Z",
               fill=INFO_BLUE)
        # Shield cross pattern
        + line("32", "16", "32", "54", stroke=WHITE, sw="3")
        + line("16", "34", "48", "34", stroke=WHITE, sw="3")
        # Border highlight
        + path("M32 10 L50 18 L50 36 Q50 52 32 58 Q14 52 14 36 L14 18 Z",
               fill=FILL_NONE, stroke=WHITE, sw="1")
        # Center gem
        + circle("32", "34", "4", fill=GOLD)
    )
    write("shield.svg", svg(inner))


def make_heal():
    """Heal - cross/plus sign."""
    inner = (
        # Background circle
        circle("32", "32", "28", fill=SUCCESS)
        # Plus / cross
        + rect("26", "14", "12", "36", rx="2", fill=WHITE, stroke=FILL_NONE, sw="0")
        + rect("14", "26", "36", "12", rx="2", fill=WHITE, stroke=FILL_NONE, sw="0")
        # Outline
        + circle("32", "32", "28", stroke="#1E8449")
        # Small sparkle
        + circle("44", "16", "2", fill=WHITE, stroke=WHITE)
        + circle("50", "22", "1.5", fill=WHITE, stroke=WHITE)
    )
    write("heal.svg", svg(inner))


def make_speed():
    """Speed - boost / wings."""
    inner = (
        # Arrow pointing right (speed lines)
        path("M8 32 L48 32 L38 20", fill=FILL_NONE, stroke=GOLD, sw="3")
        + path("M8 32 L48 32 L38 44", fill=FILL_NONE, stroke=GOLD, sw="3")
        # Speed lines behind
        + line("4", "20", "18", "20", stroke=GOLD, sw="2")
        + line("8", "26", "22", "26", stroke=LIGHT_GOLD, sw="1.5")
        + line("8", "38", "22", "38", stroke=LIGHT_GOLD, sw="1.5")
        + line("4", "44", "18", "44", stroke=GOLD, sw="2")
        # Motion trail
        + path("M2 32 L14 32 L10 28 M2 32 L14 32 L10 36", stroke=GOLD, sw="1.5")
    )
    write("speed.svg", svg(inner))


# ============================================================
# UI ICONS (8)
# ============================================================

def make_pause():
    """Pause icon."""
    inner = (
        rect("18", "12", "10", "40", rx="2", fill=LIGHT_GRAY)
        + rect("36", "12", "10", "40", rx="2", fill=LIGHT_GRAY)
    )
    write("pause.svg", svg(inner))


def make_play():
    """Play icon."""
    inner = (
        polygon("16,8 56,32 16,56", fill=LIGHT_GRAY)
    )
    write("play.svg", svg(inner))


def make_settings():
    """Settings / gear icon."""
    inner = (
        # Outer gear (simplified octagonal)
        circle("32", "32", "12", fill=LIGHT_GRAY)
        + circle("32", "32", "6", fill=BASE)
        # Gear teeth
        + rect("28", "2", "8", "8", fill=LIGHT_GRAY)
        + rect("28", "54", "8", "8", fill=LIGHT_GRAY)
        + rect("2", "28", "8", "8", fill=LIGHT_GRAY)
        + rect("54", "28", "8", "8", fill=LIGHT_GRAY)
        # Diagonal teeth
        + rect("48", "6", "8", "8", rx="1", fill=LIGHT_GRAY, stroke=STROKE, sw=SW)
        + rect("8", "50", "8", "8", rx="1", fill=LIGHT_GRAY, stroke=STROKE, sw=SW)
        + rect("6", "6", "8", "8", rx="1", fill=LIGHT_GRAY, stroke=STROKE, sw=SW)
        + rect("50", "50", "8", "8", rx="1", fill=LIGHT_GRAY, stroke=STROKE, sw=SW)
    )
    write("settings.svg", svg(inner))


def make_menu():
    """Menu / hamburger icon."""
    inner = (
        line("12", "18", "52", "18", stroke=LIGHT_GRAY, sw="4")
        + line("12", "32", "52", "32", stroke=LIGHT_GRAY, sw="4")
        + line("12", "46", "52", "46", stroke=LIGHT_GRAY, sw="4")
    )
    write("menu.svg", svg(inner))


def make_info():
    """Info icon - i in circle."""
    inner = (
        circle("32", "32", "26", fill=INFO_BLUE)
        + circle("32", "16", "4", fill=WHITE, stroke=WHITE)
        + rect("28", "24", "8", "24", rx="2", fill=WHITE, stroke=WHITE)
    )
    write("info.svg", svg(inner))


def make_close():
    """Close / X icon."""
    inner = (
        line("16", "16", "48", "48", stroke=LIGHT_GRAY, sw="4")
        + line("48", "16", "16", "48", stroke=LIGHT_GRAY, sw="4")
    )
    write("close.svg", svg(inner))


def make_arrow_left():
    """Left arrow."""
    inner = (
        path("M40 8 L16 32 L40 56", fill=FILL_NONE, stroke=LIGHT_GRAY, sw="4")
        + line("40", "32", "56", "32", stroke=LIGHT_GRAY, sw="4")
    )
    write("arrow_left.svg", svg(inner))


def make_arrow_right():
    """Right arrow."""
    inner = (
        path("M24 8 L48 32 L24 56", fill=FILL_NONE, stroke=LIGHT_GRAY, sw="4")
        + line("8", "32", "24", "32", stroke=LIGHT_GRAY, sw="4")
    )
    write("arrow_right.svg", svg(inner))


# ============================================================
# SCROLL ICONS (4)
# ============================================================

def make_scroll(border_color: str, rarity: str):
    """Scroll with colored rarity border."""
    inner = (
        # Scroll body
        rect("12", "10", "40", "44", rx="4", fill="#F5E6C8")
        # Scroll rolled ends
        + rect("10", "6", "44", "8", rx="4", fill="#D4A574")
        + rect("10", "50", "44", "8", rx="4", fill="#D4A574")
        # Rarity border
        + rect("14", "14", "36", "36", rx="2", fill=FILL_NONE, stroke=border_color, sw="3")
        # Inner decoration lines
        + line("20", "22", "44", "22", stroke=border_color, sw="1")
        + line("20", "28", "44", "28", stroke=border_color, sw="1")
        + line("20", "34", "44", "34", stroke=border_color, sw="1")
        + line("20", "40", "38", "40", stroke=border_color, sw="1")
        # Rarity gem at top
        + circle("32", "6", "4", fill=border_color, stroke=border_color)
        + circle("32", "6", "2", fill=WHITE, stroke=WHITE)
    )
    write(f"scroll_{rarity}.svg", svg(inner))


# ============================================================
# NOTIFICATION ICONS (4)
# ============================================================

def make_success():
    """Success - checkmark."""
    inner = (
        circle("32", "32", "28", fill=SUCCESS)
        + path("M18 32 L28 42 L46 22", fill=FILL_NONE, stroke=WHITE, sw="4")
    )
    write("success.svg", svg(inner))


def make_error():
    """Error - X mark."""
    inner = (
        circle("32", "32", "28", fill=DANGER)
        + line("20", "20", "44", "44", stroke=WHITE, sw="4")
        + line("44", "20", "20", "44", stroke=WHITE, sw="4")
    )
    write("error.svg", svg(inner))


def make_warning():
    """Warning - exclamation mark."""
    inner = (
        path("M32 6 L58 54 L6 54 Z", fill=ORANGE)
        + line("32", "22", "32", "38", stroke=WHITE, sw="4")
        + circle("32", "46", "3", fill=WHITE, stroke=WHITE)
    )
    write("warning.svg", svg(inner))


def make_info_circle():
    """Info circle - i."""
    inner = (
        circle("32", "32", "28", fill=INFO_BLUE)
        + circle("32", "18", "4", fill=WHITE, stroke=WHITE)
        + rect("28", "26", "8", "22", rx="3", fill=WHITE, stroke=WHITE)
    )
    write("info_circle.svg", svg(inner))


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("Generating SVG icons for Sakartvelo Defenders...")
    print(f"Output: {OUTPUT_DIR}")
    print()

    print("Tower icons (10):")
    make_archer()
    make_catapult()
    make_wall()
    make_shrine()
    make_cavalry()
    make_gunpowder()
    make_industrial()
    make_bunker()
    make_tech()
    make_special()

    print("\nResource icons (3):")
    make_gold()
    make_blue_token()
    make_heart()

    print("\nAbility icons (4):")
    make_lightning()
    make_shield()
    make_heal()
    make_speed()

    print("\nUI icons (8):")
    make_pause()
    make_play()
    make_settings()
    make_menu()
    make_info()
    make_close()
    make_arrow_left()
    make_arrow_right()

    print("\nScroll icons (4):")
    make_scroll(GRAY, "common")
    make_scroll(SUCCESS, "uncommon")
    make_scroll(INFO_BLUE, "rare")
    make_scroll(PURPLE, "epic")

    print("\nNotification icons (4):")
    make_success()
    make_error()
    make_warning()
    make_info_circle()

    print("\nDone! 33 icons generated.")
