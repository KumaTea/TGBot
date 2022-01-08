import re
from urllib import parse
from random import choice
from botSession import kuma
from mdScreen import get_screenshot
from telegram import InputMediaPhoto
from botTools import mention_other_bot
from botDB import url_blacklist, loading_image, url_regex, weibo_domains


def escape_md(text):
    markdown_char = ['*', '_', '`']  # '[', ']',
    for item in markdown_char:
        text = text.replace(item, f'\\{item}')
    return text


def weibo_link_process(message):
    chat_id = message.chat_id
    text = message.text
    if not text:
        return None

    weibo_domain = None
    if 'http' not in text:
        url = ''
        for domain in weibo_domains:
            if domain in text:
                weibo_domain = domain
                text = text.replace(domain, f'https://{domain}')
                url = re.findall(url_regex, text)[0]
        if not weibo_domain:
            return None
    else:
        url = re.findall(url_regex, text)
        if url:
            url = url[0]
        else:
            return None
    url_domain = parse.urlparse(url).netloc
    if url_domain.lower() not in weibo_domains:
        return None
    for keyword in url_blacklist:
        if keyword in url:
            return None
    url = url.replace('http://', 'https://')
    if mention_other_bot(text, url):
        return None

    # inform = kuma.send_message(chat_id, 'Weibo link found. Retrieving...')
    inform = kuma.send_photo(chat_id, choice(loading_image), caption='Weibo link found. Retrieving...')
    inform_id = inform.message_id

    kuma.send_chat_action(chat_id, 'upload_photo')
    screenshot = get_screenshot(url)
    if screenshot:
        # kuma.delete_message(chat_id, inform_id)
        # return kuma.send_photo(chat_id, screenshot)
        kuma.edit_message_media(chat_id, inform_id, media=InputMediaPhoto(screenshot))
    else:
        kuma.edit_message_caption(chat_id, inform_id, caption='__截图获取失败！__', parse_mode='Markdown')
    return True
