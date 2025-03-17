from pyrogram import Client
from bpay.load_transactions import load_transactions as load_transactions_bpay
from ecomgate.load_transactions import load_transactions as load_transactions_ecomgate
import asyncio


async def load_transactions(app: Client):
    await asyncio.gather(
        load_transactions_ecomgate(app),
        load_transactions_bpay(app),
    )
