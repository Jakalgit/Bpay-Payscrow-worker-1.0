from pyrogram import Client

from config import Config
from .handler import handler


async def load_transactions(app: Client, limit=0, offset=0):
    history_new_apps = app.search_messages(
        chat_id=Config.ECOMGATE_CHAT_ID,
        limit=limit,
        offset=offset
    )

    if limit == 0:
        return

    async for message in history_new_apps:
        await handler(app, message)
        await asyncio.sleep(0.3)
