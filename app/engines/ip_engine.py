from app.core.normalizer import normalize

def run(data: dict):
    ip = data.get("ip")

    raw = {
        "ip": ip,
        "asn": "unknown",
        "isp_type": "unknown",
        "geo_confidence": {
            "country": 0.0,
            "state": 0.0
        },
        "vpn_probability": 0.0,
        "abuse_history": False
    }

    return normalize("ip", raw, risk_score=0)
