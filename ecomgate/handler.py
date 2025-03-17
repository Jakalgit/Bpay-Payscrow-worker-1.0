import asyncio

from pyrogram import Client
from pyrogram.types import Message

from config import Config
from db.database import get_transaction_by_token, add_transaction, delete_transaction
from ecomgate.message_processing import parse_request_message

from enums import Provider
from payscorw.sending import format_caption

ADMIN_STRING="1243DEL22"


async def handler(app: Client, message: Message):
    data = parse_request_message(message.caption)

    if not data:
        return

    if ADMIN_STRING in data['token']:
        token = str(data['token']).replace(ADMIN_STRING, "")
    else:
        token = str(data['token'])

    transaction_db = get_transaction_by_token(token)

    if ADMIN_STRING in data['token'] and transaction_db:
        delete_transaction(transaction_db['token'])
        transaction_db = None
        data['token'] = token

    if transaction_db:
        try:
            await asyncio.gather(
                message.reply(text="Транзакция уже в обработке"),
                app.send_reaction(chat_id=Config.ECOMGATE_CHAT_ID, message_id=message.id, emoji="🤔"),
            )
        except Exception as e:
            print(e)
    elif message.media:
        text = format_caption(data['amount'], data['token'])
        add_transaction(
            data['token'],
            data['amount'],
            None,
            data['number'],
            Config.ECOMGATE_CHAT_ID,
            message.id,
            str(Provider.ECOMGATE)
        )
        await asyncio.gather(
            app.send_reaction(chat_id=Config.ECOMGATE_CHAT_ID, message_id=message.id, emoji="👀"),
            message.copy(chat_id=Config.PAYSCROW_CHAT_ID, caption=text),
        )


async def handle_result(app: Client, identifier: str, success: bool):
    transaction_db = get_transaction_by_token(identifier)
    if transaction_db:
        text = f"Транзакция {transaction_db['token']} ({transaction_db['external_id']}) подтверждена." if success else\
        f"Транзакция {transaction_db['token']} ({transaction_db['external_id']}) отклонена, вам ответит администратор."
        emoji = "👍" if success else "👎"
        try:
            await asyncio.gather(
                app.send_message(
                    chat_id=Config.ECOMGATE_CHAT_ID,
                    text=text,
                    reply_to_message_id=int(transaction_db['message_id']),
                ),
                app.send_reaction(
                    chat_id=Config.ECOMGATE_CHAT_ID, message_id=int(transaction_db['message_id']), emoji=emoji
                )
            )
        except Exception as e:
            print(e)
            await app.send_message(
                chat_id=Config.ECOMGATE_CHAT_ID,
                text=text,
            )
        delete_transaction(transaction_db['token'])
    if not success:
        await app.send_message(
            chat_id=Config.TECH_ECOMGATE_CHAT_ID,
            text=f"Транзакция {identifier} отклонена, требуется проверка"
        )