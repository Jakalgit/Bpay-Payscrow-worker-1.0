import re

from onewintjs.patterns import NEW_REQUEST_PATTERN


def parse_new_request(text: str) -> dict | None:
    # Применяем регулярное выражение к тексту
    match = re.fullmatch(NEW_REQUEST_PATTERN, text)

    if match:
        return {
            "merchant_token": match.group(1),
            "token": match.group(2),
            "message": match.group(3)
        }
    else:
        return None
