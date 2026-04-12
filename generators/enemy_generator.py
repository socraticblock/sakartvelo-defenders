"""
Sakartvelo Defenders Enemy Generator
Cel-shaded 2D isometric enemy sprites with 10-unit proportion system (Section 5)
"""

from PIL import Image, ImageDraw
from sprite_generator import ERA_PALETTES, hex_to_rgb, lighten, desaturate

# ==========================================
# ENEMY DEFINITIONS
# ==========================================

class EnemyGenerator:
    """Generate enemy sprites following Art Style Guide Section 7."""

    # 10-unit proportion system (Section 5)
    # Units: 1 unit = 48 pixels at 512x512 resolution
    # Head: 2 units, Torso: 3 units, Legs: 3 units, Arms: 2 units each
    UNIT_SIZE = 48

    # Enemy categories (Section 7.1)
    ENEMY_CATEGORIES = {
        "infantry": {
            "body_type": "standard_10_unit",
            "movement": "ground_path",
            "color_treatment": "era_shadow_plus_base",
            "silhouette_key": "shield_spear_shape",
        },
        "cavalry": {
            "body_type": "10_unit_plus_mount",
            "movement": "fast_ground",
            "color_treatment": "era_base_plus_highlight",
            "silhouette_key": "horse_silhouette",
        },
        "siege": {
            "body_type": "boxy_6_8_units_wide",
            "movement": "slow_ground",
            "color_treatment": "era_stone_plus_shadow",
            "silhouette_key": "wheeled_wide_frame",
        },
        "flying": {
            "body_type": "compact_8_unit",
            "movement": "air_path",
            "color_treatment": "era_shadow_translucent_wings",
            "silhouette_key": "wing_spread_shape",
        },
        "boss": {
            "body_type": "12_14_unit_scale",
            "movement": "ground_varies",
            "color_treatment": "full_era_palette_plus_glow",
            "silhouette_key": "unique_per_boss",
        },
    }

    def __init__(self, size: int = 512):
        self.size = size
        self.outline_color = hex_to_rgb("#1A1A1A")
        self.outline_width = 3  # Characters use 3px outline

    def create_base_image(self) -> Image.Image:
        """Create a new transparent base image."""
        return Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))

    def draw_humanoid_body(self, draw: ImageDraw, center_x: int, base_y: int,
                          era: int, category: str) -> None:
        """
        Draw a humanoid body using the 10-unit proportion system.
        Proportions: Head (2 units), Torso (3 units), Legs (3 units), Arms (2 units each)
        """
        palette = ERA_PALETTES[era]
        u = self.UNIT_SIZE

        # Base position (feet)
        feet_y = base_y
        knee_y = base_y - 1.5 * u
        hip_y = base_y - 3 * u
        shoulder_y = hip_y - 3 * u
        neck_y = shoulder_y
        head_bottom_y = neck_y
        head_top_y = head_bottom_y - 2 * u

        # Color treatment based on category (Section 7.2)
        if category == "infantry":
            body_color = palette.shadow
            armor_color = palette.shadow
            accent_color = palette.accent  # For shields, weapons, jewelry
        elif category == "cavalry":
            body_color = palette.base
            armor_color = palette.highlight
            accent_color = palette.accent
        else:
            body_color = palette.base
            armor_color = palette.shadow
            accent_color = palette.accent

        # Shadow on ground
        shadow_rect = [center_x - 30, feet_y, center_x + 30, feet_y + 10]
        draw.ellipse(shadow_rect, fill=desaturate(body_color, 0.4))

        # Legs (isometric view - one forward, one back)
        # Back leg (darker, in shadow)
        back_leg_points = [
            (center_x - 15, hip_y),           # Hip
            (center_x - 20, knee_y),          # Knee
            (center_x - 25, feet_y),          # Foot
            (center_x - 10, feet_y),          # Foot base
            (center_x - 5, hip_y),            # Hip base
        ]
        draw.polygon(back_leg_points, fill=desaturate(body_color), outline=self.outline_color)

        # Front leg (lighter, in highlight)
        front_leg_points = [
            (center_x + 5, hip_y),            # Hip
            (center_x + 15, knee_y),          # Knee
            (center_x + 25, feet_y),          # Foot
            (center_x + 10, feet_y),          # Foot base
            (center_x - 5, hip_y),            # Hip base
        ]
        draw.polygon(front_leg_points, fill=lighten(body_color), outline=self.outline_color)

        # Torso (3 units tall)
        torso_width = 1.5 * u
        torso_points = [
            (center_x - torso_width // 2, hip_y),           # Bottom left
            (center_x + torso_width // 2, hip_y),           # Bottom right
            (center_x + torso_width // 2 - 5, shoulder_y),  # Top right
            (center_x - torso_width // 2 + 5, shoulder_y),  # Top left
        ]
        draw.polygon(torso_points, fill=body_color, outline=self.outline_color)

        # Arms (2 units each)
        # Back arm (holding weapon)
        back_arm_points = [
            (center_x - torso_width // 2 + 5, shoulder_y),  # Shoulder
            (center_x - torso_width // 2 - 10, shoulder_y + u),  # Elbow
            (center_x - torso_width // 2 - 5, shoulder_y + 2 * u),  # Hand
            (center_x - torso_width // 2 + 5, shoulder_y + 2 * u),  # Hand base
            (center_x - torso_width // 2 + 5, shoulder_y + u),  # Elbow base
        ]
        draw.polygon(back_arm_points, fill=desaturate(body_color), outline=self.outline_color)

        # Front arm (holding shield or weapon)
        front_arm_points = [
            (center_x + torso_width // 2 - 5, shoulder_y),  # Shoulder
            (center_x + torso_width // 2 + 10, shoulder_y + u),  # Elbow
            (center_x + torso_width // 2 + 15, shoulder_y + 2 * u),  # Hand
            (center_x + torso_width // 2 + 5, shoulder_y + 2 * u),  # Hand base
            (center_x + torso_width // 2 - 5, shoulder_y + u),  # Elbow base
        ]
        draw.polygon(front_arm_points, fill=lighten(body_color), outline=self.outline_color)

        # Head (2 units tall, oval-ish for isometric view)
        head_width = 1.2 * u
        head_height = 2 * u
        head_rect = [
            center_x - head_width // 2, head_top_y,
            center_x + head_width // 2, head_bottom_y
        ]
        draw.ellipse(head_rect, fill=lighten(armor_color), outline=self.outline_color)

        # Helmet/hair (if infantry)
        if category == "infantry":
            helmet_rect = [
                center_x - head_width // 2 - 5, head_top_y - 10,
                center_x + head_width // 2 + 5, head_top_y + 15
            ]
            draw.ellipse(helmet_rect, fill=armor_color, outline=self.outline_color)

    def draw_shield(self, draw: ImageDraw, center_x: int, center_y: int,
                   era: int, shield_type: str = "round") -> None:
        """Draw a shield for infantry enemies."""
        palette = ERA_PALETTES[era]

        if shield_type == "round":
            # Round shield (Greek style)
            shield_radius = 25
            shield_rect = [center_x - shield_radius, center_y - shield_radius,
                          center_x + shield_radius, center_y + shield_radius]
            draw.ellipse(shield_rect, fill=palette.shadow, outline=self.outline_color)
            # Accent pattern (spiral or cross)
            draw.ellipse([center_x - 10, center_y - 10, center_x + 10, center_y + 10],
                        fill=palette.accent, outline=self.outline_color)
        elif shield_type == "rectangular":
            # Rectangular shield (Roman style)
            shield_width = 40
            shield_height = 50
            shield_rect = [center_x - shield_width // 2, center_y - shield_height // 2,
                          center_x + shield_width // 2, center_y + shield_height // 2]
            draw.rectangle(shield_rect, fill=palette.shadow, outline=self.outline_color)
            # Accent stripe
            draw.rectangle([center_x - 3, center_y - shield_height // 2 + 5,
                          center_x + 3, center_y + shield_height // 2 - 5],
                         fill=palette.accent)

    def draw_spear(self, draw: ImageDraw, start_x: int, start_y: int,
                   angle: int = -30, era: int = 0) -> None:
        """Draw a spear weapon."""
        palette = ERA_PALETTES[era]
        shaft_length = 80
        end_x = start_x + int(shaft_length * (angle / 90))
        end_y = start_y + int(shaft_length * 0.5)

        # Shaft
        draw.line([start_x, start_y, end_x, end_y], fill=palette.stone_earth, width=4)

        # Spearhead
        spearhead_length = 20
        spearhead_points = [
            (end_x, end_y),
            (end_x + spearhead_length, end_y - 5),
            (end_x + spearhead_length, end_y + 5),
        ]
        draw.polygon(spearhead_points, fill=palette.accent, outline=self.outline_color)

    def generate_tribal_raider_infantry(self, era: int = 0) -> Image.Image:
        """
        Generate Tribal Raider Infantry sprite (Era 0: Ancient Colchis).
        - Category: Infantry
        - Colors: Shadow #1B3A26 (leather armor), Accent #D4A017 (jewelry)
        - Silhouette: Shield/spear shape
        """
        img = self.create_base_image()
        draw = ImageDraw.Draw(img)

        center_x = self.size // 2
        base_y = self.size - 100

        # Draw body
        self.draw_humanoid_body(draw, center_x, base_y, era, category="infantry")

        # Draw shield (in front arm)
        self.draw_shield(draw, center_x + 40, base_y - 1.5 * self.UNIT_SIZE, era, shield_type="round")

        # Draw spear (in back arm)
        self.draw_spear(draw, center_x - 50, base_y - 2 * self.UNIT_SIZE, angle=-20, era=era)

        # Gold jewelry (necklace) - accent color
        necklace_y = base_y - 3 * self.UNIT_SIZE - 10
        draw.arc([center_x - 15, necklace_y - 10, center_x + 15, necklace_y + 10],
                start=0, end=180, fill=ERA_PALETTES[era].accent, width=3)

        # Tribal armbands
        for i in range(2):
            arm_y = base_y - 2 * self.UNIT_SIZE + i * 20
            draw.arc([center_x + 20 + i * 10, arm_y - 8, center_x + 30 + i * 10, arm_y + 8],
                    start=0, end=360, fill=ERA_PALETTES[era].accent, width=2)

        return img

    def generate_greek_colonist_infantry(self, era: int = 0) -> Image.Image:
        """
        Generate Greek Colonist Infantry sprite (Era 0).
        - Category: Infantry
        - Colors: Base #2D5A3D (linen tunic), Accent #D4A017 (bronze)
        - Silhouette: Shield/spear shape with larger round shield
        """
        img = self.create_base_image()
        draw = ImageDraw.Draw(img)

        center_x = self.size // 2
        base_y = self.size - 100
        palette = ERA_PALETTES[era]

        # Draw body (with lighter tunic color)
        # Override body color for Greek style
        u = self.UNIT_SIZE
        feet_y = base_y
        hip_y = base_y - 3 * u
        shoulder_y = hip_y - 3 * u

        # Legs
        back_leg_points = [
            (center_x - 15, hip_y), (center_x - 20, hip_y - 1.5 * u), (center_x - 25, feet_y),
            (center_x - 10, feet_y), (center_x - 5, hip_y),
        ]
        draw.polygon(back_leg_points, fill=desaturate(palette.base), outline=self.outline_color)

        front_leg_points = [
            (center_x + 5, hip_y), (center_x + 15, hip_y - 1.5 * u), (center_x + 25, feet_y),
            (center_x + 10, feet_y), (center_x - 5, hip_y),
        ]
        draw.polygon(front_leg_points, fill=lighten(palette.base), outline=self.outline_color)

        # Torso (linen tunic)
        torso_width = 1.5 * u
        torso_points = [
            (center_x - torso_width // 2, hip_y),
            (center_x + torso_width // 2, hip_y),
            (center_x + torso_width // 2 - 5, shoulder_y),
            (center_x - torso_width // 2 + 5, shoulder_y),
        ]
        draw.polygon(torso_points, fill=palette.base, outline=self.outline_color)

        # Arms
        back_arm_points = [
            (center_x - torso_width // 2 + 5, shoulder_y),
            (center_x - torso_width // 2 - 10, shoulder_y + u),
            (center_x - torso_width // 2 - 5, shoulder_y + 2 * u),
            (center_x - torso_width // 2 + 5, shoulder_y + 2 * u),
            (center_x - torso_width // 2 + 5, shoulder_y + u),
        ]
        draw.polygon(back_arm_points, fill=palette.base, outline=self.outline_color)

        front_arm_points = [
            (center_x + torso_width // 2 - 5, shoulder_y),
            (center_x + torso_width // 2 + 10, shoulder_y + u),
            (center_x + torso_width // 2 + 15, shoulder_y + 2 * u),
            (center_x + torso_width // 2 + 5, shoulder_y + 2 * u),
            (center_x + torso_width // 2 - 5, shoulder_y + u),
        ]
        draw.polygon(front_arm_points, fill=lighten(palette.base), outline=self.outline_color)

        # Head
        head_width = 1.2 * u
        head_top_y = shoulder_y - 2 * u
        draw.ellipse([center_x - head_width // 2, head_top_y,
                     center_x + head_width // 2, shoulder_y],
                    fill=lighten(palette.base), outline=self.outline_color)

        # Greek helmet
        helmet_rect = [center_x - head_width // 2 - 5, head_top_y - 10,
                      center_x + head_width // 2 + 5, head_top_y + 15]
        draw.ellipse(helmet_rect, fill=palette.stone_earth, outline=self.outline_color)

        # Large round shield (aspis)
        shield_radius = 35
        shield_rect = [center_x + 30, shoulder_y + u - shield_radius,
                      center_x + 30 + shield_radius * 2, shoulder_y + u + shield_radius]
        draw.ellipse(shield_rect, fill=palette.stone_earth, outline=self.outline_color)
        # Bronze rim
        draw.ellipse([center_x + 30 + 3, shoulder_y + u - shield_radius + 3,
                     center_x + 30 + shield_radius * 2 - 3, shoulder_y + u + shield_radius - 3],
                    fill=palette.accent, outline=self.outline_color)

        # Spear (dory) - longer than tribal
        spear_length = 100
        end_x = center_x - 50
        end_y = shoulder_y + u + spear_length // 2
        draw.line([center_x - 50, shoulder_y + u, end_x, end_y],
                 fill=palette.stone_earth, width=4)
        # Spearhead
        spearhead_points = [
            (end_x, end_y), (end_x + 25, end_y - 7), (end_x + 25, end_y + 7),
        ]
        draw.polygon(spearhead_points, fill=palette.accent, outline=self.outline_color)

        return img

    def generate_enemy(self, enemy_type: str, era: int = 0) -> Image.Image:
        """Generate an enemy sprite by type."""
        generators = {
            "tribal_raider_infantry": self.generate_tribal_raider_infantry,
            "greek_colonist_infantry": self.generate_greek_colonist_infantry,
        }

        generator = generators.get(enemy_type, self.generate_tribal_raider_infantry)
        return generator(era)

if __name__ == "__main__":
    # Test: Generate Era 0 enemies
    gen = EnemyGenerator(size=512)

    # Tribal Raider Infantry
    tribal = gen.generate_enemy("tribal_raider_infantry", era=0)
    output_path = "/home/socraticblock/hermes-workspace/hermes/development/sakartvelo-defenders/assets/enemies/e00_colchis/ene_e00_tribal_raider_infantry_v01.png"
    tribal.save(output_path)
    print(f"✓ Generated tribal raider infantry")

    # Greek Colonist Infantry
    greek = gen.generate_enemy("greek_colonist_infantry", era=0)
    output_path = "/home/socraticblock/hermes-workspace/hermes/development/sakartvelo-defenders/assets/enemies/e00_colchis/ene_e00_greek_colonist_infantry_v01.png"
    greek.save(output_path)
    print(f"✓ Generated greek colonist infantry")
