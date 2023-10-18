import re
import random
import hashlib
from pyrogram import Client
from local_db import trusted_group
from pyrogram.types import Message
from bot_auth import ensure_not_bl
from pyrogram.enums import ParseMode
from mod_poll import kw_reply, replace_brackets
from tools_tg import mention_other_bot, code_in_message

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


def need_to_process(message: Message):
    text = message.text or message.caption
    if text:
        if message.from_user:
            user_id = message.from_user.id
            if user_id > 0:
                if not mention_other_bot(text) and not code_in_message(message):
                    return True
    return False


async def public_message(message: Message):
    return await douban_mark(message) or await kw_reply(message) or await replace_brackets(message)


@ensure_not_bl
async def process_msg(client: Client, message: Message):
    if message:
        chat_id = message.chat.id
        await process_id(message)
        if need_to_process(message):
            if chat_id in trusted_group:
                return await local_message(message) or await public_message(message)
            else:
                return await public_message(message)
    return None
