from app.core.normalizer import normalize

def run(data: dict):
    phone = data.get("phone")

    raw = {
        "phone": phone,
        "country": "unknown",
        "carrier": "unknown",
        "line_type": "unknown",
        "spam_score": 0
    }

    return normalize("phone", raw, risk_score=0)
