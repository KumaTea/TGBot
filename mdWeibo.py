from urllib import parse
from random import choice
from botSession import kuma
from mdScreen import screenshot_mp
from botTools import mention_other_bot, find_url
from botDB import url_blacklist, loading_image, weibo_domains


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
                url = find_url(text)
        if not weibo_domain:
            return None
    else:
        url = find_url(text)
        if not url:
            return None
        url = url.replace('http://', 'https://')  # noqa
        url_domain = parse.urlparse(url).netloc
        if url_domain not in weibo_domains:
            return None
        # else:
        #     weibo_domain = url_domain
    for keyword in url_blacklist:
        if keyword in url:
            return None
    if mention_other_bot(text, url):
        return None

    # inform = kuma.send_message(chat_id, 'Weibo link found. Retrieving...')
    inform = kuma.send_photo(chat_id, choice(loading_image), caption='Weibo link found. Retrieving...')
    inform_id = inform.message_id

    kuma.send_chat_action(chat_id, 'upload_photo')
    screenshot_mp(chat_id, inform_id, url, '__截图获取失败！__', 'Markdown')
    return True
