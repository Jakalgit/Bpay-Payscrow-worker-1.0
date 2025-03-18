from pyrogram import Client
from bpay.load_transactions import load_transactions as load_transactions_bpay
from ecomgate.load_transactions import load_transactions as load_transactions_ecomgate
import asyncio

LIMIT_ECOMAGATE = 10
OFFSET_ECOMGATE = 0

LIMIT_BPAY = 0
OFFSET_BPAY = 0


async def load_transactions(app: Client):
    await asyncio.gather(
        load_transactions_ecomgate(app, LIMIT_ECOMAGATE, OFFSET_ECOMGATE),
        load_transactions_bpay(app, LIMIT_BPAY, OFFSET_BPAY),
    )
