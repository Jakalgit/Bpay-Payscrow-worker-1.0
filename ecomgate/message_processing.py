import re


def parse_request_message(text: str) -> dict | None:
    try:
        regex = r"^(\d+)\n([a-zA-Z0-9]+)\n(\d+)$"

        match = re.match(regex, text)

        if match:
            return {
                "number": match.group(1),
                "token": match.group(2),
                "amount": match.group(3)
            }
        else:
            return None
    except Exception as e:
        print(e)
        return None