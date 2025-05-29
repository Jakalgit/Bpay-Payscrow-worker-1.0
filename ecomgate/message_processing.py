import re


def parse_user_request_message(text: str) -> dict | None:
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


def parse_bot_request_message(text: str) -> dict | None:
    try:
        regex = r"^Апелляция по платежу\nВаш id: ([a-zA-Z0-9]+)\nНаш id: (\d+)\nСумма (\d+) RUB\nЗаявленная сумма (\d+) RUB\nСоздано \d{2}\/\d{2}\/\d{2} \d{2}:\d{2}$"

        match = re.match(regex, text)

        if match:
            return {
                "token": match.group(1),
                "number": match.group(2),
                "amount": match.group(3),
            }
        else:
            return None
    except Exception as e:
        print(e)
        return None


def check_reply_message(text: str):
    pattern = "Оригинальный pdf файл (на случай если Телеграм при обработке повредил текст)"
    return pattern in text
