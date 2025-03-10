from pyrogram import Client

from config import Config
from .handler import handler
import asyncio


async def load_transactions(app: Client, limit=1500):
    history_new_apps = app.search_messages(
        chat_id=Config.BPAY_CHAT_ID,
        query="Заявка на Арбитраж №",
        limit=Config.LIMIT_HISTORY,
        offset=Config.OFFSET_HISTORY
    )

    async for message in history_new_apps:
        await handler(app, message)
        await asyncio.sleep(0.3)
