import time
import logging
import sqlite3
import requests
import subprocess
from bot_db import *
from io import BytesIO
from urllib import parse
from session import kuma
from random import choice
from idle import set_busy
from session_rq import nga
from session_ff import get_driver
from pyrogram.errors import Timeout
from multiprocessing import Process
from screenshot import get_screenshot
from pyrogram.types import InputMediaPhoto
from tools import mention_other_bot, find_url
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.enums.chat_action import ChatAction
from datetime import datetime, timezone, timedelta


def escape_md(text):
    markdown_char = ['*', '_', '`']  # '[', ']',
    for item in markdown_char:
        text = text.replace(item, f'\\{item}')
    return text


def get_post_info(pid=None, tid=None):
    assert pid or tid
    table = 'NGA'
    db_path = os.path.join(db_dir, table + '.db')

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    if pid:
        c.execute(f'SELECT * FROM {table} WHERE pid = ?', (pid,))
    else:
        c.execute(f'SELECT * FROM {table} WHERE tid = ?', (tid,))
    result = c.fetchone()
    conn.close()

    return result


def write_post_info(pid, tid, title, date, author, author_id, forum, forum_id, image):
    table = 'NGA'
    db_path = os.path.join(db_dir, table + '.db')

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute(f'INSERT INTO {table} VALUES (?,?,?,?,?,?,?,?,?)',
              (pid, tid, title, date, author, author_id, forum, forum_id, image))
    conn.commit()
    conn.close()

    return logging.info(f'Writing post: {pid or tid}')


@set_busy
def update_nga(chat_id, inform_id, url, post_info, link_result, error_msg='Error!', parse_mode=ParseMode.MARKDOWN):
    post_id, thread_id, title, date, author, author_id, forum, forum_id = post_info
    screenshot, status = get_screenshot(url, chat_id, inform_id)
    if status:
        try:
            kuma.edit_message_caption(
                chat_id, inform_id, caption="Uploading image...")
            # edited = kuma.edit_message_media(chat_id, inform_id, media=InputMediaPhoto(screenshot))
            # image = edited.photo[0].file_id
            # kuma.edit_message_caption(chat_id, inform_id, caption=link_result, parse_mode=ParseMode.MARKDOWN)
            edited = requests.post(
                'http://192.168.2.225:10561/api',
                data={
                    'chat_id': chat_id,
                    'message_id': inform_id,
                    'error_msg': error_msg,
                    'parse_mode': parse_mode,
                    'caption': link_result
                },
                files={
                    'photo': screenshot
                }
            )
            # image = edited.text
            # write_post_info(post_id, thread_id, title, date, author, author_id, forum, forum_id, image)
            # return kuma.edit_message_caption(
            #     chat_id, inform_id, caption=link_result, parse_mode=parse_mode)
            return True
        except Timeout:
            logging.warning(f'Telegram reported a timeout: {post_id or thread_id}')
            return None
    return kuma.edit_message_caption(
        chat_id, inform_id, caption=f'{link_result}\n{error_msg}', parse_mode=parse_mode)


def nga_mp(chat_id, inform_id, url, post_info, link_result, error_msg='Error!', parse_mode=ParseMode.MARKDOWN):
    p = Process(target=update_nga, args=(chat_id, inform_id, url, post_info, link_result, error_msg, parse_mode))
    p.start()
    return True


def nga_link_process(message):
    chat_id = message.chat.id
    text = message.text
    if not text:
        return None

    # Find url in message
    nga_domain = None
    if 'http' not in text:
        url = ''
        for domain in nga_domains:
            if domain in text:
                nga_domain = domain
                text = text.replace(domain, f'https://{domain}')
                url = find_url(text)
        if not nga_domain:
            return None
    else:
        url = find_url(text)
        if not url:
            return None
        url = url.replace('http://', 'https://')  # noqa
        url_domain = parse.urlparse(url).netloc
        if url_domain not in nga_domains:
            return None
        else:
            nga_domain = url_domain
    for keyword in url_blacklist:
        if keyword in url:
            return None
    if mention_other_bot(text, url):
        return None

    # Get post id
    if '?' not in url:
        return False  # only domain, no post or thread id
    # if '&' in url:
    params = parse.parse_qs(parse.urlparse(url).query)
    post_id = 0
    thread_id = 0
    url_for_info = url
    if 'pid' in params:
        post_id = params['pid'][0]  # noqa
        url_for_info = f'https://bbs.nga.cn/read.php?pid={post_id}'
    elif 'tid' in params:
        thread_id = params['tid'][0]  # noqa
        url_for_info = f'https://bbs.nga.cn/read.php?tid={thread_id}'
    if not post_id and not thread_id:
        return None

    # Prepare for links
    url_for_screenshot = url_for_info
    url_for_info += '&__output=11'

    # inform = kuma.send_message(chat_id, 'NGA link found. Retrieving...')
    # logging.warn(f'[NGA] info: {chat_id}')
    db_result = get_post_info(pid=post_id, tid=thread_id)
    if db_result:
        pid, tid, title, date, author, author_id, forum, forum_id, image = db_result
        link_result = f'**{title}**\n' \
                      f'[{author}](https://{nga_domain}/nuke.php?func=ucp&uid={author_id}) ' \
                      f'{date} ' \
                      f'[{forum}](https://{nga_domain}/thread.php?fid={forum_id})'
        return kuma.send_photo(chat_id, image, caption=link_result, parse_mode=ParseMode.MARKDOWN)

    inform = kuma.send_photo(chat_id, choice(loading_image), caption='NGA link found. Retrieving...')
    inform_id = inform.id

    result = nga.get(url_for_info)
    if result.status_code != 200:
        return kuma.edit_message_caption(chat_id, inform_id, caption=f'错误：服务器返回{result.status_code}')
    else:
        try:
            _ = result.json()
        except Exception as e:
            logging.error(f'Json error!\n{str(e)}\n\n')
            return kuma.edit_message_caption(chat_id, inform_id, caption='NGA API Json 解析错误')

        if 'error' in result.json():
            return kuma.edit_message_caption(chat_id, inform_id, caption=('错误' + result.json()['error'][0]))

        result_data = result.json()['data']
        title = escape_md(result_data['__T']['subject'])
        author = result_data['__T']['author']
        author_id = result_data['__T']['authorid']
        date = datetime.fromtimestamp(
            result_data['__T']['postdate'], tz=timezone(timedelta(hours=8))).strftime('%m-%d %H:%M')
        forum = result_data['__F']['name']
        forum_id = result_data['__T']['fid']

        link_result = f'**{title}**\n' \
                      f'[{author}](https://{nga_domain}/nuke.php?func=ucp&uid={author_id}) ' \
                      f'{date} ' \
                      f'[{forum}](https://{nga_domain}/thread.php?fid={forum_id})'
        if title in text:
            kuma.edit_message_caption(chat_id, inform_id, caption='哦，已经有标题了啊，那没事了……')
            time.sleep(5)
            return kuma.delete_message(chat_id, inform_id)
        else:
            kuma.send_chat_action(chat_id, ChatAction.UPLOAD_PHOTO)
            post_info = [post_id, thread_id, title, date, author, author_id, forum, forum_id]
            nga_mp(chat_id, inform_id, url_for_screenshot, post_info, link_result, '__截图获取失败！__', ParseMode.MARKDOWN)
            return True


@set_busy
def check_nga_login():
    login_success_text = 'KumaTea'
    driver = get_driver()
    driver.get(f'https://{nga_domains[1]}/')  # 'bbs.nga.cn'
    if login_success_text in driver.page_source:
        result = True
    else:
        result = False
        subprocess.run([notify_path, '[kuma] NGA login failed'])
    driver.quit()
    return result
