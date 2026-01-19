from app.core.normalizer import normalize

def run(data: dict):
    image_input = data.get("image")

    raw = {
        "input_type": "image",
        "faces_detected": 0,
        "objects_detected": [],
        "metadata": {
            "exif_present": False,
            "location_hint": None
        }
    }

    return normalize("image", raw, risk_score=0)
