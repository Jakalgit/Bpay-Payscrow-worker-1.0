from pyrogram import Client
from pyrogram.types import Message

from config import Config
from db.database import get_transaction_by_token
from payscorw.message_processing import parse_result_message
from ecomgate.handler import handle_result


async def handler(app: Client, message: Message):
    # Если сообщение не от бота, то выходим
    if message.from_user.id != Config.PAYSCROW_BOT_ID:
        return

    # Парсим сообщение от бота
    transaction_data = parse_result_message(message.text)

    if transaction_data:
        # Получаем транзакцию из бд
        transaction_db = get_transaction_by_token(transaction_data['token'])
        if transaction_db:
            success = transaction_data['success'] or "Ордер уже исполнен на сумму" in message.text
            if int(transaction_db['chat_id']) == Config.ECOMGATE_CHAT_ID:
                await handle_result(app, transaction_db['token'], success)