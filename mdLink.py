from mdNGA import nga_link_process
from mdWeibo import weibo_link_process


def link_process(message):
    text = message.text
    if not text:
        return None

    nga_link_process(message)
    weibo_link_process(message)
    return True
