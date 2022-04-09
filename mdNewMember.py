from botSession import kuma
from localDb import welcome_chat
from botInfo import creator
from threading import Timer


def welcome(update, context):
    chat_id = update.message.chat_id
    alert_id = update.message.message_id
    new_member = update.message.new_chat_members[0]
    bot_status = new_member.is_bot
    if chat_id in welcome_chat and not bot_status:
        resp = True
        user_id = new_member.id
        if 'message' in welcome_chat[chat_id]:
            if '{name}' in welcome_chat[chat_id]['message']:
                user_name = new_member.first_name
                if new_member.last_name:
                    user_name += ' ' + new_member.last_name
                if len(user_name) > 12:
                    user_name = user_name[:12]
                user_link = f'[{user_name}](tg://user?id={user_id})'
                formatted_message = welcome_chat[chat_id]['message'].format(name=user_link)
                welcome_message = update.message.reply_text(formatted_message, parse_mode='Markdown', quote=False)
            else:
                welcome_message = update.message.reply_text(welcome_chat[chat_id]['message'], quote=False)
            msg_id = welcome_message.message_id
        else:
            msg_id = None
        if 'sticker' in welcome_chat[chat_id]:
            welcome_sticker = update.message.reply_sticker(welcome_chat[chat_id]['sticker'], quote=False)
            sticker_id = welcome_sticker.message_id
        else:
            sticker_id = None
        check = Timer(125, check_member, [chat_id, user_id, alert_id, msg_id, sticker_id])
        check.start()  # noqa
    else:
        resp = None
    return resp


def check_member(chat_id, user_id, alert_id, msg_id=None, sticker_id=None):
    print(f'[INFO] Starting new member checking...')
    left = False
    user = kuma.get_chat_member(chat_id, user_id)
    user_status = user.status
    if 'left' in user_status or 'kick' in user_status:
        left = True

    if left:
        kuma.delete_message(chat_id, alert_id)
        if sticker_id:
            kuma.delete_message(chat_id, sticker_id)
        if msg_id:
            kuma.edit_message_text('验证机器人已移除一位未通过验证的用户。', chat_id, msg_id)
        print(f'[INFO] User {user_id} status: LEFT; NOT member.')
    else:
        print(f'[INFO] User {user_id} status: IN; IS member.')
        if msg_id:
            kuma.edit_message_text('你已经是群大佬了，快来跟萌新打个招呼吧！', chat_id, msg_id)
        if 'review' in welcome_chat[chat_id] and welcome_chat[chat_id]['username']:
            referer = msg_id or sticker_id
            group_username = welcome_chat[chat_id]['username']
            kuma.send_message(creator,
                              f'Please review new member of @{group_username} '
                              f'by [this link](https://t.me/{group_username}/{referer})',
                              parse_mode='Markdown', disable_web_page_preview=True)
    return not left
