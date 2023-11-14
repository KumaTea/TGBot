import re
import random
import hashlib
from bot_db import title_re
from pyrogram.types import Message


title_pattern = re.compile(title_re)


async def douban_mark(message: Message):
    text = message.text or message.caption
    result = title_pattern.findall(text)
    if result:
        title = result[0][1:-1].strip().lower()
        title_hash = int(hashlib.md5(title.encode("utf-8")).hexdigest(), 16)
        rng = random.Random(title_hash)
        mark = rng.randint(10, 100)
        mark_str = str(mark)[:-1] + '.' + str(mark)[-1:]
        text = f'豆瓣评分：{mark_str}'
        return await message.reply_text(text, quote=False)
    return None
