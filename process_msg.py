import re
import random
import hashlib
import asyncio
from pyrogram import Client
from localDb import trusted_group  # , sticker_bl
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from tools import mention_other_bot, run_async_funcs

try:
    from local_functions import local_message
except ImportError:
    async def local_message(m):
        return None
    local_sticker = local_message


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


async def douban_mark(message: Message):
    title_re = r'《.+》'
    text = message.text or message.caption
    result = re.findall(title_re, text)
    if result:
        title = result[0][1:-1].strip().lower()
        title_hash = int(hashlib.md5(title.encode("utf-8")).hexdigest(), 16)
        random.seed(title_hash)
        mark = random.randint(10, 100)
        mark_str = str(mark)[:-1] + '.' + str(mark)[-1:]
        text = f'豆瓣评分：{mark_str}'
        return await message.reply_text(text, quote=False)
    return None


async def public_message(message: Message):
    return await douban_mark(message)


async def process_msg(client: Client, message: Message):
    async_tasks = []
    if message:
        chat_id = message.chat.id
        async_tasks.append(process_id(message))
        text = message.text or message.caption
        if text:
            if message.from_user:
                user_id = message.from_user.id
                if user_id > 0:
                    if not mention_other_bot(text):
                        if chat_id in trusted_group:
                            # return await public_message(message) or await local_message(message)
                            async_tasks.append(run_async_funcs([public_message(message), local_message(message)]))
                        else:
                            async_tasks.append(public_message(message))
        # elif message.sticker:
        #     if chat_id in trusted_group:
        #         return public_sticker(message: Message)
    if async_tasks:
        return await asyncio.gather(*async_tasks)
    return None
