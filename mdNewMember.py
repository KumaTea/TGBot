from botSession import bot
from localDb import welcome_msg
from threading import Timer


def welcome(chat_id, user_id, system_new_mem_msg_id):
    if chat_id in welcome_msg:
        resp = 'Familiar'
        if 'message' in welcome_msg[chat_id]:
            message = bot.send(chat_id).message(welcome_msg[chat_id]['message'])
            msg_id = bot.get(message).message('id')
        else:
            msg_id = None
        if 'sticker' in welcome_msg[chat_id]:
            sticker = bot.send(chat_id).sticker(welcome_msg[chat_id]['sticker'])
            sticker_id = bot.get(sticker).message('id')
        else:
            sticker_id = None
        check = Timer(300, check_member, [chat_id, user_id, system_new_mem_msg_id, msg_id, sticker_id])
        # Ignore PyCharm Error
        check.start()
    else:
        resp = 'Not familiar using default'
    return resp


def check_member(chat_id, user_id, system_new_mem_msg_id, msg_id=None, sticker_id=None):
    print(f'[INFO] Starting new member checking...')
    left = False
    try:
        user = bot.query(chat_id).chat_member(user_id, raw=True)
        if user['status'] == 'left':
            left = True
    except KeyError:
        left = True

    if left:
        bot.delete(chat_id).message(system_new_mem_msg_id)
        if sticker_id:
            bot.delete(chat_id).message(sticker_id)
        if msg_id:
            bot.edit(chat_id, msg_id).message('验证机器人已移除一位未通过验证的用户。')
        print(f'[INFO] User {user_id} status: LEFT; NOT member.')
    else:
        print(f'[INFO] User {user_id} status: IN; IS member.')
    return True
