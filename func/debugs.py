import json
import time
from common.data import *
from pyrogram import Client
from mods.title import title
from mods.mbti import get_mbti
from pyrogram.types import Message
from bot.tools import unparse_markdown
from common.tools import trimmer, trim_key
from bot.auth import bl_users, ensure_not_bl
from bot.tools import get_file, get_user_name
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton




@ensure_not_bl
async def debug(client: Client, message: Message):
    if message.reply_to_message:
        message = message.reply_to_message
    debug_message = json.loads(str(message))
    debug_message = trim_key(trimmer(debug_message))
    return await message.reply(f'`{debug_message}`', parse_mode=ParseMode.MARKDOWN)


@ensure_not_bl
async def unparse(client: Client, message: Message):
    if message.reply_to_message:
        message = message.reply_to_message
    if message.entities:
        text = unparse_markdown(message)
    else:
        text = message.text
    return await message.reply(text, parse_mode=ParseMode.DISABLED)


@ensure_not_bl
async def get_chat_id(client: Client, message: Message):
    return await message.reply(f'`{message.chat.id}`', parse_mode=ParseMode.MARKDOWN)
