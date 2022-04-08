from random import choice
from botSession import kuma
from botInfo import creator
from botTools import find_url
from botDB import loading_image
from mdNGA import nga_link_process
from mdScreen import screenshot_mp
from mdWeibo import weibo_link_process

try:
    from localDb import trusted_group
except ImportError:
    trusted_group = []


def link_process(message):
    text = message.text
    if not text:
        return None

    nga_link_process(message)
    weibo_link_process(message)
    return True


def look(update, context):
    message = update.message

    chat_id = message.chat_id
    if chat_id not in trusted_group + [creator]:
        return None

    url_in_reply = None
    reply = message.reply_to_message
    if reply:
        text = reply.text
        url_in_reply = find_url(text)

    command = message.text
    content_index = command.find(' ')
    text = command[content_index + 1:]
    url = find_url(text) or url_in_reply
    if not url:
        return kuma.send_message(chat_id, 'No url.')

    inform = kuma.send_photo(chat_id, choice(loading_image), caption='Getting screenshot...')
    inform_id = inform.message_id

    kuma.send_chat_action(chat_id, 'upload_photo')
    screenshot_mp(chat_id, inform_id, url, '__截图获取失败！__', 'Markdown')
    return True
