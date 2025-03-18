import asyncio

from pyrogram import Client

from config import Config
from ecomgate.message_processing import check_reply_message


async def find_reply_message(app:Client, message_id: int):
    await asyncio.sleep(1.5)

    for i in range(4):
        async for msg in app.get_chat_history(chat_id=Config.ECOMGATE_CHAT_ID, limit=10):
            if msg.reply_to_message_id == message_id:
                if msg.from_user and msg.from_user.id == Config.ECOMGATE_BOT_ID:
                    if check_reply_message(msg.caption):
                        return msg
        await asyncio.sleep(1.5)

    return None