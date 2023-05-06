import re
import time
import random
import hashlib
from session import kuma
from localDb import trusted_group, sticker_bl
from tools import mention_other_bot

try:
    from local_functions import local_message
except ImportError:
    def local_message(m):
        return None
    local_sticker = local_message


def douban_mark(message):
    title_re = r'《.+》'
    text = message.text or message.caption
    chat_id = message.chat.id
    result = re.findall(title_re, text)
    if result:
        title = result[0][1:-1].strip().lower()
        title_hash = int(hashlib.md5(title.encode("utf-8")).hexdigest(), 16)
        random.seed(title_hash)
        mark = random.randint(10, 100)
        mark_str = str(mark)[:-1] + '.' + str(mark)[-1:]
        text = f'豆瓣评分：{mark_str}'
        return kuma.send_message(chat_id, text)
    return None


def no_banned_package(message):
    chat_id = message.chat.id
    sticker = message.sticker
    # if sticker:
    if sticker.set_name in sticker_bl and sticker.emoji not in sticker_bl[sticker.set_name]['allowed']:
        kuma.send_message(
            chat_id,
            f'发现黑名单表情 {sticker.set_name}，执行删除！'
        )
    else:
        return None
    time.sleep(1)
    try:
        kuma.delete_messages(
            chat_id,
            message.id
            )
    except:
        try:
            kuma.send_message(
                chat_id,
                '没有删除权限，开始刷屏！'
                )
            for i in range(10):
                time.sleep(1)
                kuma.send_message(
                    chat_id,
                    '禁止发送黑名单表情！'
                    )
        except:
            kuma.leave_chat(chat_id)
    return True


def public_message(message):
    return douban_mark(message)


def public_sticker(message):
    return no_banned_package(message)


def process_msg(client, message):
    if message:
        chat_id = message.chat.id
        text = message.text or message.caption
        if text:
            if message.from_user:
                user_id = message.from_user.id
                if user_id > 0:
                    if not mention_other_bot(text):
                        if chat_id in trusted_group:
                            return public_message(message) or local_message(message)
                        else:
                            return public_message(message)
        elif message.sticker:
            return public_sticker(message)
    return None
