from botInfo import self_id
from botSession import kuma
from telegram.error import BadRequest, ChatMigrated

try:
    from localDb import trusted_group
except ImportError:
    trusted_group = []


usage = '用法\n' \
        '向对象的消息 **回复** `/title <text>` 以添加头衔\n' \
        '字数 **16** 以内，不支持 emoji'


def title(update, context):
    message = update.message
    text = message.text
    chat_id = message.chat.id
    command = text.split(' ')

    promoted = False

    if len(command) == 2:
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
                            promoted = True
                        except BadRequest:
                            return update.message.reply_text('权限不足，设为管理失败', quote=False)
                    try:
                        kuma.set_chat_administrator_custom_title(chat_id, reply.from_user.id, command[1][:16])

                        name = reply.from_user.first_name
                        if reply.from_user.last_name:
                            name += ' ' + reply.from_user.last_name
                        has_set = '设置了'
                        if promoted:
                            has_set = '设为管理并设置了'
                        result = f'已为 {name} {has_set} {command[1][:16]} 头衔。'
                        resp = update.message.reply_text(result, quote=False)
                    except BadRequest:
                        resp = update.message.reply_text(
                            '权限不足，请查看我的管理权限是否足够，以及对象是否是由其他管理员设为管理\n'
                            '或者本群还不是超级群 (supergroup)，请尝试设为公开或允许新成员查看历史记录', quote=False)
                    except ChatMigrated:
                        resp = update.message.reply_text(
                            '已升级到超级群但群ID未变，请稍后重试', quote=False)
                    except Exception as e:
                        resp = update.message.reply_text(f'未知错误：\n{e}', quote=False)
                else:
                    resp = update.message.reply_text('您的权限不足，我无权操作', quote=False)
            else:
                resp = update.message.reply_text('我还不是管理员嗷', quote=False)
        else:
            resp = update.message.reply_text(usage, parse_mode='Markdown', disable_web_page_preview=True, quote=False)
    else:
        resp = update.message.reply_text(usage, parse_mode='Markdown', disable_web_page_preview=True, quote=False)

    return resp
