from pyrogram import Client
from asyncio import sleep

from config import Config


async def set_arbitrage_in_success(app: Client, message_id: str | int):
    message = await app.get_messages(Config.BPAY_CHAT_ID, message_id)
    try:
        await message.click("Обработать")
        await sleep(500)
        await message.click("Оплачено")
        await sleep(500)
        await message.click("Заявка в статусе Success")
    except Exception as e:
        print(e)