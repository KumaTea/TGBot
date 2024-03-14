import logging
from common.tools import get_url_int_list  # , get_url_str_list


LOCAL_URL = 'https://hm.lan.kmtea.eu'


class UserStore:
    def __init__(self, data: list[int] = None):
        self.data: list[int] = data or []

    def __contains__(self, item: int) -> bool:
        return item in self.data

    def __len__(self) -> int:
        return len(self.data)

    def reload(self, data: list[int]):
        self.data = data


logging.warning('Loading local data...')

trusted_group = get_url_int_list(f'{LOCAL_URL}/trusted-group.txt')
logging.warning(f'Trusted groups: {len(trusted_group)}')
known_group = trusted_group.copy()
known_group.extend(get_url_int_list(f'{LOCAL_URL}/known-group.txt'))
logging.warning(f'Known groups: {len(known_group)}')

a55h01e = get_url_int_list('https://s.kmtea.eu/bot/a55.txt')
# lol the unmodified name makes Copilot refuse to work
soft_block = get_url_int_list(f'{LOCAL_URL}/bl-users.txt')
class_enemies = get_url_int_list(f'{LOCAL_URL}/jjdr.txt')  # 阶级敌人

# blacklist_words = get_url_str_list(f'{LOCAL_URL}/blacklist-words.txt')

known_user_ids = get_url_int_list(f'{LOCAL_URL}/known-user-ids.txt')
logging.warning(f'Known users: {len(known_user_ids)}')

bl_users = UserStore(list(set(a55h01e + soft_block + class_enemies)))
logging.warning(f'Blacklisted users: {len(bl_users)}')
