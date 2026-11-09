import math
from PIL import Image, ImageDraw
from ..github_api import hex_to_rgba

def render_snake_train(stats, output_path="dist/snake_train.gif", frame_count=20):
    commits = stats.get("contributions", 900)
    languages = stats.get("languages", {})

    engine_black = (45, 52, 54, 255)
    engine_red = (214, 48, 49, 255)
    gold_trim = (253, 203, 110, 255)
    wheel_gray = (99, 110, 114, 255)
    tie_wood = (120, 80, 50, 255)
    rail_steel = (140, 150, 160, 255)
    smoke_white = (240, 245, 250, 190)

    lang_colors = [hex_to_rgba(c) for c in languages.values()] or [
        (241, 224, 90, 255), (49, 120, 198, 255), (53, 114, 165, 255), (243, 75, 125, 255)
    ]

    # Number of carriages scales with commits: 3 up to 8
    num_carriages = min(8, max(3, int(2 + 1.2 * math.log(max(1, commits)))))

    carriage_w = 26
    carriage_h = 18
    gap = 6
    train_total_w = 46 + num_carriages * (carriage_w + gap) + 15
    canvas_w = max(300, train_total_w + 30)
    canvas_h = 130
    track_y = canvas_h - 22

    frames = []
    for f in range(frame_count):
        img = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        phase = (f / frame_count) * 2 * math.pi
        chug_y = abs(math.sin(phase * 2)) * 2.0
        wheel_rot = phase * 2

        # 1. Train Tracks
        # Railroad ties
        for tx in range(0, canvas_w, 14):
            draw.rectangle([tx, track_y + 4, tx + 6, track_y + 10], fill=tie_wood)
        # Steel rails
        draw.line([(0, track_y + 3), (canvas_w, track_y + 3)], fill=rail_steel, width=2)
        draw.line([(0, track_y + 8), (canvas_w, track_y + 8)], fill=rail_steel, width=2)

        # 2. Animated Steam Puffs from smokestack
        smokestack_x = canvas_w - 55
        smokestack_y = track_y - 36 - chug_y
        for puff_i in range(4):
            t_puff = (f / frame_count + puff_i * 0.25) % 1.0
            px = smokestack_x - (t_puff * 60)
            py = smokestack_y - (t_puff * 35) + math.sin(t_puff * 6) * 3
            pr = 4 + t_puff * 10
            alpha = int(190 * (1.0 - t_puff))
            draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(240, 245, 250, alpha))

        # 3. Engine Locomotive (at the front / right side)
        eng_x = canvas_w - 80
        eng_y = track_y - 30 - chug_y
        # Engine body
        draw.rounded_rectangle([eng_x, eng_y + 6, eng_x + 48, eng_y + 28], radius=4, fill=engine_black)
        # Cabin
        draw.rounded_rectangle([eng_x + 24, eng_y - 8, eng_x + 46, eng_y + 20], radius=3, fill=engine_red)
        # Cabin window
        draw.rectangle([eng_x + 28, eng_y - 4, eng_x + 42, eng_y + 6], fill=(220, 240, 255, 255))
        # Smokestack
        draw.polygon([(eng_x + 8, eng_y + 6), (eng_x + 5, eng_y - 8), (eng_x + 15, eng_y - 8), (eng_x + 12, eng_y + 6)], fill=engine_black)
        draw.rectangle([eng_x + 4, eng_y - 10, eng_x + 16, eng_y - 7], fill=gold_trim)
        # Front Cowcatcher
        draw.polygon([(eng_x + 48, eng_y + 14), (eng_x + 56, eng_y + 26), (eng_x + 48, eng_y + 26)], fill=gold_trim)
        # Headlight
        draw.ellipse([eng_x + 47, eng_y + 8, eng_x + 53, eng_y + 16], fill=(255, 230, 100, 255))

        # Engine Wheels
        for wx in [eng_x + 12, eng_x + 36]:
            draw.ellipse([wx - 7, track_y - 12 - chug_y, wx + 7, track_y + 2 - chug_y], fill=wheel_gray, outline=engine_black)
            # Wheel spokes
            spoke_dx = math.cos(wheel_rot) * 5
            spoke_dy = math.sin(wheel_rot) * 5
            draw.line([(wx - spoke_dx, track_y - 5 - chug_y - spoke_dy), (wx + spoke_dx, track_y - 5 - chug_y + spoke_dy)], fill=gold_trim, width=2)

        # 4. Carriages (colored by programming languages!)
        curr_x = eng_x
        for ci in range(num_carriages):
            c_color = lang_colors[ci % len(lang_colors)]
            curr_x -= (carriage_w + gap)
            c_y = track_y - carriage_h - 10 - (math.sin(phase * 2 - ci * 0.4) * 1.5)

            # Coupler hitch
            draw.line([(curr_x + carriage_w, c_y + carriage_h - 4), (curr_x + carriage_w + gap, c_y + carriage_h - 4)], fill=engine_black, width=3)

            # Carriage body
            draw.rounded_rectangle([curr_x, c_y, curr_x + carriage_w, c_y + carriage_h], radius=3, fill=c_color, outline=engine_black)
            # Carriage roof / gold trim
            draw.rectangle([curr_x + 2, c_y - 2, curr_x + carriage_w - 2, c_y], fill=gold_trim)
            # Carriage windows
            draw.rectangle([curr_x + 4, c_y + 3, curr_x + 10, c_y + 9], fill=(255, 255, 255, 220))
            draw.rectangle([curr_x + 14, c_y + 3, curr_x + 20, c_y + 9], fill=(255, 255, 255, 220))

            # Carriage wheels
            for c_wx in [curr_x + 6, curr_x + carriage_w - 6]:
                draw.ellipse([c_wx - 4, track_y - 8, c_wx + 4, track_y], fill=wheel_gray, outline=engine_black)

        frames.append(img)

    frames[0].save(output_path, format="GIF", save_all=True, append_images=frames[1:], duration=65, loop=0, disposal=2)
    return output_path

