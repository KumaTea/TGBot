from time import sleep
from botInfo import self_id
from botSession import kuma
from datetime import datetime
from telegram.error import BadRequest, ChatMigrated

try:
    from localDb import trusted_group
except ImportError:
    trusted_group = []


usage = '用法\n' \
        '向对象的消息 *回复* `/title <text>` 以添加头衔\n' \
        '字数 *16* 以内，不支持 emoji\n\n' \
        '`/title list` 列出所有头衔'
list_commands = ['list', 'print', 'dump']


def get_user_name(user):
    lang = user.language_code or 'zh'
    if user.last_name:
        if 'zh' in lang:
            return f'{user.first_name}{user.last_name}'
        else:
            return f'{user.first_name} {user.last_name}'
    else:
        return user.first_name


def get_admin_titles(chat_id):
    admin_titles = {}
    admins = kuma.get_chat_administrators(chat_id)
    for member in admins:
        if member.custom_title:
            admin_titles[member.custom_title] = admin_titles.get(member.custom_title, [])
            admin_titles[member.custom_title].append(get_user_name(member.user))
        else:
            admin_titles['AdminWithoutTitle'] = admin_titles.get('AdminWithoutTitle', [])
            admin_titles['AdminWithoutTitle'].append(get_user_name(member.user))
            # This key must exceed 16 characters, which is the length of the longest title
    return admin_titles


def print_admin_titles(chat_id):
    chat_name = kuma.get_chat(chat_id).title
    date = datetime.now().strftime('%Y%m%d')
    text = f'*{chat_name}*\n头衔列表  {date}\n\n'

    admin_titles = get_admin_titles(chat_id)
    admin_titles_list = list(admin_titles.keys())
    if 'AdminWithoutTitle' in admin_titles_list:
        admin_titles_list.remove('AdminWithoutTitle')
    # max_length = max([max([len(i) for i in admin_titles_list] or [0]), len('无名氏')])
    # align_length = max_length + len('【】  ')
    for admin_title in admin_titles:
        if admin_title != 'AdminWithoutTitle':
            # text += ('{:　<' + str(align_length) + '}{}\n').format(
            #     f'【{admin_title}】  ', ', '.join(admin_titles[admin_title]))
            text += '{}  {}\n'.format(f'【{admin_title}】', ', '.join(admin_titles[admin_title]))
    if 'AdminWithoutTitle' in admin_titles:
        # text += ('{:<' + str(align_length) + '}{}\n').format(
        #     f'【无名氏】  ', ', '.join(admin_titles['AdminWithoutTitle']))
        text += '{}  {}\n'.format('【无名氏】', ', '.join(admin_titles['AdminWithoutTitle']))
    return text


def title(update, context):
    message = update.message
    text = message.text
    chat_id = message.chat.id
    title_index = text.find(' ')

    promoted = False

    if title_index == -1:
        resp = update.message.reply_text(usage, parse_mode='Markdown', disable_web_page_preview=True, quote=False)
    else:
        reply = message.reply_to_message
        if reply:
            can_promote = kuma.get_chat_member(chat_id, self_id).can_promote_members
            if can_promote:
                authorized = False
                if chat_id in trusted_group:
                    authorized = True
                else:
                    op = kuma.get_chat_member(chat_id, message.from_user.id)
                    op_is_admin = op.can_promote_members or 'creator' in op.status
                    if op_is_admin:
                        authorized = True
                if authorized:
                    target_is_admin = 'admin' in kuma.get_chat_member(chat_id, reply.from_user.id).status
                    if not target_is_admin:
                        try:
                            if chat_id in trusted_group:
                                kuma.promote_chat_member(chat_id, reply.from_user.id,
                                                         can_manage_chat=True, can_delete_messages=True,
                                                         can_promote_members=True, can_change_info=True,
                                                         can_invite_users=True, can_pin_messages=True)
                            else:
                                kuma.promote_chat_member(chat_id, reply.from_user.id,
                                                         can_manage_chat=False, can_delete_messages=False,
                                                         can_promote_members=False, can_change_info=False,
                                                         can_invite_users=True, can_pin_messages=False)
                            sleep(2)
                            promoted = True
                        except BadRequest:
                            return update.message.reply_text('权限不足，设为管理失败', quote=False)
                    try:
                        title_to_set = text[title_index+1:title_index+1+16]
                        kuma.set_chat_administrator_custom_title(chat_id, reply.from_user.id, title_to_set)

                        name = reply.from_user.first_name
                        if reply.from_user.last_name:
                            name += ' ' + reply.from_user.last_name
                        has_set = '设置了'
                        if promoted:
                            has_set = '设为管理并设置了'
                        result = f'已为 {name} {has_set}「{title_to_set}」头衔。'
                        resp = update.message.reply_text(result, quote=False)
                    except BadRequest:
                        if chat_id > 0:
                            error_msg = '本群还不是超级群 (supergroup)，请尝试设为公开或允许新成员查看历史记录'
                        else:
                            error_msg = '权限不足，请查看我的权限是否足够，以及对象是否为bot / 已被设为管理'
                        resp = update.message.reply_text(error_msg, quote=False)
                    except ChatMigrated:
                        resp = update.message.reply_text('已升级到超级群但群ID未变，请稍后重试', quote=False)
                    except Exception as e:
                        resp = update.message.reply_text(f'未知错误：\n{e}', quote=False)
                else:
                    resp = update.message.reply_text('您的权限不足，我无权操作', quote=False)
            else:
                resp = update.message.reply_text('我还没有提拔群友的权限', quote=False)
        else:
            command = text[title_index+1:]
            if command.lower() in list_commands:
                resp = update.message.reply_text(print_admin_titles(chat_id), parse_mode='Markdown', quote=False)
            else:
                resp = update.message.reply_text(usage, parse_mode='Markdown', disable_web_page_preview=True, quote=False)
    return resp
