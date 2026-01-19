def score_ip(data):
    score = 0
    if data.get("vpn_probability", 0) > 0.5:
        score += 40
    if data.get("abuse_history"):
        score += 30
    return min(score, 100)
