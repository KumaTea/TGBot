import os
import re
from typing import Union
from common.data import url_regex, pwd


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


# run this before commit
# for aesthetic purpose
def sort_imports():
    # python_files = [i for i in os.listdir() if i.endswith('.py')]
    for root, dirs, files in os.walk(pwd):
        for file in files:
            if file.endswith('.py'):
                sort_import(os.path.join(root, file))


def sort_import(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    original_lines = lines.copy()
    imports = []
    for line in lines:
        if line.startswith('import ') or line.startswith('from '):
            imports.append(line)
        else:
            break
    if not imports:
        return None
    imports.sort(key=lambda x: len(x.split('  #')[0]))
    for i in range(len(imports)):
        imports[i] = imports[i].rstrip() + '\n'
    for i in range(len(lines)):
        if lines[i].startswith('import ') or lines[i].startswith('from '):
            lines[i] = imports.pop(0)
        if not imports:
            break
    if lines != original_lines:
        with open(file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f'{file} sorted')


if __name__ == '__main__':
    sort_imports()
