import asyncio

from pyrogram import Client, idle
from pyrogram.types import Message

from bpay.load_transactions import load_transactions
from config import Config
from controller import controller

app = Client("TransactionsBotAP", api_id=Config.API_ID, api_hash=Config.API_HASH)
CHAT_IDS = [Config.BPAY_CHAT_ID]

init_flag = False


@app.on_message(filters=CHAT_IDS)
async def handle_message(client, message: Message):
    global init_flag
    if not init_flag:
        init_flag = True
        await load_transactions(app)
    if message.chat.id in CHAT_IDS:
        await controller(app, message)

if __name__ == "__main__":
    app.run()