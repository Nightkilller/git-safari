import io
import os
import sys
from urllib.parse import parse_qs, urlparse
from http.server import BaseHTTPRequestHandler

# Add root project folder to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.github_api import fetch_user_stats
from src.creatures import CREATURES

def get_creature_gif(username, creature_name):
    """Generate GIF in-memory and return raw bytes."""
    stats = fetch_user_stats(username)
    render_fn = CREATURES.get(creature_name.lower(), CREATURES["giraffe"])
    buf = io.BytesIO()
    # 16 frames for super-fast serverless rendering (< 250ms)
    render_fn(stats, buf, frame_count=16)
    return buf.getvalue()

# 1. BaseHTTPRequestHandler interface (Vercel Serverless Function)
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        username = params.get("username", ["Nightkilller"])[0]
        creature = params.get("creature", ["giraffe"])[0]

        try:
            gif_bytes = get_creature_gif(username, creature)
            self.send_response(200)
            self.send_header("Content-Type", "image/gif")
            # Cache on Vercel Edge CDN for 4 hours, allow stale revalidate for 1 day
            self.send_header("Cache-Control", "public, max-age=14400, s-maxage=14400, stale-while-revalidate=86400")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(gif_bytes)
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Error rendering creature: {e}".encode("utf-8"))

# 2. WSGI Application interface (Alternative Vercel entrypoint)
def app(environ, start_response):
    query_string = environ.get("QUERY_STRING", "")
    params = parse_qs(query_string)

    username = params.get("username", ["Nightkilller"])[0]
    creature = params.get("creature", ["giraffe"])[0]

    try:
        gif_bytes = get_creature_gif(username, creature)
        headers = [
            ("Content-Type", "image/gif"),
            ("Cache-Control", "public, max-age=14400, s-maxage=14400, stale-while-revalidate=86400"),
            ("Access-Control-Allow-Origin", "*"),
        ]
        start_response("200 OK", headers)
        return [gif_bytes]
    except Exception as e:
        start_response("500 Internal Server Error", [("Content-Type", "text/plain")])
        return [f"Error rendering creature: {e}".encode("utf-8")]
