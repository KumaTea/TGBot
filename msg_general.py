import asyncio
import logging
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import ParseMode


special_ids = [
    100, 1000, 10000, 100000, 1000000
]
for i in special_ids.copy():
    for j in range(1, 10):
        special_ids.append(i*j)
special_ids.extend([114514, 1919, 810, 1919810])


async def process_id(message: Message):
    message_id = message.id
    if message_id in special_ids:
        await message.reply_text(f'祝贺本群第**{message_id}**条消息达成！ 🎉', parse_mode=ParseMode.MARKDOWN, quote=False)
    return True


async def unpin_channel_post(client: Client, message: Message):
    try:
        await asyncio.sleep(2)
        await client.unpin_chat_message(message.chat.id, message.id)
    except Exception as e:
        logging.warning(f'Failed to unpin channel post: {e}')
        logging.warning(f'{message=}')
