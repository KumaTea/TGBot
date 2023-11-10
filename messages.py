from pyrogram import Client
from local_db import trusted_group
from pyrogram.types import Message
from bot_auth import ensure_not_bl
from mod_poll import kw_reply, replace_brackets
from tools_tg import mention_other_bot, code_in_message
from msg_general import process_id, douban_mark, unpin_channel_post

try:
    from local_functions import local_message
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
        await process_id(message)
        if need_to_process(message):
            if chat_id in trusted_group:
                return await local_message(message) or await public_message(message)
            else:
                return await public_message(message)
        elif is_channel_post(message):
            return await unpin_channel_post(client, message)
    return None
