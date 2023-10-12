import os
import re
import bot_db
from random import choice
from pyrogram import Client
from pyrogram.types import Message
from tools import trimmer, trim_key
from tools_tg import get_file, get_user_name
from pyrogram.enums.parse_mode import ParseMode


candidates = []


async def replace_brackets(message: Message):
    text = message.text or message.caption
    result = re.findall(bot_db.brackets_re, text)
    if len(result) == 0:
        return None
    elif len(result) == 1 and text.endswith(result[0]):
        return None
    else:
        for i in result:
            text = text.replace(i, choice(candidates), 1)
        return await message.reply_text(text, quote=False)


def get_poll_groups():
    if os.path.isfile(bot_db.pool_groups_file):
        with open(bot_db.pool_groups_file, 'r', encoding='utf-8') as file:
            for line in file:
                bot_db.pool_groups.append(int(line.strip()))
    return bot_db.pool_groups


def write_poll_groups(groups: list):
    with open(bot_db.pool_groups_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(groups))


def add_poll_group(group_id: int):
    if group_id not in bot_db.pool_groups:
        bot_db.pool_groups.append(group_id)
        write_poll_groups(bot_db.pool_groups)


async def enable_group(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in bot_db.pool_groups:
        return await message.reply_text('本群已经启用抽奖了', quote=False)
    else:
        add_poll_group(chat_id)
        return await message.reply_text('本群成功启用抽奖！', quote=False)


async def disable_group(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in bot_db.pool_groups:
        bot_db.pool_groups.remove(chat_id)
        write_poll_groups(bot_db.pool_groups)
        return await message.reply_text('本群成功禁用抽奖！', quote=False)
    else:
        return await message.reply_text('本群已经禁用抽奖了', quote=False)


async def kw_reply(message: Message):
    text = message.text or message.caption
    include_list = bot_db.kw_reply_list

    text_to_reply = ''
    match_item = ''
    for item in include_list:
        keywords = include_list[item]['keywords']
        for keyword in keywords:
            if keyword in text.lower():
                if include_list[item]['reply']:
                    text_to_reply = include_list[item]['reply']
                else:
                    text_to_reply = text
                match_item = item
                break
        if text_to_reply:
            if 'skip' in include_list[match_item]:
                keywords = include_list[match_item]['skip']
                for keyword in keywords:
                    if keyword in text.lower():
                        # text_to_reply = ''
                        # break
                        return None
    if text_to_reply:
        return await message.reply_text(text_to_reply, quote=include_list[match_item]['quote'])
    return None
