import asyncio
from pyrogram import Client
from typing import Optional
from bot.tools import get_user_name
from bot.trust import enabled_groups
from pyrogram.types import User, Message
from share.local import trusted_group, bl_users


async def welcome(user: User, message: Message) -> Message:
    text = f'欢迎新成员 {user.mention()}！'
    return await message.reply_text(text, quote=False)


SPAM_KW = [
    '免费',
    '翻墙',
    'vpn',
    '直连',
    'tg',
    '电报',
]


def is_spam_user(user: User) -> bool:
    if user.id in bl_users:
        return True
    name = get_user_name(user)
    # if len(name.replace(' ', '')) > 16:
    #     return True
    # return False

    spam_points = sum(1 for kw in SPAM_KW if kw in name.lower())
    # spam_points = len(list(filter(lambda kw: kw in name.lower(), SPAM_KW)))
    return spam_points > 1


async def ban_spam_user(user: User, message: Message) -> Message:
    text = f'疑赝丁真，鉴定{user.mention("新群员")}为广告bot，已封禁！'
    del_msg, ban_user, ban_inform = await asyncio.gather(
        message.delete(),
        message.chat.ban_member(user.id),
        message.reply_text(text, quote=False)
    )
    return ban_inform


async def new_group_member(client: Client, message: Message) -> Optional[Message]:
    if message.chat.id not in enabled_groups.data | trusted_group:
        return None
    if not message.from_user and message.new_chat_members:
        return None

    auth_user = message.from_user
    new_members = message.new_chat_members

    for member in new_members:
        if member.id != auth_user.id:
            # invited
            # return await welcome(member, message)
            return None
        else:
            if is_spam_user(member):
                return await ban_spam_user(member, message)
            else:
                # return await welcome(member, message)
                return None
