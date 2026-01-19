from datetime import datetime

def normalize(tool, raw, risk_score):
    return {
        "tool": tool,
        "risk_score": risk_score,
        "confidence": round(1 - (risk_score / 120), 2),
        "generated_at": datetime.utcnow(),
        "result": raw
    }
