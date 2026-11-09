import math
from PIL import Image, ImageDraw
from ..github_api import hex_to_rgba

def render_monkey_tree(stats, output_path="dist/monkey_tree.gif", frame_count=20):
    commits = stats.get("contributions", 900)
    languages = stats.get("languages", {})

    trunk_brown = (101, 67, 33, 255)
    bark_shadow = (75, 48, 22, 255)
    leaf_green = (46, 125, 50, 255)
    leaf_light = (76, 175, 80, 255)
    monkey_brown = (139, 69, 19, 255)
    monkey_face = (255, 218, 185, 255)
    banana_yellow = (255, 215, 0, 255)

    lang_colors = [hex_to_rgba(c) for c in languages.values()] or [
        (241, 224, 90, 255), (49, 120, 198, 255), (53, 114, 165, 255)
    ]

    # Tree height scales with commits: 55px up to 145px
    tree_height = min(150, max(55, int(45 + 13 * math.log(max(1, commits)))))

    canvas_w = 260
    canvas_h = int(140 + tree_height)
    ground_y = canvas_h - 18

    tree_x = 90
    canopy_y = ground_y - tree_height

    frames = []
    for f in range(frame_count):
        img = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        phase = (f / frame_count) * 2 * math.pi
        branch_sway = math.sin(phase) * 3.0
        # Monkey swing cycle (parabolic swing arc)
        swing_angle = math.sin(phase) * 0.45

        # Ground grass
        draw.chord([tree_x - 60, ground_y - 8, tree_x + 60, ground_y + 12], 0, 360, fill=(34, 139, 34, 255))

        # 1. Tree Trunk (tapering upward)
        trunk_poly = [
            (tree_x - 14, ground_y),
            (tree_x + 14, ground_y),
            (tree_x + 8, canopy_y + 20),
            (tree_x - 8, canopy_y + 20),
        ]
        draw.polygon(trunk_poly, fill=trunk_brown)
        draw.line([(tree_x - 2, ground_y - 5), (tree_x - 1, canopy_y + 25)], fill=bark_shadow, width=2)

        # 2. Branches
        # Left Branch
        draw.line([(tree_x - 6, canopy_y + 35), (tree_x - 45, canopy_y + 22 + branch_sway * 0.5)], fill=trunk_brown, width=6)
        # Right Long Branch (where monkey hangs!)
        branch_tip_x = tree_x + 60
        branch_tip_y = canopy_y + 25 + branch_sway
        draw.line([(tree_x + 6, canopy_y + 38), (branch_tip_x, branch_tip_y)], fill=trunk_brown, width=6)

        # 3. Lush Canopy (Cloud of leafy circles)
        canopy_clusters = [
            (tree_x - 35, canopy_y + 10, 26),
            (tree_x + 35, canopy_y + 12, 28),
            (tree_x, canopy_y - 12, 34),
            (tree_x - 18, canopy_y - 2, 28),
            (tree_x + 18, canopy_y - 2, 28),
        ]
        for cx, cy, cr in canopy_clusters:
            draw.ellipse([cx - cr, cy - cr + branch_sway * 0.4, cx + cr, cy + cr + branch_sway * 0.4], fill=leaf_green)
            draw.ellipse([cx - cr + 3, cy - cr + 3 + branch_sway * 0.4, cx + cr - 4, cy + cr - 4 + branch_sway * 0.4], fill=leaf_light)

        # Language Fruit hanging on the tree
        for i, col in enumerate(lang_colors[:5]):
            fx = tree_x - 30 + i * 16
            fy = canopy_y + 8 + (i % 2) * 12 + branch_sway * 0.5
            draw.ellipse([fx - 4, fy - 4, fx + 4, fy + 4], fill=col, outline=(30, 30, 30, 180))

        # 4. The Monkey (swinging from the right branch)
        anchor_x = branch_tip_x - 12
        anchor_y = branch_tip_y
        arm_len = 28
        monkey_center_x = anchor_x + math.sin(swing_angle) * arm_len
        monkey_center_y = anchor_y + math.cos(swing_angle) * arm_len

        # Monkey Hanging Arm
        draw.line([(anchor_x, anchor_y), (monkey_center_x, monkey_center_y - 10)], fill=monkey_brown, width=3)

        # Monkey Body
        draw.ellipse([monkey_center_x - 8, monkey_center_y - 8, monkey_center_x + 8, monkey_center_y + 10], fill=monkey_brown)

        # Prehensile Curling Tail
        tail_tip_x = monkey_center_x - 14 - math.sin(phase * 2) * 5
        tail_tip_y = monkey_center_y + 4 + math.cos(phase * 2) * 5
        draw.line([(monkey_center_x - 5, monkey_center_y + 6), (monkey_center_x - 12, monkey_center_y + 8), (tail_tip_x, tail_tip_y)], fill=monkey_brown, width=3)

        # Monkey Legs
        draw.line([(monkey_center_x - 4, monkey_center_y + 8), (monkey_center_x - 8, monkey_center_y + 18)], fill=monkey_brown, width=3)
        draw.line([(monkey_center_x + 4, monkey_center_y + 8), (monkey_center_x + 6, monkey_center_y + 18)], fill=monkey_brown, width=3)

        # Free Arm holding banana
        banana_x = monkey_center_x + 10 + math.sin(phase) * 2
        banana_y = monkey_center_y
        draw.line([(monkey_center_x + 5, monkey_center_y - 2), (banana_x, banana_y)], fill=monkey_brown, width=3)
        # Golden Banana
        draw.arc([banana_x - 3, banana_y - 6, banana_x + 7, banana_y + 4], 40, 180, fill=banana_yellow, width=3)

        # Monkey Head
        head_x = monkey_center_x
        head_y = monkey_center_y - 14
        draw.ellipse([head_x - 7, head_y - 7, head_x + 7, head_y + 7], fill=monkey_brown)
        # Ears
        draw.ellipse([head_x - 10, head_y - 4, head_x - 6, head_y + 2], fill=monkey_face)
        draw.ellipse([head_x + 6, head_y - 4, head_x + 10, head_y + 2], fill=monkey_face)
        # Face muzzle
        draw.ellipse([head_x - 5, head_y - 3, head_x + 5, head_y + 6], fill=monkey_face)
        # Eyes
        draw.ellipse([head_x - 3, head_y - 2, head_x - 1, head_y], fill=(20, 20, 20, 255))
        draw.ellipse([head_x + 1, head_y - 2, head_x + 3, head_y], fill=(20, 20, 20, 255))

        frames.append(img)

    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=65, loop=0, disposal=2)
    return output_path
