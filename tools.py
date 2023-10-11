import os
import re
from typing import Union
from bot_db import url_regex
from bot_info import username
from pyrogram.types import User, Message


def trimmer(data: Union[dict, list]):
    """
    Remove empty items from dict or list.
    """
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


def trim_key(data: dict, char: str = '_'):
    """
    Remove keys that start with char,
    defaults to '_'.
    """
    trim_list = []
    for i in data:
        if i.startswith(char):
            trim_list.append(i)
    for i in trim_list:
        data.pop(i)
    return data


def find_url(text: str):
    if text:
        result = re.findall(url_regex, text)
        if result:
            return result[0]
    return None


def mention_other_bot(text: str):
    text = text.lower()
    if ('@' in text) and ('bot' in text and username.lower() not in text):
        return True
    return False


def get_user_name(user: User):
    lang = user.language_code or 'zh'
    if user.last_name:
        if user.last_name.encode().isalpha() and user.first_name.encode().isalpha():
            space = ' '
        else:
            space = ''
        if 'zh' in lang:
            return f'{user.first_name}{space}{user.last_name}'
        else:
            return f'{user.first_name}{space}{user.last_name}'
    else:
        return user.first_name


def get_file(message: Message):
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


# run this before commit
# for aesthetic purpose
def sort_imports():
    python_files = [i for i in os.listdir() if i.endswith('.py')]
    for file in python_files:
        sort_import(file)


def sort_import(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    imports = []
    for line in lines:
        if line.startswith('import ') or line.startswith('from '):
            imports.append(line)
    imports.sort(key=lambda x: len(x.split('  #')[0]))
    for i in range(len(imports)):
        imports[i] = imports[i].rstrip() + '\n'
    for i in range(len(lines)):
        if lines[i].startswith('import ') or lines[i].startswith('from '):
            lines[i] = imports.pop(0)
    with open(file, 'w', encoding='utf-8') as f:
        f.writelines(lines)


# define an async function
# accepts list of coroutines
# run sequentially
# return once the return value is not None
async def run_async_funcs(funcs: list):
    for func in funcs:
        result = await func
        if result:
            return result
    return None
