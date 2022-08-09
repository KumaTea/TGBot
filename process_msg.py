import re
from session import kuma
from random import randint
from localDb import trusted_group
from tools import mention_other_bot

try:
    from local_functions import local_process
except ImportError:
    def local_process(m):
        return None


def douban_mark(message):
    title_re = r'《.+》'
    text = message.text
    chat_id = message.chat.id
    result = re.findall(title_re, text)
    if result:
        mark = randint(10, 100)
        mark_str = str(mark)[:-1] + '.' + str(mark)[-1:]
        text = f'豆瓣评分：{mark_str}'
        return kuma.send_message(chat_id, text)
    return None


def public_process(message):
    return douban_mark(message)


def process_msg(client, message):
    if message:
        text = message.text or message.caption
        if text:
            user_id = message.from_user.id
            if user_id > 0:
                if not mention_other_bot(text):
                    chat_id = message.chat.id
                    if chat_id in trusted_group:
                        return public_process(message) or local_process(message)
                    else:
                        return public_process(message)
    return None
