from pyrogram import Client
from pyrogram.types import InputMediaDocument

from config import Config


async def send_request_for_bot(app: Client, files: list[InputMediaDocument], amount: int, token: str):
    caption = f"{token}\n{amount}"
    if len(files) > 0:
        files[0] = InputMediaDocument(media=files[0].media, caption=caption)
        await app.send_media_group(
            chat_id=Config.PAYSCROW_CHAT_ID,
            media=files
        )