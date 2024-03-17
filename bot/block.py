from tqdm import tqdm
from pyrogram import Client
from bot.session import config
from pyrogram.types import User
from share.local import bl_users
from bot.tools import get_blocked_users
from pyrogram.raw.types import User as RawUser
from pyrogram.enums.user_status import UserStatus
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid


me = Client(
    'me',
    api_id=config['kuma']['api_id'],
    api_hash=config['kuma']['api_hash']
)

PROJECTS = {
    -1001454145827,  # MetaKuma
    -1001525690242,  # Space
    -1001476670457,  # Cloud
    -1002051677176,  # FQ
    -1001713500645,  # Logs
    -1001581552395,  # zhfnl
}

GROUPS = {
    -1001688959697,  # z?fdq
    -1001214803045,  # Bot Test
    -1001836884943,  # 4th
    -1001853371415,  # 5th
    -1001932978232,  # teasps
    -1001883734921,  # 2y
    -1001923350797,  # 3y
}


def get_new_block(blocked_users: list[RawUser]):
    for i in blocked_users:
        print(i.id, '\t', i.first_name)
    print('\n')

    blocked_user_ids = [i.id for i in blocked_users]
    new_id = set(blocked_user_ids) - bl_users.data
    if new_id:
        print('New blocked users:')
        for i in new_id:
            print(i)
    else:
        print('No new blocked users')

    new = [u for u in blocked_users if u.id in new_id]
    return new


def get_more() -> list[int]:
    more = []
    print('Input more ids, ENTER to exit:\n')
    while True:
        try:
            more.append(int(input()))
        except ValueError:
            break
    return more


def is_blocked(user: User) -> bool:
    if user.status == UserStatus.LONG_AGO and not user.is_deleted:
        return True
    return False


async def check_blocked(user_ids: list[int]) -> list[User]:
    new_blocked = []
    pbar = tqdm(user_ids)
    for user_id in pbar:
        try:
            user = await me.get_users(user_id)
            if is_blocked(user):
                print(f'{user_id} blocked me!')
                new_blocked.append(user)
        except PeerIdInvalid:
            print(f'{user_id} not meet before')
    return new_blocked


async def apply_block(blocked_users: list[RawUser]):
    chat_ids = PROJECTS | GROUPS
    blocked_user_ids = [i.id for i in blocked_users]
    more = get_more()
    pbar = tqdm(chat_ids)
    for chat_id in pbar:
        for user in blocked_user_ids + more:
            await me.ban_chat_member(chat_id, user)
            pbar.set_description(f'Block: {chat_id}\t{user}')


async def main():
    print(
        'If you find something new to block, '
        'remember to add it to the txt file later, '
        'BUT NOT NOW!'
    )
    blocked_users = await get_blocked_users(me)
    blocked_users = [u for u in blocked_users if not u.bot]
    new_block = get_new_block(blocked_users)
    new_blocked_by = await check_blocked(list(bl_users.data - set([u.id for u in blocked_users])))
    await apply_block(new_block + new_blocked_by)


if __name__ == '__main__':
    # print('Listing blocked users')
    # with me:
    #     me.run(main())
    print("You can't.")
