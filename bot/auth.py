import logging
from typing import Union
from pyrogram import Client
from common.data import bl_users
from bot.tools import get_blocked_user_ids
from pyrogram.types import Message, CallbackQuery


def ensure_not_bl(func):
    async def wrapper(client: Client, obj: Union[Message, CallbackQuery]):
        if obj.from_user:
            user_id = obj.from_user.id
            if user_id in bl_users:
                logging.warning(f'User {user_id} is in blacklist! Ignoring message.')
                return None
        return await func(client, obj)
    return wrapper


if __name__ == '__main__':
    print('Listing blocked users')

    import asyncio
    from bot.session import config

    me = Client(
        'me',
        api_id=config['kuma']['api_id'],
        api_hash=config['kuma']['api_hash']
    )

    async def main():
        async with me:
            blocked_users = await get_blocked_user_ids(me)

        for i in blocked_users:
            print(i.id, '\t', i.first_name)

    asyncio.run(main())
