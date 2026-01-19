from app.core.normalizer import normalize

def run(data: dict):
    username = data.get("username")

    raw = {
        "username": username,
        "platforms_found": [],
        "confidence": 0.0,
        "aliases": []
    }

    return normalize("username", raw, risk_score=0)
