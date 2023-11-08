import re
import random
import asyncio
import hashlib
import logging
from bot_db import title_re
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

title_pattern = re.compile(title_re)


async def process_id(message: Message):
    message_id = message.id
    if message_id in special_ids:
        await message.reply_text(f'祝贺本群第**{message_id}**条消息达成！ 🎉', parse_mode=ParseMode.MARKDOWN, quote=False)
    return True


async def douban_mark(message: Message):
    text = message.text or message.caption
    result = title_pattern.findall(text)
    if result:
        title = result[0][1:-1].strip().lower()
        title_hash = int(hashlib.md5(title.encode("utf-8")).hexdigest(), 16)
        random.seed(title_hash)
        mark = random.randint(10, 100)
        mark_str = str(mark)[:-1] + '.' + str(mark)[-1:]
        text = f'豆瓣评分：{mark_str}'
        return await message.reply_text(text, quote=False)
    return None


async def unpin_channel_post(client: Client, message: Message):
    try:
        await asyncio.sleep(2)
        await client.unpin_chat_message(message.chat.id, message.id)
    except Exception as e:
        logging.warning(f'Failed to unpin channel post: {e}')
        logging.warning(f'{message=}')
