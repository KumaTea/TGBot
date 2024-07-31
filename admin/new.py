import asyncio
from pyrogram import Client
from typing import Optional
from common.info import creator
from bot.trust import enabled_groups
from pyrogram.types import User, Message
from share.local import bl_users, trusted_group
from bot.tools import get_user_bio, get_user_name
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant


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


async def ban_no_photo_user(user: User, message: Message) -> Message:
    text = f'疑赝丁真，鉴定{user.mention("新群员")}未设置或未开放头像，已踢出！'
    del_msg, ban_user, ban_inform = await asyncio.gather(
        message.delete(),
        message.chat.ban_member(user.id),
        message.reply_text(text, quote=False)
    )
    await asyncio.sleep(5)
    await message.chat.unban_member(user.id)
    return ban_inform


async def user_in_chat(user: User, message: Message) -> bool:
    try:
        await message.chat.get_member(user.id)
        return True
    except UserNotParticipant:
        return False


async def send_new_member_info(client: Client, user: User, message: Message) -> Message:
    is_human = '✅' if not user.is_bot else '❌'
    has_photo = '✅' if user.photo else '❌'
    has_bio = '✅' if await get_user_bio(client, user) else '❌'
    has_username = '✅' if user.username else '❌'
    not_premium = '✅' if not user.is_premium else '❌'
    name = get_user_name(user)
    text = f'欢迎新成员 {user.mention(name)}！\n\n'
    text += f'有头像：{has_photo}\n'
    text += f'有用户名：{has_username}\n'
    text += f'有简介：{has_bio}\n'
    text += f'非bot：{is_human}\n'
    text += f'非大会员：{not_premium}'

    inform_text = '看群'
    welcome_msg, inform = await asyncio.gather(
        message.reply_text(text, quote=False),
        client.send_message(creator, inform_text)
    )
    return welcome_msg


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
            return await send_new_member_info(client, member, message)
        else:
            if not member.photo:
                return await ban_no_photo_user(member, message)
            elif is_spam_user(member):
                return await ban_spam_user(member, message)
            else:
                # return await welcome(member, message)
                # wait for 3 minutes
                await asyncio.sleep(180)
                if await user_in_chat(member, message):
                    return await send_new_member_info(client, member, message)
