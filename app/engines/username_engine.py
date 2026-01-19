import re
import httpx
from app.core.normalizer import normalize

# Platforms to check (public profile URLs)
PLATFORMS = {
    "github": "https://github.com/{}",
    "twitter": "https://x.com/{}",
    "instagram": "https://www.instagram.com/{}/",
    "reddit": "https://www.reddit.com/user/{}/",
    "medium": "https://medium.com/@{}",
}

USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9._-]{3,30}$")

def analyze_pattern(username: str):
    score = 0
    if re.search(r"\d{3,}", username):
        score += 10
    if re.search(r"[_.-]", username):
        score += 5
    if username.islower():
        score += 5
    return score

def run(data: dict):
    username = data.get("username")
    if not username:
        return normalize("username", {"error": "username_missing"}, risk_score=100)

    if not USERNAME_REGEX.match(username):
        return normalize(
            "username",
            {"error": "invalid_username_format"},
            risk_score=80
        )

    found = []
    checked = {}

    try:
        with httpx.Client(timeout=5, follow_redirects=True) as client:
            for platform, url in PLATFORMS.items():
                resp = client.get(url.format(username))
                exists = resp.status_code == 200
                checked[platform] = exists
                if exists:
                    found.append(platform)
    except Exception:
        return normalize(
            "username",
            {"error": "lookup_failed"},
            risk_score=70
        )

    reuse_score = len(found) * 15
    pattern_score = analyze_pattern(username)

    risk = max(0, 100 - (reuse_score + pattern_score))

    raw = {
        "username": username,
        "platforms_checked": list(PLATFORMS.keys()),
        "platforms_found": found,
        "presence_map": checked,
        "reuse_count": len(found),
        "pattern_score": pattern_score
    }

    return normalize("username", raw, risk_score=risk)
