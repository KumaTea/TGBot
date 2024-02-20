from tqdm import tqdm
from pyrogram import Client
from bot.session import config
from common.local import bl_users
from bot.tools import get_blocked_users
from pyrogram.raw.types import User as RawUser


me = Client(
    'me',
    api_id=config['kuma']['api_id'],
    api_hash=config['kuma']['api_hash']
)

MY_PROJECTS = [
    -1001454145827,  # MetaKuma
    -1001525690242,  # Space
    -1001476670457,  # Cloud
    -1002051677176,  # FQ
    -1001713500645,  # Logs
    -1001581552395,  # zhfnl
]

MY_GROUPS = [
    -1001688959697,  # z?fdq
    -1001214803045,  # Bot Test
    -1001836884943,  # 4th
    -1001853371415,  # 5th
    -1001932978232,  # teasps
    -1001883734921,  # 2y
    -1001923350797,  # 3y
]


def get_new_block(blocked_users: list[RawUser]):
    for i in blocked_users:
        print(i.id, '\t', i.first_name)

    blocked_user_ids = [i.id for i in blocked_users]
    new = set(blocked_user_ids) - set(bl_users)
    if new:
        print('New blocked users:')
        for i in new:
            print(i)
    else:
        print('No new blocked users')


async def apply_block(blocked_users: list[RawUser]):
    chat_ids = MY_PROJECTS + MY_GROUPS
    pbar = tqdm(chat_ids)
    for chat_id in pbar:
        for user in blocked_users:
            await me.ban_chat_member(chat_id, user.id)
            pbar.set_description(f'Block: {chat_id}\t{user.id}')


async def main():
    blocked_users: list[RawUser] = await get_blocked_users(me)
    blocked_users = [u for u in blocked_users if not u.bot]
    get_new_block(blocked_users)
    await apply_block(blocked_users)


if __name__ == '__main__':
    print('Listing blocked users')
    with me:
        me.run(main())
