"""
Sakartvelo Defenders Map Generator
Cel-shaded map backgrounds with three-layer depth (Section 8)
"""

import math
import random
from PIL import Image, ImageDraw
from sprite_generator import ERA_PALETTES, hex_to_rgb, lighten, desaturate

class MapGenerator:
    """Generate map backgrounds following Art Style Guide Section 8."""

    def __init__(self, size: int = 2048):
        self.size = size
        # Layer proportions: Foreground 40%, Midground 35%, Background 25%
        self.foreground_height = int(size * 0.4)
        self.midground_height = int(size * 0.35)
        self.background_height = int(size * 0.25)

    def create_base_image(self) -> Image.Image:
        """Create a new base image (JPG for maps)."""
        return Image.new('RGB', (self.size, self.size), (255, 255, 255))

    def draw_background_layer(self, draw: ImageDraw, era: int, mood: str = "misty") -> None:
        """
        Draw the background layer (25% height).
        Sky, distant mountains, horizon.
        """
        palette = ERA_PALETTES[era]

        # Sky gradient
        sky_rgb = hex_to_rgb(palette.sky)
        horizon_rgb = tuple(min(255, c + 50) for c in sky_rgb)  # Lighten manually

        for y in range(self.background_height):
            ratio = y / self.background_height
            r = int(sky_rgb[0] * (1 - ratio) + horizon_rgb[0] * ratio)
            g = int(sky_rgb[1] * (1 - ratio) + horizon_rgb[1] * ratio)
            b = int(sky_rgb[2] * (1 - ratio) + horizon_rgb[2] * ratio)

            # Add misty effect for Era 0
            if mood == "misty":
                mist_factor = int(50 * (1 - ratio))
                r = min(255, r + mist_factor)
                g = min(255, g + mist_factor)
                b = min(255, b + mist_factor)

            draw.line([(0, y), (self.size, y)], fill=(r, g, b))

        # Distant mountains
        mountain_color = desaturate(palette.stone_earth)
        for i in range(5):
            mountain_x = i * (self.size // 4)
            mountain_base = self.background_height
            mountain_height = 150 + random.randint(0, 100)
            mountain_width = 200 + random.randint(0, 100)

            # Simple isometric mountain shape
            mountain_points = [
                (mountain_x, mountain_base),
                (mountain_x + mountain_width // 2, mountain_base - mountain_height),
                (mountain_x + mountain_width, mountain_base),
            ]
            draw.polygon(mountain_points, fill=mountain_color, outline=None)

        # Sun/moon glow
        sun_x = self.size // 4
        sun_y = 80
        sun_radius = 60
        sun_color = tuple(min(255, c + 100) for c in hex_to_rgb(palette.accent))

        for r in range(sun_radius, 0, -10):
            opacity = int(100 * (1 - r / sun_radius))
            # Create glow effect
            glow_color = tuple(min(255, c + opacity) for c in sun_color)
            draw.ellipse([sun_x - r, sun_y - r, sun_x + r, sun_y + r],
                        fill=glow_color)

    def draw_midground_layer(self, draw: ImageDraw, era: int) -> None:
        """
        Draw the midground layer (35% height).
        Enemy path with terrain features.
        """
        palette = ERA_PALETTES[era]
        y_offset = self.background_height

        # Base terrain
        terrain_rgb = hex_to_rgb(palette.base)
        for y in range(self.midground_height):
            draw.line([(0, y_offset + y), (self.size, y_offset + y)],
                     fill=terrain_rgb)

        # Enemy path (curved, visible against terrain)
        path_color = tuple(min(255, c + 80) for c in hex_to_rgb(palette.stone_earth))
        path_points = []
        for x in range(0, self.size, 20):
            # Winding path using sine wave
            y = int(y_offset + self.midground_height // 2 + 80 * math.sin(x / 200))
            path_points.append((x, y))

        # Draw path as wide line
        for i in range(len(path_points) - 1):
            draw.line([path_points[i], path_points[i + 1]], fill=path_color, width=40)

        # River (Era 0: Black Sea coastal area)
        river_color = hex_to_rgb(palette.water)
        river_points = []
        for x in range(0, self.size, 15):
            y = int(y_offset + 100 + 50 * math.sin(x / 150 + 1))
            river_points.append((x, y))

        for i in range(len(river_points) - 1):
            draw.line([river_points[i], river_points[i + 1]], fill=river_color, width=25)

        # Dense forest patches
        forest_color = hex_to_rgb(palette.vegetation)
        forest_positions = [
            (100, y_offset + 50), (300, y_offset + 100), (500, y_offset + 80),
            (700, y_offset + 120), (900, y_offset + 60), (1100, y_offset + 100),
            (1300, y_offset + 70), (1500, y_offset + 90), (1700, y_offset + 110),
            (1900, y_offset + 80),
        ]

        for fx, fy in forest_positions:
            # Draw multiple trees
            for i in range(5):
                tree_x = fx + random.randint(-40, 40)
                tree_y = fy + random.randint(-20, 20)
                tree_size = random.randint(30, 50)

                # Tree trunk
                trunk_color = hex_to_rgb(palette.stone_earth)
                draw.rectangle([tree_x - 3, tree_y, tree_x + 3, tree_y + tree_size // 2],
                             fill=trunk_color, outline=None)

                # Tree foliage (circle)
                draw.ellipse([tree_x - tree_size, tree_y - tree_size,
                             tree_x + tree_size, tree_y],
                            fill=forest_color, outline=None)

        # Gold mine area (Era 0 specific)
        mine_color = hex_to_rgb(palette.stone_earth)
        mine_x = self.size - 200
        mine_y = y_offset + 50

        # Mine entrance
        draw.ellipse([mine_x - 40, mine_y - 30, mine_x + 40, mine_y + 30],
                    fill=mine_color, outline=None)
        # Dark entrance
        draw.ellipse([mine_x - 20, mine_y - 15, mine_x + 20, mine_y + 15],
                    fill=(30, 30, 30), outline=None)
        # Gold nuggets
        for i in range(5):
            nugget_x = mine_x + random.randint(-30, 30)
            nugget_y = mine_y + random.randint(-20, 20)
            draw.ellipse([nugget_x - 5, nugget_y - 5, nugget_x + 5, nugget_y + 5],
                        fill=hex_to_rgb(palette.accent), outline=None)

        # Stone ruins (Ancient Vani)
        ruin_color = desaturate(palette.stone_earth)
        ruin_x = 150
        ruin_y = y_offset + 200
        # Broken pillar
        draw.rectangle([ruin_x, ruin_y - 60, ruin_x + 20, ruin_y],
                      fill=ruin_color, outline=None)
        # Another pillar fragment
        draw.rectangle([ruin_x + 30, ruin_y - 40, ruin_x + 45, ruin_y],
                      fill=ruin_color, outline=None)

    def draw_foreground_layer(self, draw: ImageDraw, era: int) -> None:
        """
        Draw the foreground layer (40% height).
        Tower placement zone with grid markers.
        """
        palette = ERA_PALETTES[era]
        y_offset = self.background_height + self.midground_height

        # Base terrain (closer, brighter)
        terrain_rgb = tuple(min(255, c + 25) for c in hex_to_rgb(palette.base))
        for y in range(self.foreground_height):
            draw.line([(0, y_offset + y), (self.size, y_offset + y)],
                     fill=terrain_rgb)

        # Tower placement zones (subtle grid markers)
        grid_color = hex_to_rgb(palette.shadow)
        grid_spacing = 120
        grid_size = 80

        for gx in range(50, self.size - 50, grid_spacing):
            for gy in range(y_offset + 30, self.size - 50, grid_spacing):
                # Draw subtle grid marker
                marker_color = (grid_color[0], grid_color[1], grid_color[2], 77)  # 30% opacity
                draw.rectangle([gx, gy, gx + grid_size, gy + grid_size],
                             outline=grid_color, width=1)

                # Inner crosshair
                draw.line([(gx + grid_size // 2, gy + 5),
                          (gx + grid_size // 2, gy + grid_size - 5)],
                         fill=grid_color, width=1)
                draw.line([(gx + 5, gy + grid_size // 2),
                          (gx + grid_size - 5, gy + grid_size // 2)],
                         fill=grid_color, width=1)

        # Larger trees in foreground (closer, more detail)
        forest_color = hex_to_rgb(palette.vegetation)
        trunk_color = hex_to_rgb(palette.stone_earth)

        # Frame the map with trees on sides
        for i in range(3):
            # Left side trees
            left_x = 30 + i * 25
            left_y = y_offset + 50 + i * 150
            tree_size = 60 + i * 10

            draw.rectangle([left_x - 5, left_y, left_x + 5, left_y + tree_size],
                         fill=trunk_color, outline=None)
            draw.ellipse([left_x - tree_size, left_y - tree_size,
                         left_x + tree_size, left_y],
                        fill=forest_color, outline=None)

            # Right side trees
            right_x = self.size - 30 - i * 25
            right_y = y_offset + 80 + i * 120

            draw.rectangle([right_x - 5, right_y, right_x + 5, right_y + tree_size],
                         fill=trunk_color, outline=None)
            draw.ellipse([right_x - tree_size, right_y - tree_size,
                         right_x + tree_size, right_y],
                        fill=forest_color, outline=None)

        # Elevation platform (visual height difference)
        elevated_y = y_offset + 80
        elevated_x = self.size // 2 - 60

        # Elevated platform base
        platform_color = hex_to_rgb(palette.stone_earth)
        draw.polygon([
            (elevated_x, elevated_y),
            (elevated_x + 120, elevated_y),
            (elevated_x + 140, elevated_y + 30),
            (elevated_x + 20, elevated_y + 30),
        ], fill=platform_color, outline=None)

        # Elevated platform surface
        surface_color = tuple(min(255, c + 50) for c in hex_to_rgb(palette.base))
        draw.polygon([
            (elevated_x + 10, elevated_y - 40),
            (elevated_x + 110, elevated_y - 40),
            (elevated_x + 120, elevated_y),
            (elevated_x + 20, elevated_y),
        ], fill=surface_color, outline=None)

        # Shadow under elevated platform
        shadow_color = tuple(int(c * 0.6) for c in platform_color)
        draw.ellipse([elevated_x, elevated_y + 30, elevated_x + 140, elevated_y + 50],
                    fill=shadow_color, outline=None)

    def generate_map(self, map_name: str, era: int = 0, mood: str = "misty") -> Image.Image:
        """Generate a map background by name."""
        img = self.create_base_image()
        draw = ImageDraw.Draw(img)

        # Draw three layers from back to front
        self.draw_background_layer(draw, era, mood)
        self.draw_midground_layer(draw, era)
        self.draw_foreground_layer(draw, era)

        return img

if __name__ == "__main__":
    import math  # Import for sine wave in path generation

    # Test: Generate Era 0 map (Colchian Forest / Black Sea Coast)
    gen = MapGenerator(size=2048)
    colchis_map = gen.generate_map("colchis_forest_coast", era=0, mood="misty")
    output_path = "/home/socraticblock/hermes-workspace/hermes/development/sakartvelo-defenders/assets/maps/e00_colchis/map_e00_colchis_forest_coast_v01.jpg"
    colchis_map.save(output_path, quality=95)
    print(f"✓ Generated Colchian Forest/Coast map (2048x2048)")
