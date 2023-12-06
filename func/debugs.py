import json
import time
import pprint
from pyrogram import Client
from pyrogram.types import Message
from bot.auth import ensure_not_bl
from bot.tools import unparse_markdown
from common.tools import trimmer, trim_key
from pyrogram.enums.parse_mode import ParseMode


@ensure_not_bl
async def debug(client: Client, message: Message):
    if message.reply_to_message:
        message = message.reply_to_message
    debug_message = json.loads(str(message))
    debug_message = trim_key(trimmer(debug_message))
    p = pprint.PrettyPrinter(indent=2)
    debug_message = p.pformat(debug_message)
    return await message.reply(f'```\n{debug_message}```', parse_mode=ParseMode.MARKDOWN, quote=False)


@ensure_not_bl
async def unparse(client: Client, message: Message):
    if message.reply_to_message:
        message = message.reply_to_message
    if not message.text:
        return await message.reply('啥也不说，找我干嘛？', quote=False)
    if message.entities:
        text = unparse_markdown(message)
    else:
        text = message.text
    return await message.reply(text, parse_mode=ParseMode.DISABLED, quote=False)


@ensure_not_bl
async def get_chat_id(client: Client, message: Message):
    return await message.reply(f'`{message.chat.id}`', parse_mode=ParseMode.MARKDOWN, quote=False)


@ensure_not_bl
async def delay(client: Client, message: Message) -> Message:
    req_timestamp = time.perf_counter()
    resp_message = await message.reply('Checking delay...')
    resp_timestamp = time.perf_counter()

    duration = resp_timestamp - req_timestamp
    duration_str = '{:.3f} ms'.format(1000 * duration)

    ms = 0.001
    if duration < 50 * ms:
        status = 'excellent'
    elif duration < 100 * ms:
        status = 'good'
    elif duration < 300 * ms:
        status = 'ok'
    else:
        status = 'bad'

    response = (
        f'Delay: {duration_str}\n'
        f'Status: {status}'
    )
    return await resp_message.edit_text(response)
