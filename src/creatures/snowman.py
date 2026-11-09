import math
import random
from PIL import Image, ImageDraw
from ..github_api import hex_to_rgba

def render_snowman(stats, output_path="dist/snowman.gif", frame_count=20):
    commits = stats.get("contributions", 900)
    languages = stats.get("languages", {})
    username = stats.get("username", "Frosty")

    # Colors
    snow_white = (245, 250, 255, 255)
    snow_shadow = (205, 225, 245, 255)
    coal_black = (40, 40, 45, 255)
    carrot_orange = (245, 120, 30, 255)
    hat_black = (30, 30, 35, 255)
    hat_ribbon = (220, 50, 50, 255)
    twig_brown = (110, 70, 35, 255)

    lang_list = list(languages.values())
    if lang_list:
        hat_ribbon = hex_to_rgba(lang_list[0])
    scarf_colors = [hex_to_rgba(c) for c in lang_list] or [(220, 50, 50, 255), (40, 120, 220, 255)]

    # Bottom snowball diameter scales with commits: 38px up to 90px
    base_radius = min(48, max(20, int(18 + 5.5 * math.log(max(1, commits)))))
    mid_radius = int(base_radius * 0.75)
    head_radius = int(base_radius * 0.55)

    canvas_w = 260
    canvas_h = int(base_radius * 2 + mid_radius * 1.6 + head_radius * 2 + 55)
    ground_y = canvas_h - 15

    center_x = 130
    base_y = ground_y - base_radius
    mid_y = base_y - int(base_radius * 0.85) - int(mid_radius * 0.85)
    head_y = mid_y - int(mid_radius * 0.85) - head_radius

    # Pre-generate 35 falling snowflakes
    rng = random.Random(sum(ord(c) for c in username) + 7)
    snowflakes = []
    for _ in range(35):
        sx = rng.randint(5, canvas_w - 5)
        sy = rng.randint(0, canvas_h)
        speed = rng.uniform(2.5, 4.5)
        flake_r = rng.uniform(1.2, 2.5)
        snowflakes.append({"x": sx, "y": sy, "speed": speed, "r": flake_r})

    frames = []
    for f in range(frame_count):
        img = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        phase = (f / frame_count) * 2 * math.pi
        arm_wave = math.sin(phase) * 6.0
        scarf_flutter = math.sin(phase * 1.5) * 5.0

        # Falling Snowflakes
        for flake in snowflakes:
            fy = (flake["y"] + f * flake["speed"]) % canvas_h
            fx = flake["x"] + math.sin(phase + flake["y"]) * 2.0
            r = flake["r"]
            draw.ellipse([fx - r, fy - r, fx + r, fy + r], fill=(230, 245, 255, 200))

        # Ground snowdrift
        draw.chord([center_x - 110, ground_y - 12, center_x + 110, ground_y + 16], 0, 360, fill=snow_shadow)
        draw.chord([center_x - 90, ground_y - 8, center_x + 90, ground_y + 12], 0, 360, fill=snow_white)

        # 1. Bottom Snowball (Scales with contributions!)
        draw.ellipse([center_x - base_radius, base_y - base_radius, center_x + base_radius, base_y + base_radius], fill=snow_shadow)
        draw.ellipse([center_x - base_radius + 3, base_y - base_radius + 2, center_x + base_radius - 2, base_y + base_radius - 4], fill=snow_white)

        # 2. Middle Snowball
        draw.ellipse([center_x - mid_radius, mid_y - mid_radius, center_x + mid_radius, mid_y + mid_radius], fill=snow_shadow)
        draw.ellipse([center_x - mid_radius + 2, mid_y - mid_radius + 2, center_x + mid_radius - 2, mid_y + mid_radius - 3], fill=snow_white)

        # Coal buttons on belly
        draw.ellipse([center_x - 3, mid_y - 6, center_x + 3, mid_y], fill=coal_black)
        draw.ellipse([center_x - 3, mid_y + 6, center_x + 3, mid_y + 12], fill=coal_black)

        # Twig Arms (branching)
        # Left Arm
        draw.line([(center_x - mid_radius + 2, mid_y), (center_x - mid_radius - 25, mid_y - 14 + arm_wave)], fill=twig_brown, width=3)
        draw.line([(center_x - mid_radius - 18, mid_y - 10 + arm_wave * 0.7), (center_x - mid_radius - 22, mid_y - 20 + arm_wave)], fill=twig_brown, width=2)
        # Right Arm (waving)
        draw.line([(center_x + mid_radius - 2, mid_y), (center_x + mid_radius + 26, mid_y - 18 - arm_wave)], fill=twig_brown, width=3)
        draw.line([(center_x + mid_radius + 18, mid_y - 13 - arm_wave * 0.7), (center_x + mid_radius + 22, mid_y - 24 - arm_wave)], fill=twig_brown, width=2)

        # 3. Head Snowball
        draw.ellipse([center_x - head_radius, head_y - head_radius, center_x + head_radius, head_y + head_radius], fill=snow_shadow)
        draw.ellipse([center_x - head_radius + 2, head_y - head_radius + 2, center_x + head_radius - 2, head_y + head_radius - 2], fill=snow_white)

        # Striped Language Scarf around neck
        scarf_y = head_y + head_radius - 4
        scarf_w = head_radius * 1.5
        draw.rounded_rectangle([center_x - scarf_w / 2, scarf_y - 4, center_x + scarf_w / 2, scarf_y + 5], radius=3, fill=scarf_colors[0])
        # Scarf stripes
        for idx, col in enumerate(scarf_colors[:4]):
            sx_pos = (center_x - scarf_w / 2) + idx * 8 + 3
            draw.rectangle([sx_pos, scarf_y - 4, sx_pos + 4, scarf_y + 5], fill=col)

        # Scarf tail fluttering in wind
        tail_tip_x = center_x + scarf_w / 2 + 16 + scarf_flutter
        tail_tip_y = scarf_y + 18
        draw.polygon([
            (center_x + scarf_w / 2 - 4, scarf_y + 1),
            (center_x + scarf_w / 2 + 6, scarf_y + 2),
            (tail_tip_x, tail_tip_y),
            (tail_tip_x - 8, tail_tip_y + 2),
        ], fill=scarf_colors[0])

        # Eyes
        draw.ellipse([center_x - 8, head_y - 5, center_x - 3, head_y], fill=coal_black)
        draw.ellipse([center_x + 3, head_y - 5, center_x + 8, head_y], fill=coal_black)

        # Carrot Nose (sticking out)
        draw.polygon([(center_x, head_y - 1), (center_x + 16, head_y + 3), (center_x, head_y + 4)], fill=carrot_orange)

        # Coal Smile
        for angle in [-25, -12, 0, 12, 25]:
            rad = math.radians(angle)
            mx = center_x + int(math.sin(rad) * 12)
            my = head_y + 7 + int(math.cos(rad) * 4)
            draw.ellipse([mx - 1.5, my - 1.5, mx + 1.5, my + 1.5], fill=coal_black)

        # Top Hat
        hat_bottom_y = head_y - head_radius + 4
        brim_w = head_radius * 1.7
        draw.rounded_rectangle([center_x - brim_w / 2, hat_bottom_y - 3, center_x + brim_w / 2, hat_bottom_y + 3], radius=2, fill=hat_black)
        top_w = head_radius * 1.1
        draw.rectangle([center_x - top_w / 2, hat_bottom_y - 24, center_x + top_w / 2, hat_bottom_y - 3], fill=hat_black)
        # Language ribbon around hat
        draw.rectangle([center_x - top_w / 2, hat_bottom_y - 9, center_x + top_w / 2, hat_bottom_y - 3], fill=hat_ribbon)

        frames.append(img)

    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=65, loop=0, disposal=2)
    return output_path

