import os
import re
import json
import base64
import logging
import sqlite3
from botDB import db_dir, url_regex
from botInfo import self_id, username


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


def mention_other_bot(text, url):
    text = text.lower()
    if ('@' in text and '@' not in url) and ('bot' in text and username.lower() not in text):
        return True
    return False


def mkdir(folder=None):
    if folder:
        if type(folder) == list or type(folder) == tuple:
            for items in folder:
                if not os.path.exists(str(items)):
                    os.mkdir(str(items))
        else:
            if not os.path.exists(str(folder)):
                os.mkdir(str(folder))
    return True


def init_db(table):
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
