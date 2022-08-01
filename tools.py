import os
import re
import json
import base64
import logging
import sqlite3
from bot_db import url_regex
from info import self_id, username


def read_file(filename, encrypt=False):
    if encrypt:
        with open(filename, 'rb') as f:
            return base64.b64decode(f.read()).decode('utf-8')
    else:
        with open(filename, 'r') as f:
            return f.read()


def write_file(content, filename, encrypt=False):
    if encrypt:
        with open(filename, 'wb') as f:
            f.write(base64.b64encode(content.encode('utf-8')))
        return True
    else:
        with open(filename, 'w') as f:
            f.write(content)
        return True


def query_token(token_id=self_id):
    return read_file(f'token_{token_id}', True)


def trimmer(data):
    if type(data) is dict:
        new_data = {}
        for key in data:
            if data[key]:
                new_data[key] = trimmer(data[key])
        return new_data
    elif type(data) is list:
        new_data = []
        for index in range(len(data)):
            if data[index]:
                new_data.append(trimmer(data[index]))
        return new_data
    else:
        return data


def trim_key(data, char='_'):
    trim_list = []
    for i in data:
        if i.startswith(char):
            trim_list.append(i)
    for i in trim_list:
        data.pop(i)
    return data


def session_update(session, original):
    changed = False
    session_headers = session.headers
    session_cookies = session.cookies.get_dict()
    for item in original['headers']:
        if original['headers'][item] != session_headers[item]:
            original['headers'][item] = session_headers[item]
            changed = True
    for item in original['cookies']:
        if original['cookies'][item] != session_cookies[item]:
            original['cookies'][item] = session_cookies[item]
            changed = True
    if changed:
        write_file(json.dumps(original), 'token_nga', True)
    return True


def init_db(db_dir, table):
    db_path = os.path.join(db_dir, table + '.db')
    if not os.path.isfile(db_path):
        logging.info(f'Creating new database...')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(f'CREATE TABLE \"{table}\" ('
                  '\"pid\" INTEGER, \"tid\" INTEGER, '
                  '\"title\" TEXT, \"date\" TEXT, '
                  '\"author\" TEXT, \"author_id\" INTEGER, '
                  '\"forum\" TEXT, \"forum_id\" INTEGER, '
                  '\"image\" TEXT'
                  ')')
        conn.commit()
        conn.close()
    return True


def find_url(text):
    if text:
        result = re.findall(url_regex, text)
        if result:
            return result[0]
    return None


def mention_other_bot(text):
    text = text.lower()
    if ('@' in text) and ('bot' in text and username.lower() not in text):
        return True
    return False


def get_user_name(user):
    lang = user.language_code or 'zh'
    if user.last_name:
        if 'zh' in lang:
            return f'{user.first_name}{user.last_name}'
        else:
            return f'{user.first_name} {user.last_name}'
    else:
        return user.first_name


def get_file(message):
    file_id = None
    file_type = None
    file_types = [
        'audio', 'document',
        'photo', 'sticker',
        'animation', 'video',
        'voice', 'video_note'
    ]

    if message.text:
        file_id = message.text
        file_type = 'text'
    for i in file_types:
        if getattr(message, i):
            file_id = getattr(message, i).file_id
            file_type = i
            break
    if not any([file_id, file_type]):
        file_id = ''
        file_type = 'unknown'
    return file_id, file_type
