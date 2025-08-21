from pyrogram import Client
from pyrogram.types import Message, ReplyKeyboardRemove


async def copy_message_to_chat(app: Client, new_caption: str, message: Message, to_chat_id: str | int):
    if message.media_group_id:
        await app.copy_media_group(
            chat_id=to_chat_id,
            from_chat_id=message.chat.id,
            message_id=message.id,
            captions=new_caption,
        )
    elif message.caption:
        await message.copy(
            chat_id=to_chat_id,
            reply_markup=ReplyKeyboardRemove(),
            caption=new_caption,
        )
    else:
        await app.send_message(
            chat_id=to_chat_id,
            reply_markup=ReplyKeyboardRemove(),
            text=new_caption
        )