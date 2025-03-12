from pyrogram import Client
from pyrogram.types import Message

from bpay.message_processing import extract_urls_for_attachment, download_files_to_memory, parse_update_app
from config import Config
from .message_processing import parse_new_app
from payscorw.sending import send_request_for_bot


async def handler(app: Client, message: Message):
    # Если сообщение не от бота, то выходим
    if message.from_user.id != Config.BPAY_BOT_ID:
        return

    data = parse_new_app(message.text)

    if data:
        await handle_new_app(app, message, data)



async def handle_new_app(app: Client, message: Message, data: dict):
    if not message.reply_markup:
        return

    url = extract_urls_for_attachment(message)
    files = await download_files_to_memory(url)
    amount = int(data['amount'])

    await send_request_for_bot(app, files, amount, data['token'])