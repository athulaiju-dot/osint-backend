import hashlib
import requests
from io import BytesIO
from PIL import Image
import exifread
from app.core.normalizer import normalize

MAX_IMAGE_SIZE_MB = 5

def hash_bytes(data: bytes):
    return {
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest()
    }

def extract_exif(image_bytes: bytes):
    tags = {}
    try:
        with BytesIO(image_bytes) as f:
            exif = exifread.process_file(f, details=False)
            for tag, value in exif.items():
                if tag.startswith("EXIF") or tag.startswith("Image"):
                    tags[tag] = str(value)
    except Exception:
        pass
    return tags

def run(data: dict):
    image_url = data.get("image")

    if not image_url:
        return normalize("image", {"error": "image_url_missing"}, risk_score=100)

    try:
        r = requests.get(image_url, timeout=6)
        image_bytes = r.content
    except Exception:
        return normalize("image", {"error": "download_failed"}, risk_score=80)

    size_mb = len(image_bytes) / (1024 * 1024)
    if size_mb > MAX_IMAGE_SIZE_MB:
        return normalize("image", {"error": "image_too_large"}, risk_score=60)

    # Validate image
    try:
        img = Image.open(BytesIO(image_bytes))
        img.verify()
    except Exception:
        return normalize("image", {"error": "invalid_image"}, risk_score=90)

    hashes = hash_bytes(image_bytes)
    exif_data = extract_exif(image_bytes)

    # Risk scoring
    risk = 0
    if not exif_data:
        risk += 20
    if "EXIF DateTimeOriginal" not in exif_data:
        risk += 10

    raw = {
        "image_url": image_url,
        "format": img.format,
        "mode": img.mode,
        "size_pixels": img.size,
        "file_size_mb": round(size_mb, 2),
        "hashes": hashes,
        "exif_present": bool(exif_data),
        "exif_metadata": exif_data
    }

    return normalize("image", raw, risk_score=risk)
