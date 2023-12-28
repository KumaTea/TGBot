from pyrogram import Client
from bot.session import config
from common.local import bl_users
from bot.tools import get_blocked_users


me = Client(
    'me',
    api_id=config['kuma']['api_id'],
    api_hash=config['kuma']['api_hash']
)


async def main():
    blocked_users = await get_blocked_users(me)

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


if __name__ == '__main__':
    print('Listing blocked users')
    with me:
        me.run(main())
