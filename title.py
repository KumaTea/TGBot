import asyncio
from session import kuma
from pyrogram import Client
from bot_info import self_id
from datetime import datetime
from tools import get_user_name
from pyrogram.errors import BadRequest
from pyrogram.enums import ChatMemberStatus
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import ChatPrivileges, Message
from pyrogram.enums.chat_members_filter import ChatMembersFilter

try:
    from localDb import trusted_group
except ImportError:
    trusted_group = []


usage = '用法\n' \
        '向对象的消息 **回复** `/title <text>` 以添加头衔\n' \
        '字数 **16** 以内，不支持 emoji\n\n' \
        '`/title list` 列出所有头衔'
list_commands = ['list', 'print', 'dump']


async def get_admin_titles(chat_id):
    admin_titles = {}
    admins = kuma.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS)
    # no await
    # it's a generator
    async for member in admins:
        if member.custom_title:
            admin_titles[member.custom_title] = admin_titles.get(member.custom_title, [])
            admin_titles[member.custom_title].append(get_user_name(member.user))
        else:
            admin_titles['AdminWithoutTitle'] = admin_titles.get('AdminWithoutTitle', [])
            admin_titles['AdminWithoutTitle'].append(get_user_name(member.user))
            # This key must exceed 16 characters, which is the length of the longest title
    return admin_titles


async def gen_admins_summary(chat_id):
    # chat_name = await kuma.get_chat(chat_id).title
    # admin_titles = await get_admin_titles(chat_id)
    async_tasks = [
        kuma.get_chat(chat_id),
        get_admin_titles(chat_id)
    ]
    chat, admin_titles = await asyncio.gather(*async_tasks)
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


async def title(client: Client, message: Message):
    text = message.text
    chat_id = message.chat.id
    title_index = text.find(' ')

    promoted = False

    if title_index == -1:  # no args
        resp = await message.reply(usage, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    else:  # with args
        reply = message.reply_to_message
        if reply:
            bot_status = await kuma.get_chat_member(chat_id, self_id)
            if bot_status.privileges:
                can_promote = bot_status.privileges.can_promote_members
            else:
                can_promote = False
            if can_promote:
                authorized = False
                if chat_id in trusted_group:
                    authorized = True
                else:
                    operator = await kuma.get_chat_member(chat_id, message.from_user.id)
                    if operator.privileges:
                        if operator.privileges.can_promote_members:
                            authorized = True
                    elif operator.status == ChatMemberStatus.OWNER:
                        authorized = True
                    else:
                        authorized = False
                if authorized:
                    target = await kuma.get_chat_member(chat_id, reply.from_user.id)
                    target_is_admin = target.status == ChatMemberStatus.ADMINISTRATOR
                    if not target_is_admin:
                        try:
                            if chat_id in trusted_group:
                                await kuma.promote_chat_member(
                                    chat_id, reply.from_user.id,
                                    ChatPrivileges(
                                        can_manage_chat=True, can_delete_messages=False,
                                        can_manage_video_chats=True, can_restrict_members=True,
                                        can_promote_members=True, can_change_info=True,
                                        can_invite_users=True, can_pin_messages=True,
                                        is_anonymous=False
                                    )
                                )
                            else:
                                await kuma.promote_chat_member(
                                    chat_id, reply.from_user.id,
                                    ChatPrivileges(
                                        can_manage_chat=False, can_delete_messages=False,
                                        can_manage_video_chats=False, can_restrict_members=False,
                                        can_promote_members=False, can_change_info=False,
                                        can_invite_users=True, can_pin_messages=False,
                                        is_anonymous=False
                                    )
                                )
                            promoted = True
                        except BadRequest:
                            return await message.reply('权限不足，设为管理失败')
                    try:
                        title_to_set = text[title_index+1:title_index+1+16]
                        await kuma.set_administrator_title(chat_id, reply.from_user.id, title_to_set)

                        name = get_user_name(reply.from_user)
                        has_set = '设置了'
                        if promoted:
                            has_set = '设为管理并设置了'
                        result = f'已为 {name} {has_set}「{title_to_set}」头衔。'
                        resp = await message.reply(result)
                    except BadRequest:
                        if chat_id > 0:
                            error_msg = '本群还不是超级群 (supergroup)，请尝试设为公开或允许新成员查看历史记录'
                        else:
                            error_msg = '权限不足，请查看我的权限是否足够，以及对象是否为bot / 已 被设为管理'
                        resp = await message.reply(error_msg)
                    # except ChatMigrated:
                    #     resp = message.reply('已升级到超级群但群ID未变，请稍后重试')
                    except Exception as e:
                        resp = await message.reply(f'未知错误：\n{e}')
                else:
                    resp = await message.reply('您的权限不足，我无权操作')
            else:
                resp = await message.reply('我还没有提拔群友的权限')
        else:  # no reply but with args
            command = text[title_index+1:]
            if command.lower() in list_commands:
                resp = await message.reply(await gen_admins_summary(chat_id), parse_mode=ParseMode.MARKDOWN, quote=False)
            else:
                resp = await message.reply(usage, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    return resp
