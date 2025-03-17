from pyrogram import Client
from pyrogram.types import InputMediaDocument

from config import Config


def format_caption(amount: int | str, token: str) -> str:
    return f"{token}\n{amount}"

async def send_request_for_bot(app: Client, files: list[InputMediaDocument], amount: int, token: str):
    caption = format_caption(amount, token)
    if len(files) > 0:
        files[0] = InputMediaDocument(media=files[0].media, caption=caption)
        await app.send_media_group(
            chat_id=Config.PAYSCROW_CHAT_ID,
            media=files
        )