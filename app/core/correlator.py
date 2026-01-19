from collections import defaultdict
from datetime import datetime

# In-memory correlation store (safe for now)
CORRELATION_STORE = defaultdict(list)

def add_entity(case_id: str, entity_type: str, value: dict):
    CORRELATION_STORE[case_id].append({
        "type": entity_type,
        "value": value,
        "timestamp": datetime.utcnow().isoformat()
    })

def correlate(case_id: str):
    entities = CORRELATION_STORE.get(case_id, [])
    links = []

    for i in range(len(entities)):
        for j in range(i + 1, len(entities)):
            a = entities[i]
            b = entities[j]

            links.append({
                "entity_a": a["type"],
                "entity_b": b["type"],
                "confidence": calculate_confidence(a, b)
            })

    return {
        "case_id": case_id,
        "entities": entities,
        "links": links,
        "entity_count": len(entities)
    }

def calculate_confidence(a, b):
    score = 0.5

    # Heuristic rules
    if a["type"] == "ip" and b["type"] == "username":
        if a["value"].get("country") and b["value"].get("pattern_score", 0) > 0:
            score += 0.2

    if a["type"] == "phone" and b["type"] == "username":
        score += 0.3

    if a["type"] == "image" and b["type"] == "username":
        score += 0.2

    return min(score, 0.95)
