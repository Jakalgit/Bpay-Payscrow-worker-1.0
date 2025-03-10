from pyrogram import Client
from pyrogram.types import Message
from bpay.handler import handler as bpay_handler

async def controller(app: Client, message: Message):
    await bpay_handler(app, message)