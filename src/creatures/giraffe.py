import math
import random
from PIL import Image, ImageDraw
from ..github_api import hex_to_rgba

def render_giraffe(stats, output_path="dist/giraffe.gif", frame_count=20):
    commits = stats.get("contributions", 900)
    languages = stats.get("languages", {})
    username = stats.get("username", "Nightkilller")

    body_color = (245, 196, 90, 255)
    body_shadow = (220, 168, 65, 255)
    hoof_color = (55, 40, 30, 255)
    mane_color = (130, 75, 40, 255)
    muzzle_color = (250, 220, 185, 255)
    eye_color = (35, 25, 20, 255)
    leaf_green = (76, 175, 80, 255)
    stem_color = (139, 90, 43, 255)
    cloud_color = (255, 255, 255, 170)

    lang_colors = [hex_to_rgba(c, 240) for c in languages.values()] or [(180, 100, 50, 240)]

    # Neck length scales with logarithmic commits: 45px up to 150px
    neck_length = min(150, max(50, int(42 + 12.5 * math.log(max(1, commits)))))

    canvas_w = 260
    canvas_h = int(175 + neck_length)
    ground_y = canvas_h - 22

    body_center_x = 90
    body_center_y = ground_y - 45
    shoulder_x = body_center_x + 35
    shoulder_y = body_center_y - 12
    hip_x = body_center_x - 35
    hip_y = body_center_y + 5

    rng = random.Random(sum(ord(c) for c in username))
    body_spots = []
    for _ in range(15):
        sx = rng.randint(body_center_x - 32, body_center_x + 26)
        sy = rng.randint(body_center_y - 12, body_center_y + 14)
        sr = rng.randint(5, 8)
        sc = rng.choice(lang_colors)
        body_spots.append((sx, sy, sr, sc))

    neck_spots_dist = []
    num_neck_spots = max(6, int(neck_length / 14))
    for i in range(num_neck_spots):
        t_val = 0.12 + (i / num_neck_spots) * 0.78
        side = -4 if i % 2 == 0 else 3
        sc = rng.choice(lang_colors)
        neck_spots_dist.append((t_val, side, rng.randint(4, 6), sc))

    frames = []
    for f in range(frame_count):
        img = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        phase = (f / frame_count) * 2 * math.pi
        sway = math.sin(phase) * 6.5
        tail_sway = math.sin(phase * 2) * 8.5
        chew = math.sin(phase * 4) * 2.0

        if neck_length > 95:
            cx = 210 + math.sin(phase * 0.5) * 4
            cy = 35
            draw.ellipse([cx - 20, cy - 8, cx + 20, cy + 8], fill=cloud_color)
            draw.ellipse([cx - 10, cy - 14, cx + 10, cy + 6], fill=cloud_color)

        # Back Legs
        draw.rectangle([hip_x - 8, hip_y, hip_x - 2, ground_y], fill=body_shadow)
        draw.rectangle([hip_x - 8, ground_y - 6, hip_x - 2, ground_y], fill=hoof_color)
        draw.rectangle([shoulder_x - 14, shoulder_y + 5, shoulder_x - 8, ground_y], fill=body_shadow)
        draw.rectangle([shoulder_x - 14, ground_y - 6, shoulder_x - 8, ground_y], fill=hoof_color)

        # Tail
        tail_start = (hip_x - 25, hip_y - 2)
        tail_end = (hip_x - 35 + tail_sway, hip_y + 28)
        draw.line([tail_start, tail_end], fill=body_shadow, width=3)
        draw.ellipse([tail_end[0] - 4, tail_end[1] - 4, tail_end[0] + 4, tail_end[1] + 4], fill=mane_color)

        # Torso
        torso = [
            (shoulder_x, shoulder_y - 12),
            (shoulder_x + 8, shoulder_y + 12),
            (hip_x, hip_y + 16),
            (hip_x - 24, hip_y - 4),
            (shoulder_x - 15, shoulder_y - 15),
        ]
        draw.polygon(torso, fill=body_color)
        draw.chord([body_center_x - 35, body_center_y - 15, body_center_x + 35, body_center_y + 20], 0, 360, fill=body_color)

        for sx, sy, sr, sc in body_spots:
            draw.ellipse([sx - sr, sy - sr * 0.8, sx + sr, sy + sr * 0.8], fill=sc, outline=body_shadow)

        # Front Legs
        draw.rectangle([hip_x + 4, hip_y + 2, hip_x + 10, ground_y], fill=body_color)
        draw.rectangle([hip_x + 4, ground_y - 6, hip_x + 10, ground_y], fill=hoof_color)
        draw.rectangle([shoulder_x - 2, shoulder_y + 6, shoulder_x + 4, ground_y], fill=body_color)
        draw.rectangle([shoulder_x - 2, ground_y - 6, shoulder_x + 4, ground_y], fill=hoof_color)

        # Neck
        neck_front = []
        neck_back = []
        neck_spine = []
        segs = 18
        for i in range(segs + 1):
            t = i / segs
            dx = (t ** 1.3) * sway
            seg_x = shoulder_x + (t * 22) + dx
            seg_y = shoulder_y - (t * neck_length)
            neck_spine.append((seg_x, seg_y))

            half_w = 9.5 - (t * 3.5)
            neck_front.append((seg_x + half_w, seg_y))
            neck_back.append((seg_x - half_w, seg_y))

        for i in range(len(neck_back) - 1):
            bx, by = neck_back[i]
            draw.rectangle([bx - 4, by - 2, bx, by + 4], fill=mane_color)

        draw.polygon(neck_front + list(reversed(neck_back)), fill=body_color)

        for t_val, lateral_offset, spot_r, spot_col in neck_spots_dist:
            idx = int(t_val * segs)
            if 0 <= idx < len(neck_spine):
                cx, cy = neck_spine[idx]
                draw.ellipse([cx + lateral_offset - spot_r, cy - spot_r, cx + lateral_offset + spot_r, cy + spot_r], fill=spot_col, outline=body_shadow)

        # Head
        head_x, head_y = neck_spine[-1]
        ear_sway = math.sin(phase - 0.5) * 2
        draw.polygon([(head_x - 6, head_y - 2), (head_x - 14, head_y - 6 + ear_sway), (head_x - 8, head_y + 3)], fill=body_shadow)
        draw.polygon([(head_x - 2, head_y - 3), (head_x - 10, head_y - 8 + ear_sway), (head_x - 4, head_y + 2)], fill=body_color)

        draw.line([(head_x + 1, head_y - 6), (head_x + 3, head_y - 15)], fill=body_shadow, width=2)
        draw.ellipse([head_x + 1, head_y - 18, head_x + 5, head_y - 13], fill=mane_color)
        draw.line([(head_x + 6, head_y - 6), (head_x + 9, head_y - 15)], fill=body_color, width=2)
        draw.ellipse([head_x + 7, head_y - 18, head_x + 11, head_y - 13], fill=mane_color)

        draw.ellipse([head_x - 4, head_y - 8, head_x + 16, head_y + 8], fill=body_color)

        muzzle_x = head_x + 14
        muzzle_y = head_y + 1 + chew
        draw.rounded_rectangle([muzzle_x - 4, muzzle_y - 4, muzzle_x + 10, muzzle_y + 7], radius=4, fill=muzzle_color)
        draw.ellipse([muzzle_x + 6, muzzle_y - 1, muzzle_x + 8, muzzle_y + 1], fill=eye_color)

        draw.ellipse([head_x + 7, head_y - 3, head_x + 11, head_y + 2], fill=eye_color)
        draw.point((head_x + 8, head_y - 2), fill=(255, 255, 255, 255))

        twig_x = muzzle_x + 4
        twig_y = muzzle_y + 3
        draw.line([(twig_x, twig_y), (twig_x + 13, twig_y + 4)], fill=stem_color, width=2)
        draw.ellipse([twig_x + 10, twig_y + 1, twig_x + 16, twig_y + 5], fill=leaf_green)
        draw.ellipse([twig_x + 12, twig_y + 4, twig_x + 18, twig_y + 8], fill=leaf_green)

        frames.append(img)

    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=65, loop=0, disposal=2)
    return output_path
