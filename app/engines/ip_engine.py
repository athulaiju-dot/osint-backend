import requests
from app.core.normalizer import normalize

IP_API_URL = "http://ip-api.com/json/{}?fields=status,country,regionName,city,isp,org,as,proxy,hosting"

def run(data: dict):
    ip = data.get("ip")
    if not ip:
        return normalize("ip", {"error": "ip_missing"}, risk_score=100)

    try:
        r = requests.get(IP_API_URL.format(ip), timeout=5)
        info = r.json()
    except Exception:
        return normalize("ip", {"error": "lookup_failed"}, risk_score=80)

    if info.get("status") != "success":
        return normalize("ip", {"error": "invalid_ip"}, risk_score=90)

    # Risk scoring
    risk = 0
    if info.get("proxy"):
        risk += 40
    if info.get("hosting"):
        risk += 30

    raw = {
        "ip": ip,
        "country": info.get("country"),
        "region": info.get("regionName"),
        "city": info.get("city"),
        "isp": info.get("isp"),
        "organization": info.get("org"),
        "asn": info.get("as"),
        "is_proxy": info.get("proxy"),
        "is_hosting": info.get("hosting")
    }

    return normalize("ip", raw, risk_score=risk)
