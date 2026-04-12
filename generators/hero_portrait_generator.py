"""
Sakartvelo Defenders Hero Portrait Generator
Cel-shaded hero portraits following Art Style Guide Section 6
"""

from PIL import Image, ImageDraw, ImageFont
from sprite_generator import ERA_PALETTES, hex_to_rgb, lighten, desaturate
import math

class HeroPortraitGenerator:
    """Generate hero portraits following Art Style Guide Section 6."""

    def __init__(self, size: int = 1024):
        self.size = size
        self.outline_color = hex_to_rgb("#1A1A1A")
        self.outline_width = 3

    def create_base_image(self) -> Image.Image:
        """Create a new base image with era background."""
        return Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))

    def draw_gradient_background(self, draw: ImageDraw, era: int) -> None:
        """
        Draw a blurred, desaturated era palette gradient background.
        The hero's Accent color appears as a subtle radial glow behind the head.
        """
        palette = ERA_PALETTES[era]

        # Create gradient from sky color to base color
        sky_rgb = hex_to_rgb(palette.sky)
        base_rgb = hex_to_rgb(palette.base)

        # Simple vertical gradient
        for y in range(self.size):
            ratio = y / self.size
            r = int(sky_rgb[0] * (1 - ratio) + base_rgb[0] * ratio)
            g = int(sky_rgb[1] * (1 - ratio) + base_rgb[1] * ratio)
            b = int(sky_rgb[2] * (1 - ratio) + base_rgb[2] * ratio)
            # Desaturate by blending with gray
            avg = (r + g + b) // 3
            r = int(r * 0.6 + avg * 0.4)
            g = int(g * 0.6 + avg * 0.4)
            b = int(b * 0.6 + avg * 0.4)
            draw.line([(0, y), (self.size, y)], fill=(r, g, b, 255))

        # Radial glow of accent color behind head
        center_x = self.size // 2
        center_y = self.size // 2 - 50
        accent_rgb = hex_to_rgb(palette.accent)

        for radius in range(200, 0, -10):
            opacity = int((1 - radius / 200) * 50)  # Max 50% opacity
            draw.ellipse([center_x - radius, center_y - radius,
                         center_x + radius, center_y + radius],
                        fill=(accent_rgb[0], accent_rgb[1], accent_rgb[2], opacity))

    def draw_medea_portrait(self, era: int = 0) -> Image.Image:
        """
        Generate Medea portrait (Era 0: Ancient Colchis).
        - Half-body, three-quarter view
        - Expression: Calm, serene (support hero)
        - Era markers: Greek artifacts, gold jewelry
        - Background: #2D5A3D with #D4A017 radial glow
        """
        img = self.create_base_image()
        draw = ImageDraw.Draw(img)

        # Draw background
        self.draw_gradient_background(draw, era)

        palette = ERA_PALETTES[era]
        center_x = self.size // 2
        center_y = self.size // 2 + 50

        # Proportions for portrait (half-body)
        # Head: 120 units, Neck: 30 units, Torso: 200 units
        head_size = 120
        neck_height = 30
        torso_height = 200

        # Face positioning (upper third, centered horizontally)
        face_center_y = center_y - 150

        # ===== HEAD =====
        # Face (oval shape, three-quarter view)
        face_width = head_size
        face_height = head_size * 1.2

        # Main face shape
        face_points = [
            (center_x - face_width // 3, face_center_y - face_height // 2),  # Top left
            (center_x + face_width // 2, face_center_y - face_height // 2 + 20),  # Top right
            (center_x + face_width // 2, face_center_y + face_height // 2 - 10),  # Bottom right
            (center_x - face_width // 2, face_center_y + face_height // 2),  # Bottom left
            (center_x - face_width // 2, face_center_y),  # Cheek
        ]
        draw.polygon(face_points, fill=lighten(palette.base), outline=self.outline_color)

        # Hair (long, dark, flowing)
        hair_color = desaturate(palette.shadow)
        hair_points = [
            (center_x - face_width // 2 - 20, face_center_y - face_height // 2 + 10),
            (center_x + face_width // 2 + 10, face_center_y - face_height // 2 + 30),
            (center_x + face_width // 2 + 20, face_center_y + 20),
            (center_x + face_width // 2 + 15, face_center_y + face_height // 2),
            (center_x, face_center_y + face_height // 2 + 30),
            (center_x - face_width // 2, face_center_y + face_height // 2),
            (center_x - face_width // 2 - 15, face_center_y + 20),
        ]
        draw.polygon(hair_points, fill=hair_color, outline=self.outline_color)

        # Hair strands (detailed)
        for i in range(5):
            strand_x = center_x - face_width // 2 + i * 15
            strand_y = face_center_y + face_height // 2
            draw.line([(strand_x, strand_y), (strand_x + 10, strand_y + 40)],
                     fill=hair_color, width=3)

        # ===== FACIAL FEATURES =====
        # Eyes (calm, serene expression)
        eye_y = face_center_y - 20
        eye_spacing = 35

        # Left eye (more visible in three-quarter view)
        left_eye_x = center_x - eye_spacing // 2
        draw.ellipse([left_eye_x - 12, eye_y - 8, left_eye_x + 12, eye_y + 8],
                    fill=lighten(palette.shadow), outline=self.outline_color)
        # Pupil
        draw.ellipse([left_eye_x - 4, eye_y - 4, left_eye_x + 4, eye_y + 4],
                    fill=(0, 0, 0, 255), outline=None)

        # Right eye (slightly smaller, angled)
        right_eye_x = center_x + eye_spacing // 2 + 10
        draw.ellipse([right_eye_x - 10, eye_y - 7, right_eye_x + 10, eye_y + 7],
                    fill=lighten(palette.shadow), outline=self.outline_color)
        draw.ellipse([right_eye_x - 3, eye_y - 3, right_eye_x + 3, eye_y + 3],
                    fill=(0, 0, 0, 255), outline=None)

        # Eyebrows (gently arched, serene)
        draw.line([(left_eye_x - 15, eye_y - 15), (left_eye_x + 5, eye_y - 18)],
                 fill=hair_color, width=4)
        draw.line([(right_eye_x - 5, eye_y - 18), (right_eye_x + 15, eye_y - 15)],
                 fill=hair_color, width=4)

        # Nose (subtle, refined)
        nose_tip_x = center_x + 5
        nose_tip_y = face_center_y + 10
        draw.line([(center_x, eye_y + 5), (nose_tip_x, nose_tip_y)],
                 fill=desaturate(palette.base), width=2)
        # Nose shadow
        draw.ellipse([nose_tip_x - 8, nose_tip_y - 5, nose_tip_x + 5, nose_tip_y + 8],
                    fill=desaturate(palette.base), outline=None)

        # Mouth (slight, serene smile)
        mouth_y = face_center_y + 40
        mouth_x = center_x + 5
        draw.arc([mouth_x - 15, mouth_y - 8, mouth_x + 20, mouth_y + 5],
                start=170, end=350, fill=desaturate(palette.shadow), width=3)

        # ===== NECK =====
        neck_width = 60
        neck_top = face_center_y + face_height // 2 - 5
        neck_bottom = neck_top + neck_height

        neck_points = [
            (center_x - neck_width // 2, neck_top),
            (center_x + neck_width // 2 - 10, neck_top),
            (center_x + neck_width // 2, neck_bottom),
            (center_x - neck_width // 2 + 10, neck_bottom),
        ]
        draw.polygon(neck_points, fill=lighten(palette.base), outline=self.outline_color)

        # ===== TORSO & ROBES =====
        torso_top = neck_bottom
        torso_bottom = torso_top + torso_height
        torso_width = 300

        # Main robe (flowing)
        robe_points = [
            (center_x - torso_width // 2, torso_top),
            (center_x + torso_width // 2 - 30, torso_top),
            (center_x + torso_width // 2, torso_bottom),
            (center_x, torso_bottom + 30),
            (center_x - torso_width // 2, torso_bottom),
        ]
        draw.polygon(robe_points, fill=palette.base, outline=self.outline_color)

        # Robe folds (cel-shaded)
        fold_colors = [lighten(palette.base), desaturate(palette.base)]
        for i, (fold_x, fold_color) in enumerate(zip(
            [center_x - 80, center_x, center_x + 70],
            fold_colors
        )):
            fold_points = [
                (fold_x, torso_top + 20),
                (fold_x + 10, torso_top + 150),
                (fold_x - 5, torso_bottom),
                (fold_x - 15, torso_top + 150),
            ]
            draw.polygon(fold_points, fill=fold_color, outline=self.outline_color)

        # ===== GOLD JEWELRY (Accent Color) =====
        # Necklace (multiple strands)
        necklace_y = neck_bottom + 20
        for i in range(3):
            strand_y = necklace_y + i * 8
            draw.arc([center_x - 60, strand_y - 15, center_x + 60, strand_y + 15],
                    start=0, end=180, fill=palette.accent, width=3 + i)

        # Pendant (Greek artifact - amulet)
        pendant_x = center_x
        pendant_y = necklace_y + 30
        pendant_points = [
            (pendant_x, pendant_y - 15),
            (pendant_x + 12, pendant_y),
            (pendant_x, pendant_y + 15),
            (pendant_x - 12, pendant_y),
        ]
        draw.polygon(pendant_points, fill=palette.accent, outline=self.outline_color)
        # Inner detail
        draw.ellipse([pendant_x - 5, pendant_y - 5, pendant_x + 5, pendant_y + 5],
                    fill=lighten(palette.accent), outline=self.outline_color)

        # Armbands
        armband_y = torso_top + 60
        for i in range(2):
            armband_x = center_x - 80 + i * 160
            draw.ellipse([armband_x - 15, armband_y - 8, armband_x + 15, armband_y + 8],
                        fill=palette.accent, outline=self.outline_color)
            # Decorative pattern
            draw.ellipse([armband_x - 8, armband_y - 4, armband_x + 8, armband_y + 4],
                        fill=lighten(palette.accent), outline=None)

        # Headband/crown (golden)
        headband_y = face_center_y - face_height // 2 + 15
        draw.line([(center_x - 50, headband_y), (center_x + 50, headband_y)],
                 fill=palette.accent, width=6)
        # Center jewel
        draw.ellipse([center_x - 10, headband_y - 8, center_x + 10, headband_y + 8],
                    fill=palette.accent, outline=self.outline_color)
        draw.ellipse([center_x - 5, headband_y - 3, center_x + 5, headband_y + 3],
                    fill=lighten(palette.accent), outline=None)

        # ===== ERA MARKERS (Background Elements) =====
        # Ancient Vani ruins (subtle in background)
        ruin_color = desaturate(palette.stone_earth)
        ruin_x = self.size - 150
        ruin_y = self.size - 100

        # Pillar
        draw.rectangle([ruin_x, ruin_y - 100, ruin_x + 30, ruin_y],
                      fill=ruin_color, outline=self.outline_color)
        # Column capital
        draw.ellipse([ruin_x - 10, ruin_y - 115, ruin_x + 40, ruin_y - 95],
                    fill=ruin_color, outline=self.outline_color)

        # Another pillar (more faded)
        draw.rectangle([ruin_x - 50, ruin_y - 80, ruin_x - 30, ruin_y + 20],
                      fill=ruin_color, outline=self.outline_color)

        return img

    def generate_hero_portrait(self, hero_name: str, era: int = 0) -> Image.Image:
        """Generate a hero portrait by name."""
        generators = {
            "medea": self.draw_medea_portrait,
        }

        generator = generators.get(hero_name.lower(), self.draw_medea_portrait)
        return generator(era)

if __name__ == "__main__":
    # Test: Generate Medea portrait (Era 0)
    gen = HeroPortraitGenerator(size=1024)
    medea = gen.generate_hero_portrait("medea", era=0)
    output_path = "/home/socraticblock/hermes-workspace/hermes/development/sakartvelo-defenders/assets/heroes/e00_colchis/her_e00_medea_v01.png"
    medea.save(output_path)
    print(f"✓ Generated Medea portrait (1024x1024)")
