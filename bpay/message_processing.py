import re
from io import BytesIO

import aiohttp
import ssl
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message, InputMediaDocument

from bpay.patterns import NEW_APP_PATTERN


async def parse_new_app(text: str) -> dict | None:
    # Применяем регулярное выражение к тексту
    match = re.fullmatch(NEW_APP_PATTERN, text)

    if match:
        return {
            "arbitrage_number": match.group(2),
            "token": match.group(3),
            "amount": match.group(4),
            "date": match.group(5)
        }
    else:
        return None


def extract_urls_for_attachment(message: Message, attachment_text="Вложение #1"):
    urls = []

    for entity in message.entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            text = message.text[entity.offset: entity.offset + entity.length]
            if text == attachment_text:  # Проверяем, что текст совпадает
                urls.append(entity.url)

    return urls


async def download_files_to_memory(urls: list[str]):
    files = []
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        for i, url in enumerate(urls):
            try:
                async with session.get(url, ssl=ssl_context, timeout=180) as response:
                    if response.status == 200:
                        content = await response.read()
                        file = BytesIO(content)
                        ex = url.split('.')[-1]
                        file.name = f"file_{i+1}.{ex}"
                        files.append(InputMediaDocument(file))
            except Exception as e:
                print(f"Ошибка при загрузке {url}: {e}")

    return files
