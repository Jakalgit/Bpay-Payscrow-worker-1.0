from pyrogram import Client, idle
from pyrogram.types import Message

from config import Config
from controller import controller
from load_transactions import load_transactions

app = Client("TransactionsBotAP", api_id=Config.API_ID, api_hash=Config.API_HASH)
CHAT_IDS = [Config.PAYSCROW_CHAT_ID, Config.ECOMGATE_CHAT_ID, Config.ONEWIN_TJS_CHAT_ID]

@app.on_message(filters=CHAT_IDS)
async def handle_message(client, message: Message):
    if message.chat.id in CHAT_IDS:
        await controller(app, message)


async def main():
    await app.start()
    async for dialog in app.get_dialogs():
        print("Loaded dialog:", dialog.chat.id)
    await load_transactions(app)
    await idle()
    await app.stop()

if __name__ == "__main__":
    app.run(main())