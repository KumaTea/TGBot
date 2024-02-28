import json
import time
import pprint
from pyrogram import Client
from typing import Optional
from bot.auth import ensure_auth
from func.tools import get_content
from pyrogram.types import Message
from common.local import known_group
from common.tools import trimmer, trim_key
from pyrogram.enums.parse_mode import ParseMode
from common.data import administrators, REFUSE_STICKER
from bot.tools import unparse_markdown, get_chat_member_ids


@ensure_auth
async def debug(client: Client, message: Message):
    if message.reply_to_message:
        message = message.reply_to_message
    debug_message = json.loads(str(message))
    debug_message = trim_key(trimmer(debug_message))
    p = pprint.PrettyPrinter(indent=2)
    debug_message = p.pformat(debug_message)
    return await message.reply(f'```\n{debug_message}```', parse_mode=ParseMode.MARKDOWN, quote=False)


@ensure_auth
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


@ensure_auth
async def get_chat_id(client: Client, message: Message):
    return await message.reply(f'`{message.chat.id}`', parse_mode=ParseMode.MARKDOWN, quote=False)


@ensure_auth
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


# @ensure_auth
async def command_get_users(client: Client, message: Message) -> Optional[Message]:
    if message.from_user.id not in administrators:
        return None
    # if known_user_ids.data:
    #     return await message.reply_text('Already known.')
    # else:
    chat_id = -1001932978232  # Dic
    user_ids = await get_chat_member_ids(client, chat_id)
    user_ids_str = '\n'.join([str(user_id) for user_id in user_ids])
    return await message.reply_text(f'Data: ```log\n{user_ids_str}\n```')


# @ensure_auth
async def command_get_groups(client: Client, message: Message) -> Optional[Message]:
    if message.from_user.id not in administrators:
        return None
    group_ids_str = '\n'.join([str(group_id) for group_id in known_group])
    return await message.reply_text(f'Data: ```log\n{group_ids_str}\n```')


async def eval_code_core(client: Client, message: Message, output=True) -> Optional[tuple[str, int]]:
    # return: result, success_code
    content = get_content(message)
    if not content:
        return str(client), 0
    else:
        attr_splitter = ['(', '.', '[']
        attr = content
        for splitter in attr_splitter:
            attr = attr.split(splitter)[0]
        if not hasattr(client, attr):
            return f'No attribute named {attr}.', 1

        is_callable = callable(getattr(client, attr))
        if not is_callable:
            # return getattr(client, content), 0
            return eval(f'client.{content}'), 0

        try:
            # func = eval(f'client.{content}')  # async or result of sync
            # is_async = hasattr(func, '__await__')
            result = await eval(f'client.{content}')
            if output:
                return result, 0
            return 'Done.', 0
        except Exception as e:
            return str(e), 1


@ensure_auth
async def eval_code(client: Client, message: Message) -> Optional[Message]:
    if message.from_user.id not in administrators:
        return await message.reply_sticker(REFUSE_STICKER, quote=False)
    result, success_code = await eval_code_core(client, message)
    result = str(result)
    status_icon = '✅' if success_code == 0 else '❌'
    text = f'{status_icon}\n\n'
    if len(result) > 100:
        text += f'```log\n{result}```'
    else:
        text += f'`{result}`'
    return await message.reply(text, quote=False)
