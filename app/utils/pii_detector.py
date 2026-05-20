import re

EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

PHONE_REGEX = r"\b\d{10}\b"

PASSPORT_REGEX = r"\b[A-Z][0-9]{7}\b"


def detect_pii(key, value):

    if not isinstance(value, str):
        return None

    key = key.lower()

    if "name" in key:
        return "user"

    if "passport" in key:
        return "passport"

    if "member" in key or "loyalty" in key:
        return "memberid"

    if re.match(EMAIL_REGEX, value):
        return "email"

    if re.match(PHONE_REGEX, value):
        return "phone"

    if re.match(PASSPORT_REGEX, value):
        return "passport"

    return None
