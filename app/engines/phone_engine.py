import phonenumbers
from phonenumbers import carrier, geocoder, number_type
from app.core.normalizer import normalize

def run(data: dict):
    phone_raw = data.get("phone")
    if not phone_raw:
        return normalize(
            "phone",
            {"error": "phone_missing"},
            risk_score=100
        )

    try:
        phone = phonenumbers.parse(phone_raw, None)
    except Exception:
        return normalize(
            "phone",
            {"error": "invalid_format"},
            risk_score=90
        )

    if not phonenumbers.is_valid_number(phone):
        return normalize(
            "phone",
            {"error": "invalid_number"},
            risk_score=80
        )

    # Extract intelligence
    country = geocoder.country_name_for_number(phone, "en")
    region = geocoder.description_for_number(phone, "en")
    carrier_name = carrier.name_for_number(phone, "en")
    num_type = number_type(phone)

    # Risk scoring
    risk = 0
    if carrier_name == "":
        risk += 30
    if num_type in [phonenumbers.PhoneNumberType.VOIP]:
        risk += 40

    raw = {
        "input": phone_raw,
        "international_format": phonenumbers.format_number(
            phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        ),
        "national_format": phonenumbers.format_number(
            phone, phonenumbers.PhoneNumberFormat.NATIONAL
        ),
        "country": country,
        "region": region,
        "carrier": carrier_name or "unknown",
        "line_type": str(num_type).replace("PhoneNumberType.", "").lower()
    }

    return normalize("phone", raw, risk_score=risk)
