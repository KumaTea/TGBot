from pyrogram import Client
from mods.title import title  # noqa
from mods.mbti import get_mbti
from pyrogram.types import Message
from bot.tools import unparse_markdown
from bot.auth import bl_users, ensure_auth
from bot.tools import get_file, get_user_name
from pyrogram.enums.parse_mode import ParseMode
from common.data import group_help, title_help, poll_help
from func.debugs import debug, unparse, get_chat_id, delay, eval_code  # noqa
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton


@ensure_auth
async def repeat(client: Client, message: Message):
    command = message.text
    content_index = command.find(' ')

    reply = message.reply_to_message
    if content_index == -1:
        # no text
        # /rp
        if reply:
            if reply.from_user.id in bl_users:
                return await message.reply('拒绝。')
            if reply.text:
                name = get_user_name(reply.from_user)
                if reply.entities:
                    text = unparse_markdown(reply)
                    parse_mode = ParseMode.MARKDOWN
                else:
                    text = reply.text
                    parse_mode = None
                repeat_message = name + ': \n' + text
                resp = await message.reply(repeat_message, parse_mode=parse_mode, quote=False)
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
        if message.entities:
            text = unparse_markdown(message)
            parse_mode = ParseMode.MARKDOWN
        else:
            text = command
            parse_mode = None
        reply_text = text[content_index+1:]
        if reply:
            resp = await reply.reply(reply_text, parse_mode=parse_mode, quote=True)
        else:
            resp = await message.reply(reply_text, parse_mode=parse_mode, quote=False)
    return resp


@ensure_auth
async def group_help_cmd(client: Client, message: Message):
    command = message.text
    content_index = command.find(' ')
    section = command[content_index+1:].lower()
    if content_index == -1:
        return await message.reply(group_help, quote=False)
    elif 'title' in section:
        return await message.reply(title_help, quote=False)
    elif 'poll' in section:
        return await message.reply(poll_help, quote=False)
    else:
        return await message.reply(group_help, quote=False)


@ensure_auth
async def mbti(client: Client, message: Message):
    return await get_mbti(message)


@ensure_auth
async def view_bl(client: Client, message: Message):
    inform_text = '当前全域黑名单如下。所有封禁均有充足理由，可私聊管理员获取原因。'
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('查看', callback_data='bl_view')]
    ])
    return await message.reply_text(inform_text, reply_markup=reply_markup, quote=False)


# no need to check bl
async def cb_bl_view(client: Client, callback_query: CallbackQuery):
    text = '当前封禁 ID 如下：\n\n'
    for user_id in bl_users:
        text += str(user_id) + '\n'
    return await callback_query.answer(text, show_alert=True)
