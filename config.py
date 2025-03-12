import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    API_HASH = os.environ.get('API_HASH')
    API_ID = os.environ.get('API_ID')

    PAYSCROW_BOT_ID = int(os.environ.get('PAYSCROW_BOT_ID'))
    PAYSCROW_CHAT_ID = int(os.environ.get('PAYSCROW_CHAT_ID'))

    BPAY_BOT_ID = int(os.environ.get('BPAY_BOT_ID'))
    BPAY_CHAT_ID = int(os.environ.get('BPAY_CHAT_ID'))

    TECH_CHAT_ID = os.environ.get('TECH_CHAT_ID')

    LIMIT_HISTORY = 1500
    OFFSET_HISTORY = 0