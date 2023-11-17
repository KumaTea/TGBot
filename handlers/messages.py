from pyrogram import Client
from mods.mark import douban_mark
from pyrogram.types import Message
from bot.auth import ensure_not_bl
from mods.poll import kw_reply, replace_brackets, poll_groups
from handlers.msg.general import process_id, unpin_channel_post
from bot.tools import mention_other_bot, code_in_message

try:
    from local_db import trusted_group
except ImportError:
    trusted_group = []

try:
    from local_functions import local_message, local_sticker
except ImportError:
    async def local_message(m):
        return None
    local_sticker = local_message


def is_channel_post(message: Message):
    return message.sender_chat and message.forward_from_chat and message.sender_chat.id == message.forward_from_chat.id


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
        if chat_id in poll_groups.data or chat_id in trusted_group:
            await process_id(message)
            if need_to_process(message):
                if chat_id in trusted_group:
                    return await local_message(message) or await public_message(message)
                else:
                    return await public_message(message)
            elif is_channel_post(message):
                return await unpin_channel_post(client, message)
    return None