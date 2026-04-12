"""
Sakartvelo Defenders Sprite Generator
Cel-shaded 2D isometric pixel art generation based on Art Style Guide v2.0
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from dataclasses import dataclass
from typing import Tuple, List, Optional
import os

# ==========================================
# ERA PALETTES (from Art Style Guide Section 3)
# ==========================================

@dataclass
class EraPalette:
    name: str
    base: str        # Dominant color for large surfaces
    highlight: str   # Brightest color for light-facing planes
    shadow: str      # Darkest color for depth
    accent: str      # Signature color for banners, heroes
    sky: str         # Background for maps
    vegetation: str  # Trees, grass, crops
    stone_earth: str # Building materials
    water: str       # Rivers, fountains, coast

ERA_PALETTES = {
    0: EraPalette("Ancient Colchis", "#2D5A3D", "#4CAF50", "#1B3A26", "#D4A017", "#87CEEB", "#3A7D44", "#8B7355", "#2E86AB"),
    1: EraPalette("Kingdom of Iberia", "#4A3728", "#8D6E63", "#2C1F17", "#C8A96E", "#7FB3D8", "#5D8A3C", "#9E8B6E", "#4682B4"),
    2: EraPalette("Age of Invasions", "#5C3A21", "#A0522D", "#3B2510", "#DAA520", "#B8860B", "#6B8E23", "#8B7D6B", "#4A708B"),
    3: EraPalette("Georgian Golden Age", "#1A4D2E", "#D4AF37", "#0D2818", "#C41E3A", "#4A90D9", "#4CAF50", "#B8860B", "#2980B9"),
    4: EraPalette("Mongol Catastrophe", "#3D2B1F", "#8B6914", "#261A11", "#CC5500", "#8B4513", "#556B2F", "#696969", "#4682B4"),
    5: EraPalette("Between Empires", "#1A3C5E", "#3498DB", "#0D2137", "#E74C3C", "#F5DEB3", "#2E8B57", "#CD853F", "#5F9EA0"),
    6: EraPalette("Russian Empire", "#2C2C3E", "#7B8DB1", "#1A1A2E", "#9B59B6", "#BDC3C7", "#4A7C59", "#8B8682", "#5B8FA8"),
    7: EraPalette("First Dem. Republic", "#1B4332", "#52B788", "#0B2618", "#E63946", "#A8DADC", "#40916C", "#6B705C", "#457B9D"),
    8: EraPalette("The Soviet Century", "#2D2D2D", "#757575", "#1A1A1A", "#D32F2F", "#90A4AE", "#558B2F", "#795548", "#546E7A"),
    9: EraPalette("Modern Georgia", "#0D1B2A", "#415A77", "#070E18", "#E63946", "#E0E1DD", "#2D6A4F", "#777777", "#1D3557"),
}

# GLOBAL UI PALETTE (Section 2)
UI_PALETTE = {
    "bg_dark": "#1A1A1A",
    "bg_light": "#F5F0EB",
    "text_dark": "#FFFFFF",
    "text_light": "#1A1A1A",
    "text_secondary_dark": "#B0B8C0",
    "text_secondary_light": "#6B7280",
    "accent": "#E67E22",
    "accent_hover": "#F39C12",
    "danger": "#E74C3C",
    "success": "#27AE60",
    "info": "#3498DB",
    "panel_bg_dark": "#2C3E50",
    "panel_bg_light": "#FFFFFF",
    "border_dark": "#3D566E",
    "border_light": "#E5E7EB",
    "disabled_dark": "#4A5568",
    "disabled_light": "#D1D5DB",
}

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex color string."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def desaturate(hex_color: str, opacity: float = 0.4) -> str:
    """Create desaturated version of color for shadows."""
    r, g, b = hex_to_rgb(hex_color)
    avg = (r + g + b) // 3
    result = (
        int(r * (1 - opacity) + avg * opacity),
        int(g * (1 - opacity) + avg * opacity),
        int(b * (1 - opacity) + avg * opacity)
    )
    return rgb_to_hex(result)

def lighten(hex_color: str, opacity: float = 0.3) -> str:
    """Create lighter version for highlights."""
    r, g, b = hex_to_rgb(hex_color)
    result = (
        int(r * (1 - opacity) + 255 * opacity),
        int(g * (1 - opacity) + 255 * opacity),
        int(b * (1 - opacity) + 255 * opacity)
    )
    return rgb_to_hex(result)

# ==========================================
# SPRITE GENERATOR CLASS
# ==========================================

class SpriteGenerator:
    """Cel-shaded sprite generator for Sakartvelo Defenders."""

    def __init__(self, size: int = 512):
        self.size = size
        self.outline_color = hex_to_rgb("#1A1A1A")
        self.outline_width = 2

    def create_base_image(self, transparent: bool = True) -> Image.Image:
        """Create a new base image."""
        if transparent:
            img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        else:
            img = Image.new('RGBA', (self.size, self.size), (255, 255, 255, 255))
        return img

    def draw_isometric_cube(self, draw: ImageDraw.Draw, x: int, y: int,
                           size: int, height: int,
                           base_color: str, highlight_color: str, shadow_color: str,
                           outline: bool = True) -> None:
        """
        Draw an isometric cube with cel-shaded lighting.
        Shadow direction: lower-right 45°
        Lighting: upper-left
        """
        # Isometric projection angles
        angle = 30 * (3.14159 / 180)  # 30 degrees in radians

        # Cube dimensions
        width = size
        depth = size * 0.5  # Isometric foreshortening

        # Calculate vertex positions
        # Top face (diamond)
        top_x = x
        top_y = y - height

        # Top face vertices
        top_vertices = [
            (top_x, top_y),                              # top center
            (top_x + width * 0.5, top_y + depth * 0.5),  # top right
            (top_x, top_y + depth),                      # bottom right
            (top_x - width * 0.5, top_y + depth * 0.5),  # bottom left
        ]

        # Left face vertices (in shadow)
        left_vertices = [
            top_vertices[3],
            top_vertices[2],
            (x, y + depth),  # bottom right of left face
            (x - width * 0.5, y + depth * 0.5),  # bottom left of left face
        ]

        # Right face vertices (highlight)
        right_vertices = [
            top_vertices[2],
            top_vertices[1],
            (x + width * 0.5, y + depth * 0.5),  # bottom right of right face
            (x, y + depth),  # bottom left of right face
        ]

        # Draw faces with flat colors (cel-shaded)
        # Top face - base color
        draw.polygon(top_vertices, fill=base_color, outline=self.outline_color if outline else None)
        # Left face - shadow color
        draw.polygon(left_vertices, fill=shadow_color, outline=self.outline_color if outline else None)
        # Right face - highlight color
        draw.polygon(right_vertices, fill=highlight_color, outline=self.outline_color if outline else None)

    def draw_cylinder(self, draw: ImageDraw.Draw, x: int, y: int,
                     width: int, height: int,
                     base_color: str, highlight_color: str, shadow_color: str,
                     outline: bool = True) -> None:
        """Draw a cylinder (for towers with round tops)."""
        radius = width // 2
        ellipse_rect = [x - radius, y - height - radius // 2,
                       x + radius, y - height + radius // 2]

        # Draw body (rectangle)
        body_rect = [x - radius, y - height, x + radius, y]
        draw.rectangle(body_rect, fill=base_color, outline=self.outline_color if outline else None)

        # Draw top ellipse (highlight)
        draw.ellipse(ellipse_rect, fill=highlight_color, outline=self.outline_color if outline else None)

    def draw_shadow(self, draw: ImageDraw.Draw, x: int, y: int,
                   size: int, height: int,
                   base_color: str) -> None:
        """Draw cel-shaded shadow at lower-right 45°."""
        shadow_color = desaturate(base_color, 0.4)
        shadow_offset = height // 3

        # Shadow is a flattened ellipse
        shadow_rect = [
            x - size // 2 + shadow_offset // 2,
            y + shadow_offset,
            x + size // 2 + shadow_offset,
            y + shadow_offset + size // 4
        ]
        draw.ellipse(shadow_rect, fill=shadow_color, outline=None)

    def draw_decorative_element(self, draw: ImageDraw.Draw, x: int, y: int,
                               element_type: str, size: int, color: str) -> None:
        """Draw decorative elements (crosses, banners, patterns)."""
        if element_type == "cross":
            # Georgian cross
            bar_width = size // 4
            # Vertical bar
            draw.rectangle([x - bar_width // 2, y - size // 2, x + bar_width // 2, y + size // 2],
                         fill=color, outline=self.outline_color)
            # Horizontal bar
            draw.rectangle([x - size // 2, y - bar_width // 2, x + size // 2, y + bar_width // 2],
                         fill=color, outline=self.outline_color)
        elif element_type == "diamond":
            # Diamond pattern
            points = [(x, y - size // 2), (x + size // 2, y), (x, y + size // 2), (x - size // 2, y)]
            draw.polygon(points, fill=color, outline=self.outline_color)
        elif element_type == "circle":
            # Circular pattern
            draw.ellipse([x - size // 2, y - size // 2, x + size // 2, y + size // 2],
                        fill=color, outline=self.outline_color)

# ==========================================
# TOWER GENERATORS
# ==========================================

class TowerGenerator(SpriteGenerator):
    """Generate tower sprites following Art Style Guide Section 4."""

    TOWER_TYPES = [
        "archer",
        "catapult",
        "wall",
        "shrine",
        "cavalry",
        "gunpowder",
        "industrial",
        "bunker",
        "tech",
        "special",
    ]

    def generate_archer_tower(self, era: int) -> Image.Image:
        """Generate an archer tower sprite."""
        palette = ERA_PALETTES[era]
        img = self.create_base_image()
        draw = ImageDraw.Draw(img)

        center = self.size // 2
        base_y = self.size - 80

        # Draw shadow
        self.draw_shadow(draw, center, base_y, 120, 100, palette.stone_earth)

        # Stone foundation (Era 0-2: wood on stone)
        if era <= 1:
            # Stone base
            self.draw_isometric_cube(draw, center, base_y - 30, 100, 30,
                                   palette.stone_earth,
                                   lighten(palette.stone_earth),
                                   desaturate(palette.stone_earth))
            # Wooden platform
            self.draw_isometric_cube(draw, center, base_y - 80, 80, 50,
                                   palette.base,
                                   lighten(palette.base),
                                   desaturate(palette.base))
        else:
            # Stone/brick tower
            self.draw_isometric_cube(draw, center, base_y - 50, 90, 50,
                                   palette.stone_earth,
                                   lighten(palette.stone_earth),
                                   desaturate(palette.stone_earth))

        # Tower body
        tower_height = 120
        self.draw_isometric_cube(draw, center, base_y - tower_height - 50, 60, tower_height,
                               palette.base,
                               palette.highlight,
                               palette.shadow)

        # Top platform
        self.draw_isometric_cube(draw, center, base_y - tower_height - 90, 70, 40,
                               palette.stone_earth,
                               lighten(palette.stone_earth),
                               desaturate(palette.stone_earth))

        # Crenellations / Parapet
        for i in range(4):
            offset = (i - 1.5) * 15
            self.draw_isometric_cube(draw, center + offset, base_y - tower_height - 130, 10, 15,
                                   palette.base,
                                   palette.highlight,
                                   palette.shadow)

        # Decorative accent (gold/cross for Era 3+)
        if era >= 3:
            self.draw_decorative_element(draw, center, base_y - tower_height - 100, "cross", 20, palette.accent)
        else:
            self.draw_decorative_element(draw, center, base_y - tower_height - 100, "diamond", 15, palette.accent)

        return img

    def generate_catapult_tower(self, era: int) -> Image.Image:
        """Generate a catapult/siege tower sprite."""
        palette = ERA_PALETTES[era]
        img = self.create_base_image()
        draw = ImageDraw.Draw(img)

        center = self.size // 2
        base_y = self.size - 80

        # Shadow
        self.draw_shadow(draw, center, base_y, 140, 80, palette.stone_earth)

        # Wide stone base
        self.draw_isometric_cube(draw, center, base_y - 40, 130, 40,
                               palette.stone_earth,
                               lighten(palette.stone_earth),
                               desaturate(palette.stone_earth))

        # Tower body (wider)
        self.draw_isometric_cube(draw, center, base_y - 120, 100, 80,
                               palette.base,
                               palette.highlight,
                               palette.shadow)

        # Arm base
        self.draw_isometric_cube(draw, center, base_y - 160, 50, 40,
                               palette.stone_earth,
                               lighten(palette.stone_earth),
                               desaturate(palette.stone_earth))

        # Catapult arm (diagonal)
        arm_end_x = center + 60
        arm_end_y = base_y - 220
        draw.line([center - 40, base_y - 140, arm_end_x, arm_end_y],
                 fill=palette.stone_earth, width=8)

        # Arm tip
        draw.ellipse([arm_end_x - 10, arm_end_y - 10, arm_end_x + 10, arm_end_y + 10],
                    fill=palette.accent, outline=self.outline_color)

        # Accent banner
        draw.rectangle([center - 20, base_y - 170, center + 20, base_y - 150],
                      fill=palette.accent, outline=self.outline_color)

        return img

    def generate_wall_tower(self, era: int) -> Image.Image:
        """Generate a wall/defensive tower sprite."""
        palette = ERA_PALETTES[era]
        img = self.create_base_image()
        draw = ImageDraw.Draw(img)

        center = self.size // 2
        base_y = self.size - 80

        # Shadow
        self.draw_shadow(draw, center, base_y, 150, 60, palette.stone_earth)

        # Wide wall base
        self.draw_isometric_cube(draw, center, base_y - 40, 140, 40,
                               palette.stone_earth,
                               lighten(palette.stone_earth),
                               desaturate(palette.stone_earth))

        # Wall body
        self.draw_isometric_cube(draw, center, base_y - 100, 120, 60,
                               palette.stone_earth,
                               lighten(palette.stone_earth),
                               desaturate(palette.stone_earth))

        # Battlements
        for i in range(6):
            offset = (i - 2.5) * 20
            self.draw_isometric_cube(draw, center + offset, base_y - 120, 12, 20,
                                   palette.stone_earth,
                                   lighten(palette.stone_earth),
                                   desaturate(palette.stone_earth))

        # Accent color on battlements
        for i in range(3):
            offset = (i - 1) * 40
            draw.rectangle([center + offset - 5, base_y - 115, center + offset + 5, base_y - 105],
                          fill=palette.accent)

        return img

    def generate_shrine_tower(self, era: int) -> Image.Image:
        """Generate a shrine tower sprite (Era 3+)."""
        palette = ERA_PALETTES[era]
        img = self.create_base_image()
        draw = ImageDraw.Draw(img)

        center = self.size // 2
        base_y = self.size - 80

        # Shadow
        self.draw_shadow(draw, center, base_y, 120, 100, palette.stone_earth)

        # Ornate base
        self.draw_isometric_cube(draw, center, base_y - 40, 100, 40,
                               palette.stone_earth,
                               lighten(palette.stone_earth),
                               desaturate(palette.stone_earth))

        # Main shrine body
        self.draw_isometric_cube(draw, center, base_y - 120, 70, 80,
                               palette.base,
                               palette.highlight,
                               palette.shadow)

        # Gold dome (cylinder)
        self.draw_cylinder(draw, center, base_y - 160, 60, 50,
                          palette.accent,
                          lighten(palette.accent),
                          desaturate(palette.accent))

        # Cross on top
        self.draw_decorative_element(draw, center, base_y - 220, "cross", 25, palette.accent)

        # Decorative columns
        for i in range(4):
            offset = (i - 1.5) * 30
            self.draw_cylinder(draw, center + offset, base_y - 120, 12, 80,
                             palette.highlight,
                             lighten(palette.highlight),
                             desaturate(palette.highlight))

        return img

    def generate_cavalry_tower(self, era: int) -> Image.Image:
        """Generate a cavalry tower sprite (spawns mounted units)."""
        palette = ERA_PALETTES[era]
        img = self.create_base_image()
        draw = ImageDraw.Draw(img)

        center = self.size // 2
        base_y = self.size - 80

        # Shadow
        self.draw_shadow(draw, center, base_y, 110, 80, palette.stone_earth)

        # Stone stable base
        self.draw_isometric_cube(draw, center, base_y - 35, 100, 35,
                               palette.stone_earth,
                               lighten(palette.stone_earth),
                               desaturate(palette.stone_earth))

        # Tower body
        self.draw_isometric_cube(draw, center, base_y - 100, 70, 65,
                               palette.base,
                               palette.highlight,
                               palette.shadow)

        # Horse stall opening (arch)
        arch_rect = [center - 25, base_y - 95, center + 25, base_y - 50]
        draw.ellipse(arch_rect, fill=desaturate(palette.stone_earth, 0.7))

        # Top platform with horse emblem
        self.draw_isometric_cube(draw, center, base_y - 130, 75, 30,
                               palette.highlight,
                               lighten(palette.highlight),
                               desaturate(palette.highlight))

        # Horse emblem (simplified)
        emblem_x = center
        emblem_y = base_y - 145
        draw.ellipse([emblem_x - 15, emblem_y - 8, emblem_x + 15, emblem_y + 8],
                    fill=palette.accent, outline=self.outline_color)

        # Flag banner
        draw.polygon([(center + 30, base_y - 130), (center + 30, base_y - 80),
                     (center + 70, base_y - 105)],
                    fill=palette.accent, outline=self.outline_color)

        return img

    def generate_gunpowder_tower(self, era: int) -> Image.Image:
        """Generate a gunpowder/cannon tower sprite."""
        palette = ERA_PALETTES[era]
        img = self.create_base_image()
        draw = ImageDraw.Draw(img)

        center = self.size // 2
        base_y = self.size - 80

        # Shadow
        self.draw_shadow(draw, center, base_y, 130, 90, palette.stone_earth)

        # Reinforced brick base
        self.draw_isometric_cube(draw, center, base_y - 45, 120, 45,
                               palette.stone_earth,
                               lighten(palette.stone_earth),
                               desaturate(palette.stone_earth))

        # Thick stone walls
        self.draw_isometric_cube(draw, center, base_y - 120, 100, 75,
                               palette.stone_earth,
                               lighten(palette.stone_earth),
                               desaturate(palette.stone_earth))

        # Gunport openings
        for i in range(3):
            offset = (i - 1) * 25
            draw.rectangle([center + offset - 8, base_y - 110, center + offset + 8, base_y - 70],
                          fill=desaturate(palette.base, 0.8))

        # Cannon barrel protruding
        cannon_x = center
        cannon_y = base_y - 100
        draw.rectangle([cannon_x - 40, cannon_y - 8, cannon_x + 20, cannon_y + 8],
                      fill=palette.stone_earth, outline=self.outline_color)

        # Smoke effect (simplified)
        for i in range(5):
            smoke_x = cannon_x - 45 - i * 10
            smoke_y = cannon_y - 15 - i * 8
            draw.ellipse([smoke_x - 8, smoke_y - 6, smoke_x + 8, smoke_y + 6],
                        fill=lighten(palette.stone_earth, 0.6), outline=None)

        # Fuse sparks
        spark_x = cannon_x - 45
        spark_y = cannon_y - 10
        for i in range(3):
            draw.ellipse([spark_x + i * 3 - 2, spark_y - i * 4 - 2,
                        spark_x + i * 3 + 2, spark_y - i * 4 + 2],
                        fill=palette.accent, outline=None)

        return img

    def generate_industrial_tower(self, era: int) -> Image.Image:
        """Generate an industrial/area damage tower sprite."""
        palette = ERA_PALETTES[era]
        img = self.create_base_image()
        draw = ImageDraw.Draw(img)

        center = self.size // 2
        base_y = self.size - 80

        # Shadow
        self.draw_shadow(draw, center, base_y, 140, 100, palette.stone_earth)

        # Concrete foundation
        self.draw_isometric_cube(draw, center, base_y - 40, 130, 40,
                               palette.stone_earth,
                               lighten(palette.stone_earth),
                               desaturate(palette.stone_earth))

        # Industrial structure
        self.draw_isometric_cube(draw, center, base_y - 110, 110, 70,
                               palette.base,
                               palette.highlight,
                               palette.shadow)

        # Chimney/smokestack
        self.draw_cylinder(draw, center, base_y - 160, 40, 50,
                          palette.stone_earth,
                          lighten(palette.stone_earth),
                          desaturate(palette.stone_earth))

        # Steam vents on sides
        for i in range(2):
            vent_x = center + (i - 0.5) * 60
            vent_y = base_y - 100
            self.draw_cylinder(draw, vent_x, vent_y, 15, 30,
                              palette.highlight,
                              lighten(palette.highlight),
                              desaturate(palette.highlight))

        # Warning stripes
        for i in range(4):
            stripe_x = center - 45 + i * 30
            draw.line([stripe_x, base_y - 110, stripe_x, base_y - 60],
                     fill=palette.accent, width=6)

        return img

    def generate_bunker_tower(self, era: int) -> Image.Image:
        """Generate a fortified bunker tower sprite."""
        palette = ERA_PALETTES[era]
        img = self.create_base_image()
        draw = ImageDraw.Draw(img)

        center = self.size // 2
        base_y = self.size - 80

        # Large shadow
        self.draw_shadow(draw, center, base_y, 150, 70, palette.stone_earth)

        # Wide concrete bunker base
        self.draw_isometric_cube(draw, center, base_y - 50, 140, 50,
                               palette.stone_earth,
                               lighten(palette.stone_earth),
                               desaturate(palette.stone_earth))

        # Reinforced structure
        self.draw_isometric_cube(draw, center, base_y - 100, 120, 50,
                               palette.base,
                               palette.highlight,
                               palette.shadow)

        # Sandbag top (stacked rectangles)
        for i in range(3):
            bag_y = base_y - 100 - i * 10
            bag_width = 120 - i * 5
            draw.rectangle([center - bag_width // 2, bag_y,
                          center + bag_width // 2, bag_y + 8],
                         fill=palette.highlight, outline=self.outline_color)

        # Machine gun position
        mg_x = center
        mg_y = base_y - 130
        draw.ellipse([mg_x - 12, mg_y - 8, mg_x + 12, mg_y + 8],
                    fill=palette.stone_earth, outline=self.outline_color)
        draw.line([mg_x, mg_y, mg_x + 30, mg_y + 10],
                 fill=palette.stone_earth, width=6)

        # Crossed sandbags (barricade)
        draw.line([center - 40, base_y - 60, center - 20, base_y - 40],
                 fill=palette.highlight, width=8)
        draw.line([center - 40, base_y - 40, center - 20, base_y - 60],
                 fill=palette.highlight, width=8)

        return img

    def generate_tech_tower(self, era: int) -> Image.Image:
        """Generate a high-tech tower with special effects."""
        palette = ERA_PALETTES[era]
        img = self.create_base_image()
        draw = ImageDraw.Draw(img)

        center = self.size // 2
        base_y = self.size - 80

        # Shadow with glow effect
        self.draw_shadow(draw, center, base_y, 100, 100, palette.accent)

        # Circular base platform
        base_radius = 70
        draw.ellipse([center - base_radius, base_y - base_radius // 2,
                     center + base_radius, base_y + base_radius // 2],
                    fill=palette.stone_earth, outline=self.outline_color)

        # Central tower body (cylinder)
        self.draw_cylinder(draw, center, base_y - 80, 50, 80,
                          palette.base,
                          palette.highlight,
                          palette.shadow)

        # Energy crystal at top
        crystal_y = base_y - 140
        crystal_points = [
            (center, crystal_y - 30),  # top
            (center + 20, crystal_y),  # right
            (center, crystal_y + 30),  # bottom
            (center - 20, crystal_y),  # left
        ]
        draw.polygon(crystal_points, fill=palette.accent, outline=self.outline_color)

        # Energy rings (glowing circles)
        for i in range(3):
            ring_y = crystal_y + i * 15
            ring_radius = 35 + i * 8
            draw.ellipse([center - ring_radius, ring_y - ring_radius // 3,
                         center + ring_radius, ring_y + ring_radius // 3],
                        outline=lighten(palette.accent, 0.5), width=3)

        # Antenna array
        for i in range(4):
            antenna_x = center + (i - 1.5) * 20
            antenna_y = base_y - 120
            draw.line([antenna_x, antenna_y, antenna_x, antenna_y - 40],
                     fill=palette.stone_earth, width=3)
            draw.ellipse([antenna_x - 4, antenna_y - 45, antenna_x + 4, antenna_y - 37],
                        fill=palette.accent, outline=self.outline_color)

        return img

    def generate_special_tower(self, era: int) -> Image.Image:
        """Generate a special unique tower sprite."""
        palette = ERA_PALETTES[era]
        img = self.create_base_image()
        draw = ImageDraw.Draw(img)

        center = self.size // 2
        base_y = self.size - 80

        # Shadow
        self.draw_shadow(draw, center, base_y, 120, 120, palette.accent)

        # Ornate foundation with gold trim
        self.draw_isometric_cube(draw, center, base_y - 40, 110, 40,
                               palette.stone_earth,
                               lighten(palette.stone_earth),
                               desaturate(palette.stone_earth))

        # Gold border on base
        for i in range(4):
            offset = (i - 1.5) * 25
            draw.rectangle([center + offset - 10, base_y - 42, center + offset + 10, base_y - 38],
                          fill=palette.accent)

        # Main tower structure
        self.draw_isometric_cube(draw, center, base_y - 110, 80, 70,
                               palette.base,
                               palette.highlight,
                               palette.shadow)

        # Ornate roof (dome)
        self.draw_cylinder(draw, center, base_y - 150, 50, 40,
                          palette.accent,
                          lighten(palette.accent),
                          desaturate(palette.accent))

        # Georgian cross on top
        self.draw_decorative_element(draw, center, base_y - 200, "cross", 30, palette.accent)

        # Decorative columns on each side
        for i in range(4):
            col_x = center + (i - 1.5) * 40
            self.draw_cylinder(draw, col_x, base_y - 110, 12, 70,
                             palette.highlight,
                             lighten(palette.highlight),
                             desaturate(palette.highlight))

        # Banners on each side
        for i in range(2):
            banner_x = center + (i - 0.5) * 50
            draw.polygon([(banner_x, base_y - 150), (banner_x, base_y - 70),
                         (banner_x + 30, base_y - 110)],
                        fill=palette.accent, outline=self.outline_color)
            # Banner symbol (diamond)
            self.draw_decorative_element(draw, banner_x + 15, base_y - 110, "diamond", 12, palette.highlight)

        return img

    def generate_tower(self, tower_type: str, era: int = 0) -> Image.Image:
        """Generate a tower sprite by type."""
        generators = {
            "archer": self.generate_archer_tower,
            "catapult": self.generate_catapult_tower,
            "wall": self.generate_wall_tower,
            "shrine": self.generate_shrine_tower,
            "cavalry": self.generate_cavalry_tower,
            "gunpowder": self.generate_gunpowder_tower,
            "industrial": self.generate_industrial_tower,
            "bunker": self.generate_bunker_tower,
            "tech": self.generate_tech_tower,
            "special": self.generate_special_tower,
        }

        generator = generators.get(tower_type, self.generate_archer_tower)
        return generator(era)

    def generate_tower_silhouette_sheet(self, era: int = 0) -> Image.Image:
        """Generate a silhouette sheet with all 10 tower types."""
        # Create sheet with 2 rows x 5 columns
        sheet_width = 512 * 5
        sheet_height = 512 * 2
        sheet = Image.new('RGBA', (sheet_width, sheet_height), (50, 50, 50, 255))
        draw = ImageDraw.Draw(sheet)

        # Generate and place each tower
        for i, tower_type in enumerate(self.TOWER_TYPES):
            row = i // 5
            col = i % 5
            x = col * 512
            y = row * 512

            # Generate tower
            tower = self.generate_tower(tower_type, era)

            # Convert to silhouette (solid black)
            silhouette = Image.new('RGBA', tower.size, (0, 0, 0, 255))
            for px in range(tower.size[0]):
                for py in range(tower.size[1]):
                    if tower.getpixel((px, py))[3] > 0:  # If not transparent
                        silhouette.putpixel((px, py), (0, 0, 0, 255))

            # Paste silhouette onto sheet
            sheet.paste(silhouette, (x, y))

            # Add label
            draw.text((x + 10, y + 10), f"{i+1}. {tower_type}", fill=(200, 200, 200, 255))

        return sheet

# ==========================================
# MAIN EXPORT
# ==========================================

def generate_tower_sheet(output_path: str, era: int = 0) -> None:
    """Generate and save tower silhouette sheet."""
    generator = TowerGenerator(size=512)
    sheet = generator.generate_tower_silhouette_sheet(era)
    sheet.save(output_path)
    print(f"Saved tower silhouette sheet to {output_path}")

if __name__ == "__main__":
    # Test: Generate Era 0 tower sheet
    output_path = "/home/socraticblock/hermes-workspace/hermes/development/sakartvelo-defenders/assets/towers/tower_silhouette_sheet_e00.png"
    generate_tower_sheet(output_path, era=0)
    print(f"✓ Generated tower silhouette sheet")

    # Test: Generate all 10 tower types for Era 0
    gen = TowerGenerator(size=512)
    for tower_type in gen.TOWER_TYPES:
        tower = gen.generate_tower(tower_type, era=0)
        output_path = f"/home/socraticblock/hermes-workspace/hermes/development/sakartvelo-defenders/assets/towers/e00_colchis/twr_e00_{tower_type}_v01.png"
        tower.save(output_path)
        print(f"✓ Generated {tower_type} tower")
