import re
import time
import random
import hashlib
from session import kuma
from info import self_id
from tools import mention_other_bot
from pyrogram.enums import ParseMode
from localDb import trusted_group, sticker_bl

try:
    from local_functions import local_message
except ImportError:
    def local_message(m):
        return None
    local_sticker = local_message


special_ids = [
    100, 1000, 10000, 100000, 1000000
]
for i in special_ids.copy():
    for j in range(1, 10):
        special_ids.append(i*j)
special_ids.extend([114514, 1919, 810, 1919810])


def process_id(message):
    chat_id = message.chat.id
    message_id = message.id
    if message_id in special_ids:
        kuma.send_message(chat_id, f'祝贺本群第**{message_id}**条消息达成！ 🎉', parse_mode=ParseMode.MARKDOWN)
        if kuma.get_chat_member(chat_id, self_id).can_pin_messages:
            kuma.pin_chat_message(chat_id, message_id, disable_notification=True)
    return True


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
        process_id(message)
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
