from botSession import kuma
from botInfo import creator
from botTools import find_url
from mdNGA import nga_link_process
from mdScreen import get_screenshot
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
        return None
    else:
        text = command[content_index + 1:]
        url = find_url(text)
        if not url:
            return None
        try:
            screenshot = get_screenshot(url)
            return kuma.send_photo(chat_id, screenshot)
        except Exception as e:
            return kuma.send_message(chat_id, 'Error: {}'.format(e))
