import os
import re
import pickle
import bot_db
import asyncio
from random import choice
from pyrogram import Client
from tools_tg import is_admin
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


class PollGroups:
    def __init__(self):
        self.groups = []

    def read_poll_groups(self):
        if os.path.isfile(bot_db.poll_groups_file):
            with open(bot_db.poll_groups_file, 'r', encoding='utf-8') as file:
                for line in file:
                    self.groups.append(int(line.strip()))
        return self.groups

    def write_poll_groups(self):
        with open(bot_db.poll_groups_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join([str(group) for group in self.groups]))

    def add_poll_group(self, group_id: int):
        # if group_id not in poll_groups.groups:
        self.groups.append(group_id)
        self.write_poll_groups()

    def del_poll_group(self, group_id: int):
        # if group_id in poll_groups.groups:
        self.groups.remove(group_id)
        self.write_poll_groups()


poll_groups = PollGroups()


async def enable_group(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in poll_groups.groups:
        return await message.reply_text('本群已经启用抽奖了', quote=False)
    else:
        if await is_admin(chat_id, message.from_user.id, client):
            poll_groups.add_poll_group(chat_id)
            return await message.reply_text('本群成功启用抽奖！', quote=False)
        else:
            return await message.reply_text('仅管理员可操作', quote=False)


async def disable_group(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in poll_groups.groups:
        if await is_admin(chat_id, message.from_user.id, client):
            poll_groups.del_poll_group(chat_id)
            return await message.reply_text('本群成功禁用抽奖！', quote=False)
        else:
            return await message.reply_text('仅管理员可操作', quote=False)
    else:
        return await message.reply_text('本群没有启用抽奖', quote=False)


class PollCandidates:
    def __init__(self):
        self.candidates = {}
        self.read_candidates()
        if not self.candidates:
            self.candidates = {5273618487: 'Kuma'}

    def read_candidates(self):
        if os.path.isfile(bot_db.poll_candidates_file):
            with open(bot_db.poll_candidates_file, 'rb') as file:
                self.candidates = pickle.load(file)
        return self.candidates

    def write_candidates(self):
        with open(bot_db.poll_candidates_file, 'wb') as file:
            pickle.dump(self.candidates, file)

    def add_candidate(self, user_id: int, name: str):
        self.candidates[user_id] = name
        self.write_candidates()

    def del_candidate(self, user_id: int):
        del self.candidates[user_id]
        self.write_candidates()


poll_candidates = PollCandidates()


async def kw_reply(message: Message):
    chat_id = message.chat.id
    if chat_id not in poll_groups.groups:
        return None

    text = message.text or message.caption
    include_list = bot_db.kw_reply_dict

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
        if 'RANDUSER' in text_to_reply:
            text_to_reply = text_to_reply.replace('RANDUSER', choice(list(poll_candidates.candidates.values())))
        return await message.reply_text(text_to_reply, quote=include_list[match_item]['quote'])
    return None


async def replace_brackets(message: Message):
    # pool_candidates = {
    #    id: 'name',
    # }
    candidates = list(poll_candidates.candidates.values())
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


async def apply_delete_from_candidates(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id in poll_candidates.candidates:
        inform_text = (f'你的昵称：{poll_candidates.candidates[user_id]}\n'
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
            poll_candidates.del_candidate(user_id)
            async_tasks.append(message.edit_text('删除成功！'))
            async_tasks.append(callback_query.answer('删除成功！'))
        else:
            async_tasks.append(message.edit_text('已取消删除'))
            async_tasks.append(callback_query.answer('已取消删除'))
    else:
        async_tasks.append(callback_query.answer('不是你的别乱按！', show_alert=True))
    return await asyncio.gather(*async_tasks)


async def apply_add_to_candidates(client: Client, message: Message):
    user_id = message.from_user.id
    command = message.text
    content_index = command.find(' ')

    if content_index == -1:
        return await message.reply(
            '请在命令后面加上昵称\n'
            '`/help poll`',
            parse_mode=ParseMode.MARKDOWN,
            quote=False
        )

    name = command[content_index + 1:].strip()
    if len(name) > 2:
        return await message.reply(
            '昵称不可超过两个字\n'
            '`/help poll`',
            parse_mode=ParseMode.MARKDOWN,
            quote=False
        )
    if not (name.endswith('比') or name.endswith('批') or name[-1] == name[-2]):
        return await message.reply(
            '昵称必须以「比」「批」结尾或为叠词\n'
            '`/help poll`',
            parse_mode=ParseMode.MARKDOWN,
            quote=False
        )

    if user_id in poll_candidates.candidates:
        return await message.reply(
            f'你已经有昵称 {poll_candidates.candidates[user_id]} 了\n'
            f'如需更改请先删除\n'
            f'`/help poll`',
            parse_mode=ParseMode.MARKDOWN,
            quote=False
        )

    if name in poll_candidates.candidates.values():
        return await message.reply(
            f'昵称 {name} 已被使用\n'
            f'`/help poll`',
            parse_mode=ParseMode.MARKDOWN,
            quote=False
        )

    inform_text = (f'你的昵称：{name}\n'
                   f'正在等待管理员确认……')
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
    elif callback_query.from_user.id in bot_db.poll_admins and confirm == 'y':
        poll_candidates.add_candidate(user_id, name)
        async_tasks.append(message.edit_text(f'你的昵称：{name}\n添加成功！'))
        async_tasks.append(callback_query.answer('添加成功！'))
    else:
        async_tasks.append(callback_query.answer('不是你的别乱按！', show_alert=True))
    return await asyncio.gather(*async_tasks)


async def poll_callback_handler(client, callback_query):
    subtask = callback_query.data.split('_')[1]

    if subtask == 'add':
        return await callback_add(client, callback_query)
    elif subtask == 'del':
        return await callback_delete(client, callback_query)
    return None
