import asyncio
from typing import Optional
from pyrogram import Client
from bot.session import kuma
from datetime import datetime
from common.info import self_id
from bot.auth import ensure_auth
from common.data import title_help
from bot.tools import get_user_name
from pyrogram.errors import BadRequest
from pyrogram.enums import ChatMemberStatus
from pyrogram.enums.parse_mode import ParseMode
from common.local import bl_users, trusted_group
from pyrogram.types import Message, ChatPrivileges
from pyrogram.enums.chat_members_filter import ChatMembersFilter


list_commands = ['list', 'print', 'dump']


async def get_admin_titles(chat_id):
    admin_titles = {}
    admins = kuma.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS)
    # no await
    # it's a generator
    async for member in admins:
        if member.user.id in bl_users or not get_user_name(member.user):
            continue
        titles = admin_titles.setdefault(member.custom_title or 'AdminWithoutTitle', [])
        titles.append(get_user_name(member.user))
        # This key must exceed 16 characters, which is the length of the longest title
    return admin_titles


async def gen_admins_summary(chat_id):
    # chat_name = await kuma.get_chat(chat_id).title
    # admin_titles = await get_admin_titles(chat_id)
    chat, admin_titles = await asyncio.gather(kuma.get_chat(chat_id), get_admin_titles(chat_id))
    chat_name = chat.title
    date = datetime.now().strftime('%Y%m%d')
    text = f'**{chat_name}**\n头衔列表  {date}\n\n'

    admin_titles_list = list(admin_titles.keys())
    if 'AdminWithoutTitle' in admin_titles_list:
        admin_titles_list.remove('AdminWithoutTitle')
    # max_length = max([max([len(i) for i in admin_titles_list] or [0]), len('无名氏')])
    # align_length = max_length + len('【】  ')
    for admin_title in admin_titles:
        if admin_title != 'AdminWithoutTitle':
            # text += ('{:　<' + str(align_length) + '}{}\n').format(
            #     f'【{admin_title}】  ', ', '.join(admin_titles[admin_title]))
            text += '{}  {}\n'.format(
                f'【{admin_title}】',
                ', '.join(admin_titles[admin_title])
            )
    if 'AdminWithoutTitle' in admin_titles:
        # text += ('{:<' + str(align_length) + '}{}\n').format(
        #     f'【无名氏】  ', ', '.join(admin_titles['AdminWithoutTitle']))
        text += '{}  {}\n'.format(
            '【无名氏】',
            ', '.join(admin_titles['AdminWithoutTitle'])
        )
    return text


async def _is_authorized(client: Client, message: Message) -> bool:
    # Is this a trusted group?
    # Or is the requested user an admin?

    if message.chat.id in trusted_group:
        return True
    operator = await client.get_chat_member(message.chat.id, message.from_user.id)
    return (
        operator.status == ChatMemberStatus.OWNER or
        (operator.privileges and operator.privileges.can_promote_members)
    )


@ensure_auth
async def title(client: Client, message: Message) -> Optional[Message]:
    """Set the title of a user as an admin in a chat.

    Args:
        client: The client object to interact with the Telegram API.
        message: The message object that contains the command and arguments.

    Returns:
        A message object that contains the response, or None if no response is needed.
    """
    text = message.text
    chat_id = message.chat.id
    args = text.split()[1:]

    if not args:  # no args
        return await message.reply(title_help, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

    # with args
    reply = message.reply_to_message
    if not reply:
        # no reply but with args
        if args[0].lower() not in list_commands:
            return await message.reply(title_help, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return await message.reply(
            await gen_admins_summary(chat_id), parse_mode=ParseMode.MARKDOWN, quote=False
        )

    # detect replied user
    if reply.from_user.id == self_id:
        return await message.reply('我无法给自己添加头衔！')
    if reply.from_user.id in bl_users:
        return await message.reply('拒绝。')

    # can I promote?
    bot_status = await client.get_chat_member(chat_id, self_id)
    can_promote = bot_status.privileges and bot_status.privileges.can_promote_members

    if not can_promote:
        return await message.reply('我还没有提拔群友的权限')

    if not await _is_authorized(client, message):
        return await message.reply('你的权限不足，我无权操作')

    target = await client.get_chat_member(chat_id, reply.from_user.id)
    promoting = target.status is not ChatMemberStatus.ADMINISTRATOR

    # set as admin first
    if promoting:
        trusted = chat_id in trusted_group
        try:
            await client.promote_chat_member(
                chat_id, reply.from_user.id,
                ChatPrivileges(
                    can_manage_chat=trusted, can_delete_messages=False,
                    can_manage_video_chats=trusted, can_restrict_members=trusted,
                    can_promote_members=trusted, can_change_info=trusted,
                    can_invite_users=True, can_pin_messages=trusted,
                    is_anonymous=False
                )
            )
        except BadRequest:
            return await message.reply('权限不足，设为管理失败')

    # set title
    try:
        title_to_set = ' '.join(args)  # support spaces
        await client.set_administrator_title(chat_id, reply.from_user.id, title_to_set)
        name = get_user_name(reply.from_user)
        has_set = '设为管理并设置了' if promoting else '设置了'
        return await message.reply(f'已将 {name} {has_set}「{title_to_set}」头衔。')
    except BadRequest:
        if chat_id > 0:
            error_msg = '本群还不是超级群 (supergroup)，请尝试设为公开或允许新成员查看历史记录'
        else:
            error_msg = '权限不足，请查看我的权限是否足够，以及对象是否为bot / 已 被设为管理'
        return await message.reply(error_msg)
    # except ChatMigrated:
    #     return message.reply('已升级到超级群但群ID未变，请稍后重试')
    except Exception as e:
        return await message.reply(f'未知错误：\n{e}')
