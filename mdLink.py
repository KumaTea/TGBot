from random import choice
from botSession import kuma
from botInfo import creator
from botTools import find_url
from botDB import loading_image
from mdNGA import nga_link_process
from mdScreen import get_screenshot
from telegram import InputMediaPhoto
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

    command = message.text
    content_index = command.find(' ')
    if content_index == -1:
        return kuma.send_message(chat_id, 'No content.')
    else:
        text = command[content_index + 1:]
        url = find_url(text)
        if not url:
            return kuma.send_message(chat_id, 'No url.')

        inform = kuma.send_photo(chat_id, choice(loading_image), caption='Getting screenshot...')
        inform_id = inform.message_id
        try:
            kuma.send_chat_action(chat_id, 'upload_photo')
            screenshot = get_screenshot(url)
            kuma.edit_message_media(chat_id, inform_id, media=InputMediaPhoto(screenshot))
            # kuma.edit_message_caption(chat_id, inform_id, caption='')
            return True
        except Exception as e:
            return kuma.edit_message_caption(chat_id, inform_id, 'Error: {}'.format(e))
