import logging
from pyrogram import Client
from common.info import self_id
from mods.mark import douban_mark
from pyrogram.types import Message
from bot.auth import ensure_auth
from bot.trust import enabled_groups
from common.local import trusted_group
from common.data import administrators
from mods.poll import kw_reply, replace_brackets
from bot.tools import mention_other_bot, code_in_message
from func.private import private_get_file_id, private_unknown
from msg.general import process_id, unpin_channel_post, mention_all, cue_remind

try:
    from local_functions import local_message
except ImportError:
    logging.warning('No local functions found. Using default.')

    async def local_message(m):
        return None


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


async def public_message(client: Client, message: Message):
    return (
        await douban_mark(message) or
        await kw_reply(message) or
        await replace_brackets(message) or
        await mention_all(client, message)
    )


@ensure_auth
async def process_msg(client: Client, message: Message):
    if message:
        chat_id = message.chat.id
        if chat_id in enabled_groups.data + trusted_group:
            await process_id(message)
            if need_to_process(message):
                if chat_id in trusted_group:
                    return await local_message(message) or await public_message(client, message)
                else:
                    return await public_message(client, message)
            if is_channel_post(message):
                return await unpin_channel_post(client, message)
    return None


async def detect_msg(client: Client, message: Message):
    if message:
        chat_id = message.chat.id
        if chat_id not in trusted_group:
            return await cue_remind(client, message)
    return None


@ensure_auth
async def private_msg(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id == self_id:
        return None
    if user_id in administrators:
        return await private_get_file_id(client, message)
    else:
        return await private_unknown(client, message)


async def group_msg(client: Client, message: Message):
    await process_msg(client, message)
    await detect_msg(client, message)
