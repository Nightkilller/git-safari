import argparse
import os
import sys
from .github_api import fetch_user_stats
from .creatures import CREATURES

def main():
    parser = argparse.ArgumentParser(description="Git-Safari: Dynamic animated creatures powered by your GitHub stats!")
    parser.add_argument("--username", "-u", default="Nightkilller", help="GitHub username")
    parser.add_argument("--creature", "-c", default="all", choices=list(CREATURES.keys()) + ["all"], help="Which creature to generate")
    parser.add_argument("--output-dir", "-o", default="dist", help="Output directory for generated GIFs")
    parser.add_argument("--token", "-t", default=None, help="GitHub Personal Access Token (optional, uses GITHUB_TOKEN if set)")
    parser.add_argument("--frames", "-f", type=int, default=20, help="Number of animation frames in the loop")

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    print(f"🐾 Fetching GitHub stats for @{args.username}...")
    stats = fetch_user_stats(args.username, args.token)
    print(f"📊 Found: {stats['contributions']} contributions, {len(stats['languages'])} languages: {list(stats['languages'].keys())}")

    targets = list(CREATURES.keys()) if args.creature == "all" else [args.creature]

    for c_name in targets:
        render_fn = CREATURES[c_name]
        out_file = os.path.join(args.output_dir, f"{c_name}.gif")
        print(f"✨ Rendering {c_name} to {out_file}...")
        render_fn(stats, out_file, frame_count=args.frames)
        print(f"✅ Generated {out_file} successfully!")

if __name__ == "__main__":
    main()

