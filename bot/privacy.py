from typing import List
from pyrogram import Client
from bot.session import config
from pyrogram.types import User
from pyrogram.raw.types.user import User as RawUser
from pyrogram.raw.functions.contacts import GetBlocked
from pyrogram.raw.functions.account import GetPrivacy, SetPrivacy
from pyrogram.raw.types import InputPrivacyKeyProfilePhoto, InputUser
from pyrogram.raw.types import InputPrivacyValueAllowAll, InputPrivacyValueDisallowUsers


me = Client(
    'me',
    api_id=config['kuma']['api_id'],
    api_hash=config['kuma']['api_hash']
)


async def get_current_restricted(client: Client) -> List[RawUser]:
    result = await client.invoke(GetPrivacy(key=InputPrivacyKeyProfilePhoto()))
    return result.users


async def check_group(client: Client, chat_id: int) -> List[User]:
    no_profile = []
    async for member in client.get_chat_members(chat_id):
        user = member.user
        has_pic = user.photo
        is_bot = user.is_bot
        if not has_pic and not is_bot:
            no_profile.append(user)
    return no_profile


def get_input_user(user: RawUser) -> InputUser:
    return InputUser(
        user_id=user.id,
        access_hash=user.access_hash
    )


async def get_blocked(client: Client) -> List[User]:
    result = await me.invoke(GetBlocked(offset=0, limit=0))
    for u in result.users:
        if not hasattr(u, 'access_hash') or not u.access_hash:
            print(f'User {u.id=} has no access_hash')
    return result.users


async def update_restrictions(client: Client, users: List[User]):
    key = InputPrivacyKeyProfilePhoto()
    rules = [
        InputPrivacyValueDisallowUsers(
            users=list(map(get_input_user, users))
        ),
        InputPrivacyValueAllowAll()
    ]
    await client.invoke(SetPrivacy(key=key, rules=rules))


async def handler(client: Client, chat_id: int):
    print('Getting current restrictions')
    current_restricted = await get_current_restricted(client)
    print('Getting group members')
    no_profile = await check_group(client, chat_id)
    print('Getting blocked users')
    blocked = await get_blocked(client)
    blocked_ids = [u.id for u in blocked]

    print('Now block all users without profile photo')
    for u in no_profile:
        await client.block_user(u.id)
    print('Updating new blocked')
    new_blocked = await get_blocked(client)
    diff = [u for u in new_blocked if u.id not in blocked_ids]
    all_restricted = current_restricted + diff
    print('Updating restrictions')
    await update_restrictions(client, all_restricted)
    print('Unblocking users')
    for u in diff:
        await client.unblock_user(u.id)
    print('Done')


async def main(client: Client):
    print('Start')
    while chat_id := input('Chat ID: '):
        chat_id = int(chat_id)
        await handler(client, chat_id)


if __name__ == '__main__':
    async with me:
        me.run(main(me))
