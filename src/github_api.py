import os
import re
import sys
import requests

GITHUB_LANG_COLORS = {
    "JavaScript": "#F7DF1E",
    "TypeScript": "#3178C6",
    "Python": "#3572A5",
    "C++": "#F34B7D",
    "C": "#555555",
    "C#": "#178600",
    "Java": "#B07219",
    "HTML": "#E34F26",
    "CSS": "#563D7C",
    "Dart": "#00B4AB",
    "Swift": "#F05138",
    "Rust": "#DEA584",
    "Go": "#00ADD8",
    "Ruby": "#701516",
    "PHP": "#4F5D95",
    "Kotlin": "#A97BFF",
    "Shell": "#89E051",
}

def hex_to_rgba(hex_code, alpha=255):
    h = hex_code.lstrip("#")
    if len(h) == 3:
        h = "".join([c * 2 for c in h])
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (alpha,)

def fetch_user_stats(username="Nightkilller", token=None):
    """
    Fetches the user's lifetime/yearly contribution count and top languages.
    Falls back gracefully if GitHub API is rate-limited.
    """
    stats = {
        "username": username,
        "contributions": 929,
        "languages": {
            "JavaScript": "#F7DF1E",
            "TypeScript": "#3178C6",
            "Python": "#3572A5",
            "Java": "#B07219",
            "Dart": "#00B4AB",
            "HTML": "#E34F26",
        }
    }

    token = token or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    headers = {"User-Agent": "Git-Critters-Engine"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        # 1. Fetch contribution count from GitHub contributions page
        c_url = f"https://github.com/users/{username}/contributions"
        r = requests.get(c_url, headers=headers, timeout=5)
        if r.status_code == 200:
            matches = re.findall(r"([0-9,]+)\s+contributions", r.text)
            if matches:
                cnt = int(matches[0].replace(",", ""))
                if cnt > 0:
                    stats["contributions"] = cnt

        # 2. Fetch repos to determine top languages
        repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&type=owner"
        rr = requests.get(repos_url, headers=headers, timeout=5)
        if rr.status_code == 200:
            repos = rr.json()
            counts = {}
            for repo in repos:
                if isinstance(repo, dict) and not repo.get("fork"):
                    lang = repo.get("language")
                    if lang:
                        counts[lang] = counts.get(lang, 0) + 1
            if counts:
                top = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:6]
                stats["languages"] = {
                    name: GITHUB_LANG_COLORS.get(name, "#888888")
                    for name, _ in top
                }
    except Exception as e:
        print(f"[git-critters] Notice: Using fallback stats ({e})", file=sys.stderr)

    return stats

