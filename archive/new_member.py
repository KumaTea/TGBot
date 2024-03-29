import time
import logging
from session import kuma
from info import creator
from localDb import welcome_chat
from multiprocessing import Process
from pyrogram.enums.parse_mode import ParseMode


def welcome(client: Client, message: Message):
    chat_id = message.chat.id
    alert_id = message.id
    new_member = message.new_chat_members[0]
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
                welcome_message = message.reply(formatted_message, parse_mode=ParseMode.MARKDOWN)
            else:
                welcome_message = message.reply(welcome_chat[chat_id]['message'])
            msg_id = welcome_message.id
        else:
            msg_id = None
        if 'sticker' in welcome_chat[chat_id]:
            welcome_sticker = message.reply_sticker(welcome_chat[chat_id]['sticker'])
            sticker_id = welcome_sticker.id
        else:
            sticker_id = None
        check = Process(target=check_member, args=(chat_id, user_id, alert_id, msg_id, sticker_id, 125))
        check.start()  # noqa
    else:
        resp = None
    return resp


def check_member(chat_id, user_id, alert_id, msg_id=None, sticker_id=None, wait_time=125):
    time.sleep(wait_time)
    logging.info(f'Starting new member checking...')
    left = False
    user = kuma.get_chat_member(chat_id, user_id)
    user_status = user.status
    if 'left' in user_status or 'kick' in user_status:
        left = True

    if left:
        kuma.delete_messages(chat_id, alert_id)
        if sticker_id:
            kuma.delete_messages(chat_id, sticker_id)
        if msg_id:
            kuma.edit_message_text('验证机器人已移除一位未通过验证的用户。', chat_id, msg_id)
        logging.info(f'User {user_id} status: LEFT; NOT member.')
    else:
        logging.info(f'User {user_id} status: IN; IS member.')
        if msg_id:
            kuma.edit_message_text('你已经是群大佬了，快来跟萌新打个招呼吧！', chat_id, msg_id)
        if 'review' in welcome_chat[chat_id] and welcome_chat[chat_id]['username']:
            referer = msg_id or sticker_id
            group_username = welcome_chat[chat_id]['username']
            kuma.send_message(creator,
                              f'Please review new member of @{group_username} '
                              f'by [this link](https://t.me/{group_username}/{referer})',
                              parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    return not left
