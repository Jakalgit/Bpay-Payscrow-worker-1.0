
SUCCESS_WORD = """удовлетворена"""
FAILED_WORD = """отклонена."""

def parse_result_message(text: str) -> dict | None:

    if not text:
        return None

    arr = text.split(' ')

    if not (arr[0] == "Апелляция" and arr[2] == "для" and arr[3] == "ордера"):
        return None

    amount = float(arr[-1].replace(",", "")) if arr[7] == SUCCESS_WORD else -1
    token = arr[6]
    appeal_id = arr[1]
    order_id = arr[4]

    return {
        "amount": amount,
        "token": token,
        "appeal_id": appeal_id,
        "order_id": order_id,
        "success": arr[7] == SUCCESS_WORD,
    }