from pyrogram import Client
from pyrogram.types import Message
from bpay.handler import handler as bpay_handler
from config import Config
from payscorw.handler import handler as payscrow_handler
from ecomgate.handler import handler as ecomgate_handler
from onewintjs.hander import handler as onewin_tjs_handler

handlers = {
    Config.ECOMGATE_CHAT_ID: ecomgate_handler,
    Config.PAYSCROW_CHAT_ID: payscrow_handler,
    Config.BPAY_CHAT_ID: bpay_handler,
    Config.ONEWIN_TJS_CHAT_ID: onewin_tjs_handler
}

async def controller(app: Client, message: Message):
    handler = handlers.get(message.chat.id)
    if handler:
        await handler(app, message)