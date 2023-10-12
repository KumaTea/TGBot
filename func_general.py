import json
import time
from title import title  # noqa
from pyrogram import Client
from pyrogram.types import Message
from bot_auth import ensure_not_bl
from tools import trimmer, trim_key
from tools_tg import get_file, get_user_name
from pyrogram.enums.parse_mode import ParseMode


@ensure_not_bl
async def debug(client: Client, message: Message):
    if message.reply_to_message:
        message = message.reply_to_message
    debug_message = json.loads(str(message))
    debug_message = trim_key(trimmer(debug_message))
    return await message.reply(f'`{debug_message}`', parse_mode=ParseMode.MARKDOWN)


@ensure_not_bl
async def delay(client: Client, message: Message):
    req_timestamp = time.perf_counter()

    resp_message = await message.reply('Checking delay...')

    resp_timestamp = time.perf_counter()
    duration = resp_timestamp - req_timestamp
    duration_str = '{:.3f} ms'.format(1000 * duration)
    if duration < 0.1:
        status = 'excellent'
    elif duration < 0.5:
        status = 'good'
    elif duration < 1:
        status = 'ok'
    else:
        status = 'bad'
    return await resp_message.edit_text(f'Delay is {duration_str}.\nThe connectivity is {status}.')


@ensure_not_bl
async def repeat(client: Client, message: Message):
    command = message.text
    content_index = command.find(' ')

    reply = message.reply_to_message
    if content_index == -1:
        # no text
        # /rp
        if reply:
            if reply.text:
                name = get_user_name(reply.from_user)
                repeat_message = name + ': \n' + reply.text
                resp = await message.reply(repeat_message, quote=False)
            else:
                file_id, file_type = get_file(reply)
                if file_id:
                    # credit: https://t.me/echoesofdream/7709
                    reply_method = getattr(message, f'reply_{file_type}')
                    resp = await reply_method(file_id, quote=False)
                else:
                    resp = None
        else:
            resp = await message.reply(command, quote=False)
    else:
        # has text
        # /rp example
        reply_text = command[content_index+1:]
        if reply:
            resp = await reply.reply(reply_text, quote=True)
        else:
            resp = await message.reply(reply_text, quote=False)
    return resp
