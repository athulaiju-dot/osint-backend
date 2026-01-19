import phonenumbers
from phonenumbers import carrier, geocoder, number_type
from app.core.normalizer import normalize

def run(data: dict):
    phone_raw = data.get("phone")
    if not phone_raw:
        return normalize("phone", {"error": "phone_missing"}, risk_score=100)

    # Force India as default region if no country code
    try:
        if phone_raw.startswith("+"):
            phone = phonenumbers.parse(phone_raw, None)
        else:
            phone = phonenumbers.parse(phone_raw, "IN")
    except Exception:
        return normalize("phone", {"error": "invalid_format"}, risk_score=90)

    if not phonenumbers.is_valid_number(phone):
        return normalize("phone", {"error": "invalid_number"}, risk_score=80)

    country = geocoder.country_name_for_number(phone, "en")
    region = geocoder.description_for_number(phone, "en")
    carrier_name = carrier.name_for_number(phone, "en") or "unknown"
    num_type = number_type(phone)

    # Risk scoring
    risk = 0
    if carrier_name == "unknown":
        risk += 10
    if num_type == phonenumbers.PhoneNumberType.VOIP:
        risk += 40

    raw = {
        "input": phone_raw,
        "international_format": phonenumbers.format_number(
            phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        ),
        "national_format": phonenumbers.format_number(
            phone, phonenumbers.PhoneNumberFormat.NATIONAL
        ),
        "country": country or "India",
        "region": region or "India",
        "carrier": carrier_name,
        "line_type": str(num_type).replace("PhoneNumberType.", "").lower()
    }

    return normalize("phone", raw, risk_score=risk)
