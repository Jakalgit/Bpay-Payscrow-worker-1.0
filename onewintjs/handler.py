import asyncio

from pyrogram import Client
from pyrogram.types import Message

from config import Config
from onewintjs.message_processing import parse_new_request

from message_processing import copy_message_to_chat


async def handler(app: Client, message: Message):
    text = message.caption if message.caption else message.text

    if not text:
        return

    data = parse_new_request(text)

    if data:
        text = f"{data["token"]}" + (f"\n{data["message"]}" if data["message"] else "")
        await copy_message_to_chat(app, text, message, Config.YUMMY_CHAT_ID)
        await asyncio.sleep(3.1)
        await app.send_reaction(chat_id=Config.ECOMGATE_CHAT_ID, message_id=message.id, emoji="👀")