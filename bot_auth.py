from pyrogram import Client
from pyrogram.types import Message
from pyrogram.raw.functions.contacts.get_blocked import GetBlocked

try:
    from local_db import trusted_group, bl_users
except ImportError:
    trusted_group = []
    bl_users = []

# me = Client(
#     'me',
#     api_id=config['kuma']['api_id'],
#     api_hash=config['kuma']['api_hash']
# )


async def get_blocked_users(client: Client, offset: int = 0, limit: int = 100):
    result = await client.invoke(GetBlocked(offset=offset, limit=limit))
    return result.users


async def get_blocked_user_ids(client: Client, offset: int = 0, limit: int = 100):
    result = await get_blocked_users(client, offset, limit)
    # for i in result:
    #     yield i.id
    return [i.id for i in result]


def not_bl_command(func):
    async def wrapper(client: Client, message: Message):
        user_id = message.from_user.id
        if user_id in bl_users:
            return None
        else:
            return await func(client, message)
    return wrapper


def not_bl_message(func):
    async def wrapper(message: Message):
        user_id = message.from_user.id
        if user_id in bl_users:
            return None
        else:
            return await func(message)
    return wrapper
