import math
from PIL import Image, ImageDraw
from ..github_api import hex_to_rgba

def render_buffalo(stats, output_path="dist/buffalo.gif", frame_count=20):
    commits = stats.get("contributions", 900)
    languages = stats.get("languages", {})

    # Colors
    buffalo_dark = (38, 38, 42, 255)
    buffalo_shadow = (25, 25, 28, 255)
    horn_gray = (110, 115, 120, 255)
    horn_highlight = (160, 165, 170, 255)
    hoof_black = (18, 18, 20, 255)
    muzzle_gray = (65, 65, 72, 255)
    can_silver = (210, 218, 225, 255)
    can_shadow = (150, 160, 170, 255)
    can_lid = (180, 190, 200, 255)
    grass_green = (46, 125, 50, 255)

    lang_colors = [hex_to_rgba(c) for c in languages.values()] or [
        (241, 224, 90, 255), (49, 120, 198, 255), (53, 114, 165, 255)
    ]

    # Milk cans count: 1 can per 100 commits, max 10 cans
    milk_cans = min(10, max(1, int(commits / 100)))

    canvas_w = 280
    canvas_h = 160
    ground_y = canvas_h - 22

    # Buffalo position
    buf_x = 110
    buf_y = ground_y - 48

    frames = []
    for f in range(frame_count):
        img = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        phase = (f / frame_count) * 2 * math.pi
        chew_offset = math.sin(phase * 4) * 2.0
        tail_wag = math.sin(phase * 2) * 7.0
        breath_y = math.sin(phase) * 1.2

        # Ground grass tufts
        for gx in range(10, canvas_w, 24):
            draw.line([(gx, ground_y), (gx + 3, ground_y - 4)], fill=grass_green, width=2)
            draw.line([(gx + 4, ground_y), (gx + 7, ground_y - 6)], fill=grass_green, width=2)

        # 1. Buffalo Back Legs
        for lx in [buf_x - 30, buf_x + 22]:
            draw.rectangle([lx - 4, buf_y + 12, lx + 2, ground_y], fill=buffalo_shadow)
            draw.rectangle([lx - 4, ground_y - 5, lx + 2, ground_y], fill=hoof_black)

        # 2. Tail with brush tuft
        tail_start = (buf_x - 42, buf_y + 2)
        tail_end = (buf_x - 55 + tail_wag, buf_y + 32)
        draw.line([tail_start, tail_end], fill=buffalo_dark, width=3)
        draw.ellipse([tail_end[0] - 4, tail_end[1] - 4, tail_end[0] + 4, tail_end[1] + 4], fill=buffalo_shadow)

        # 3. Buffalo Heavy Torso
        torso_box = [buf_x - 44, buf_y - 12 - breath_y, buf_x + 32, buf_y + 24 - breath_y]
        draw.rounded_rectangle(torso_box, radius=12, fill=buffalo_dark)
        # Hump on back
        draw.chord([buf_x - 14, buf_y - 22 - breath_y, buf_x + 18, buf_y - 2 - breath_y], 0, 360, fill=buffalo_dark)

        # 4. Front Legs
        for lx in [buf_x - 22, buf_x + 30]:
            draw.rectangle([lx - 3, buf_y + 14, lx + 3, ground_y], fill=buffalo_dark)
            draw.rectangle([lx - 3, ground_y - 5, lx + 3, ground_y], fill=hoof_black)

        # 5. Buffalo Head & Horns
        head_x = buf_x + 46
        head_y = buf_y - 8 - breath_y

        # Curved Water Buffalo Horns (sweeping backward and curling)
        # Left horn
        draw.arc([head_x - 22, head_y - 26, head_x + 4, head_y - 2], 120, 300, fill=horn_gray, width=4)
        draw.arc([head_x - 20, head_y - 28, head_x + 2, head_y - 4], 140, 280, fill=horn_highlight, width=2)
        # Right horn
        draw.arc([head_x - 4, head_y - 26, head_x + 22, head_y - 2], 240, 60, fill=horn_gray, width=4)
        draw.arc([head_x - 2, head_y - 28, head_x + 20, head_y - 4], 260, 40, fill=horn_highlight, width=2)

        # Head Skull
        draw.rounded_rectangle([head_x - 10, head_y - 12, head_x + 16, head_y + 14], radius=6, fill=buffalo_dark)

        # Muzzle with chewing animation
        muzzle_x = head_x + 10
        muzzle_y = head_y + 2 + chew_offset
        draw.rounded_rectangle([muzzle_x - 4, muzzle_y - 3, muzzle_x + 12, muzzle_y + 9], radius=4, fill=muzzle_gray)
        # Nostrils
        draw.ellipse([muzzle_x + 6, muzzle_y + 1, muzzle_x + 8, muzzle_y + 4], fill=(15, 15, 18, 255))
        # Straw / grass in mouth
        draw.line([(muzzle_x + 4, muzzle_y + 5), (muzzle_x + 16, muzzle_y + 9)], fill=(120, 200, 80, 255), width=2)

        # Ears
        draw.polygon([(head_x - 6, head_y - 4), (head_x - 14, head_y + 4), (head_x - 4, head_y + 4)], fill=buffalo_shadow)
        draw.polygon([(head_x + 6, head_y - 4), (head_x + 14, head_y + 4), (head_x + 4, head_y + 4)], fill=buffalo_dark)

        # Eye
        draw.ellipse([head_x + 3, head_y - 4, head_x + 7, head_y], fill=(15, 15, 18, 255))
        draw.point((head_x + 4, head_y - 3), fill=(255, 255, 255, 255))

        # 6. Milk Cans Lined Up on the Left (1 can per 100 commits!)
        can_w = 14
        can_h = 24
        # Two rows of stacking if > 5 cans
        start_can_x = 18
        for i in range(milk_cans):
            row = 0 if i < 6 else 1
            col = i if i < 6 else (i - 6)
            cx = start_can_x + col * (can_w + 4)
            cy = ground_y - can_h - (row * (can_h + 2))

            # Milk can body
            draw.rounded_rectangle([cx, cy + 4, cx + can_w, cy + can_h], radius=2, fill=can_silver, outline=can_shadow)
            # Neck & Lid
            draw.rectangle([cx + 3, cy + 1, cx + can_w - 3, cy + 4], fill=can_lid)
            draw.ellipse([cx + 2, cy - 2, cx + can_w - 2, cy + 2], fill=can_lid, outline=can_shadow)
            # Side handle
            draw.arc([cx - 3, cy + 6, cx + 3, cy + 14], 90, 270, fill=can_shadow, width=2)
            draw.arc([cx + can_w - 3, cy + 6, cx + can_w + 3, cy + 14], 270, 90, fill=can_shadow, width=2)

            # Language badge / colored band around the milk can
            band_col = lang_colors[i % len(lang_colors)]
            draw.rectangle([cx + 1, cy + 11, cx + can_w - 1, cy + 15], fill=band_col)

        frames.append(img)

    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=65, loop=0, disposal=2)
    return output_path

