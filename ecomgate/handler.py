import asyncio

from pyrogram import Client
from pyrogram.types import Message

from config import Config
from db.database import get_transaction_by_token, add_transaction, delete_transaction
from ecomgate.find_reply_message import find_reply_message
from ecomgate.message_processing import parse_user_request_message, parse_bot_request_message, copy_message_to_chat

from enums import Provider
from payscorw.sending import format_caption

ADMIN_STRING="1243DEL22"


async def handler(app: Client, message: Message):
    result = await handle_user_request(app, message)

    if not result:
        await handle_bot_request(app, message)


async def handle_user_request(app: Client, message: Message) -> bool:
    data = parse_user_request_message(message.caption)

    if not data:
        return False

    if message.reactions:
        return True

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
            False,
            str(Provider.ECOMGATE)
        )
        await asyncio.gather(
            app.send_reaction(chat_id=Config.ECOMGATE_CHAT_ID, message_id=message.id, emoji="👀"),
            message.copy(chat_id=Config.PAYSCROW_CHAT_ID, caption=text),
        )

    return True


async def handle_bot_request(app: Client, message: Message) -> bool:
    if not message.reply_markup or message.from_user.id != Config.ECOMGATE_BOT_ID:
        return False

    data = parse_bot_request_message(message.caption)

    if not data:
        return False

    transaction_db = get_transaction_by_token(data['token'])

    if transaction_db:
        delete_transaction(transaction_db['token'])

    text = format_caption(data['amount'], data['token'])
    reply_message = await find_reply_message(app, message.id)

    if reply_message:
        await copy_message_to_chat(app, text, reply_message)
    else:
        await copy_message_to_chat(app, text, message)

    add_transaction(
        data['token'],
        data['amount'],
        None,
        data['number'],
        Config.ECOMGATE_CHAT_ID,
        message.id,
        True,
        str(Provider.ECOMGATE)
    )

    return True


async def handle_result(app: Client, identifier: str, success: bool):
    transaction_db = get_transaction_by_token(identifier)
    if transaction_db:
        if bool(transaction_db['from_bot']):
            await handle_result_bot(app, transaction_db, success)
        else:
            await handle_result_user(app, transaction_db, success)

        delete_transaction(transaction_db['token'])

    if not success:
        await app.send_message(
            chat_id=Config.TECH_ECOMGATE_CHAT_ID,
            text=f"Транзакция {identifier} отклонена, требуется проверка"
        )


async def handle_result_bot(app: Client, transaction_db: dict, success: bool):
    message = await app.get_messages(chat_id=Config.BPAY_CHAT_ID, message_ids=int(transaction_db['message_id']))

    if not message:
        return

    if success:
        try:
            await message.click("Обновили, уведомить 🔁")
            await app.request_callback_answer(
                chat_id=message.chat.id,
                message_id=message.id,
                callback_data=message.reply_markup.inline_keyboard[0][0].callback_data
            )
        except Exception as e:
            print("Submit appeal:", e)
    else:
        try:
            await app.request_callback_answer(
                chat_id=message.chat.id,
                message_id=message.id,
                callback_data=message.reply_markup.inline_keyboard[0][1].callback_data
            )
        except Exception as e:
            print("Cancel appeal:", e)


async def handle_result_user(app: Client, transaction_db: dict, success: bool):
    text = f"Транзакция {transaction_db['token']} ({transaction_db['external_id']}) подтверждена." if success else \
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