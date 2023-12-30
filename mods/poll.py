import re
import asyncio
from random import choice
from pyrogram import Client
from bot.tools import is_admin
from common.info import self_id
from common.local import trusted_group
from pyrogram.enums.parse_mode import ParseMode
from bot.auth import ensure_not_bl, enabled_groups, poll_candidates
from common.data import poll_help, poll_admins, kw_reply_dict, brackets_re
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


brackets_pattern = re.compile(brackets_re)


async def am_i_admin(client: Client, chat_id: int):
    me = await client.get_chat_member(chat_id, self_id)
    return all([
        me.privileges.can_delete_messages,
        me.privileges.can_restrict_members,
        me.privileges.can_promote_members,
    ])


@ensure_not_bl
async def enable_group(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in enabled_groups.data:
        return await message.reply_text('本群已经启用扩展功能了。', quote=False)
    elif chat_id in trusted_group:
        return await message.reply_text('本群为受信群，默认启用扩展功能。注意某些彩蛋亦已启用。', quote=False)
    else:
        if await is_admin(chat_id, message.from_user.id, client):
            if await am_i_admin(client, chat_id):
                enabled_groups.add_item(chat_id)
                return await message.reply_text('本群成功启用扩展功能！豆瓣评分、关键词回复、群员抽奖等功能现已生效。', quote=False)
            else:
                return await message.reply_text('我还没有获得删除消息、封禁用户及提拔用户权限，设置失败。', quote=False)
        else:
            return await message.reply_text('仅管理员可操作！', quote=False)


@ensure_not_bl
async def disable_group(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in enabled_groups.data:
        if await is_admin(chat_id, message.from_user.id, client):
            enabled_groups.del_item(chat_id)
            return await message.reply_text('本群成功禁用扩展功能。', quote=False)
        else:
            return await message.reply_text('仅管理员可操作！', quote=False)
    elif chat_id in trusted_group:
        return await message.reply_text('我看你是想太多？', quote=False)
    else:
        return await message.reply_text('本群尚未启用扩展功能。', quote=False)


async def kw_reply(message: Message, include_dict: dict = None, candidates: list = None):
    text = message.text or message.caption
    if not text:
        return None
    if not include_dict:
        include_dict = kw_reply_dict

    text_to_reply = ''
    match_item = ''
    for item in include_dict:
        keywords = include_dict[item]['keywords']
        for keyword in keywords:
            if keyword in text.lower():
                if include_dict[item]['reply']:
                    text_to_reply = include_dict[item]['reply']
                else:
                    text_to_reply = text
                match_item = item
                break
        if text_to_reply:
            if 'skip' in include_dict[match_item]:
                keywords = include_dict[match_item]['skip']
                for keyword in keywords:
                    if keyword in text.lower():
                        # text_to_reply = ''
                        # break
                        return None
    if text_to_reply:
        if not candidates:
            candidates = list(poll_candidates.data.values()) + ['我']
        if 'RANDUSER' in text_to_reply:
            text_to_reply = text_to_reply.replace('RANDUSER', choice(candidates))
        return await message.reply_text(text_to_reply, quote=include_dict[match_item]['quote'])
    return None


async def replace_brackets(message: Message, candidates: list = None):
    if not candidates:
        candidates = list(poll_candidates.data.values()) + ['我']
    text = message.text or message.caption
    if not text:
        return None
    result = brackets_pattern.findall(text)
    if len(result) == 0:
        return None
    elif len(result) == 1 and text.endswith(result[0]):
        return None
    else:
        for i in result:
            text = text.replace(i, choice(candidates), 1)
        return await message.reply_text(text, quote=False)


@ensure_not_bl
async def apply_delete_from_candidates(client: Client, message: Message):
    user_id = message.from_user.id
    reply = message.reply_to_message
    if reply:
        user_id = reply.from_user.id
        if message.from_user.id not in poll_admins:
            return await message.reply_text(poll_help, parse_mode=ParseMode.MARKDOWN, quote=False)
        else:
            poll_candidates.del_item(user_id)
            return await message.reply_text('一位管理员滥权把你从池子里捞起来了！', quote=False)
    if user_id in poll_candidates.data:
        inform_text = (f'你的昵称：{poll_candidates.data[user_id]}\n'
                       f'是否确认删除？')
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('确认', callback_data=f'poll_del_{user_id}_y')],
            [InlineKeyboardButton('取消', callback_data=f'poll_del_{user_id}_n')]
        ])
        return await message.reply_text(inform_text, reply_markup=reply_markup, quote=False)
    else:
        return await message.reply_text('你还不在池子里', quote=False)


async def callback_delete(client: Client, callback_query: CallbackQuery):
    task, subtask, user_id, confirm = callback_query.data.split('_')
    user_id = int(user_id)
    message = callback_query.message
    async_tasks = []
    if callback_query.from_user.id == user_id:
        if confirm == 'y':
            poll_candidates.del_item(user_id)
            async_tasks.append(message.edit_text('删除成功！'))
            async_tasks.append(callback_query.answer('删除成功！'))
        else:
            async_tasks.append(message.edit_text('已取消删除'))
            async_tasks.append(callback_query.answer('已取消删除'))
    else:
        async_tasks.append(callback_query.answer('不是你的别乱按！', show_alert=True))
    return await asyncio.gather(*async_tasks)


@ensure_not_bl
async def apply_add_to_candidates(client: Client, message: Message):
    user_id = message.from_user.id
    command = message.text
    content_index = command.find(' ')
    reply = message.reply_to_message
    if reply:
        user_id = reply.from_user.id

    if content_index == -1:
        return await message.reply(
            '请在命令后面加上昵称\n'
            '`/help poll`',
            parse_mode=ParseMode.MARKDOWN,
            quote=False
        )

    name = command[content_index + 1:].strip()
    if not reply:
        try:
            if len(name.encode('gbk')) != 4:
                return await message.reply(
                    '昵称必须为两个字\n'
                    '`/help poll`',
                    parse_mode=ParseMode.MARKDOWN,
                    quote=False
                )
        except UnicodeEncodeError:
            return await message.reply(
                '禁止使用无法被 `gbk` 编码的字符\n',
                parse_mode=ParseMode.MARKDOWN,
                quote=False
            )

        if not (name.endswith('比') or name.endswith('批') or name[-1] == name[-2] or name.encode().isalpha()):
            return await message.reply(
                '昵称必须以「比」「批」结尾或为叠词\n'
                '`/help poll`',
                parse_mode=ParseMode.MARKDOWN,
                quote=False
            )

    if user_id in poll_candidates.data:
        return await message.reply(
            f'你已经有昵称 {poll_candidates.data[user_id]} 了\n'
            f'如需更改请先删除\n'
            f'`/help poll`',
            parse_mode=ParseMode.MARKDOWN,
            quote=False
        )

    if name in poll_candidates.data.values():
        return await message.reply(
            f'昵称 {name} 已被使用\n'
            f'`/help poll`',
            parse_mode=ParseMode.MARKDOWN,
            quote=False
        )

    if reply:
        if message.from_user.id in poll_admins:
            inform_text = (
                f'一位管理员想要为你添加昵称：{name}\n'
                f'是否确认？'
            )
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton('确认 (自)', callback_data=f'poll_invite_{user_id}_y')],
                [InlineKeyboardButton('取消 (管)', callback_data=f'poll_invite_{user_id}_n')]
            ])
        else:
            return await message.reply_text(poll_help, parse_mode=ParseMode.MARKDOWN, quote=False)
    else:
        inform_text = (
            f'你的昵称：{name}\n'
            f'正在等待管理员确认……'
        )
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('确认 (管)', callback_data=f'poll_add_{user_id}_y')],
            [InlineKeyboardButton('取消 (自)', callback_data=f'poll_add_{user_id}_n')]
        ])
    return await message.reply_text(inform_text, reply_markup=reply_markup, quote=False)


async def callback_add(client: Client, callback_query: CallbackQuery):
    task, subtask, user_id, confirm = callback_query.data.split('_')
    user_id = int(user_id)
    message = callback_query.message
    name = message.text.split('：')[1].split('\n')[0]
    async_tasks = []
    if callback_query.from_user.id == user_id and confirm == 'n':
        async_tasks.append(message.edit_text('已取消添加'))
        async_tasks.append(callback_query.answer('已取消添加'))
    elif callback_query.from_user.id in poll_admins and confirm == 'y':
        poll_candidates.add_item(user_id, name)
        async_tasks.append(message.edit_text(f'你的昵称：{name}\n添加成功！'))
        async_tasks.append(callback_query.answer('添加成功！'))
    else:
        async_tasks.append(callback_query.answer('不是你的别乱按！', show_alert=True))
    return await asyncio.gather(*async_tasks)


async def callback_invite(client: Client, callback_query: CallbackQuery):
    task, subtask, user_id, confirm = callback_query.data.split('_')
    user_id = int(user_id)
    message = callback_query.message
    name = message.text.split('：')[1].split('\n')[0]
    async_tasks = []
    if (callback_query.from_user.id in poll_admins or callback_query.from_user.id == user_id) and confirm == 'n':
        async_tasks.append(message.edit_text('已取消添加'))
        async_tasks.append(callback_query.answer('已取消添加'))
    elif callback_query.from_user.id == user_id and confirm == 'y':
        poll_candidates.add_item(user_id, name)
        async_tasks.append(message.edit_text(f'你的昵称：{name}\n添加成功！'))
        async_tasks.append(callback_query.answer('添加成功！'))
    else:
        async_tasks.append(callback_query.answer('不是你的别乱按！', show_alert=True))
    return await asyncio.gather(*async_tasks)


@ensure_not_bl
async def view_candidates(client: Client, message: Message):
    inform_text = '按下面按钮查看'
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('查看', callback_data='poll_view')]
    ])
    return await message.reply_text(inform_text, reply_markup=reply_markup, quote=False)


async def callback_view(client: Client, callback_query: CallbackQuery):
    candidates = poll_candidates.data
    if candidates:
        text = '抽奖池：\n'
        text += ', '.join(list(poll_candidates.data.values()))
    else:
        text = '抽奖池为空'
    return await callback_query.answer(text, show_alert=True)


async def poll_callback_handler(client, callback_query):
    subtask = callback_query.data.split('_')[1]

    if subtask == 'add':
        return await callback_add(client, callback_query)
    elif subtask == 'invite':
        return await callback_invite(client, callback_query)
    elif subtask == 'del':
        return await callback_delete(client, callback_query)
    elif subtask == 'view':
        return await callback_view(client, callback_query)
    return None
