from pyrogram import Client
from typing import Optional
from bot.session import kuma
from common.info import username
from pyrogram.types import User, Message
from pyrogram.raw.types import InputUser
from pyrogram.parser.parser import Parser
from pyrogram.raw.types.users import UserFull
from pyrogram.raw.types import User as RawUser
from pyrogram.enums import ChatMemberStatus, MessageEntityType
from pyrogram.raw.functions.bots.set_bot_info import SetBotInfo
from pyrogram.raw.functions.contacts.get_blocked import GetBlocked
from pyrogram.raw.functions.users.get_full_user import GetFullUser


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
    file_types = {
        'audio', 'document',
        'photo', 'sticker',
        'animation', 'video',
        'voice', 'video_note'
    }

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


async def is_admin(chat_id: int, user_id: int, client: Client = kuma):
    user = await client.get_chat_member(chat_id, user_id)
    if user.privileges:
        return True
    elif user.status == ChatMemberStatus.OWNER:
        return True
    else:
        return False


def code_in_message(message: Message):
    if message.text:
        if message.entities:
            for i in message.entities:
                if i.type == MessageEntityType.CODE:
                    return True
                elif i.type == MessageEntityType.PRE:
                    return True
    return False


async def get_blocked_users(client: Client, offset: int = 0, limit: int = 100) -> list[RawUser]:
    result = await client.invoke(GetBlocked(offset=offset, limit=limit))
    return result.users


async def get_blocked_user_ids(client: Client, offset: int = 0, limit: int = 100) -> list[int]:
    result = await get_blocked_users(client, offset, limit)
    # for i in result:
    #     yield i.id
    return [i.id for i in result]


def set_bot_info(
    client: Client,
    lang_code: str = 'en',
    name: str = None,
    about: str = None,
    description: str = None
):
    with client:
        result = client.invoke(
            SetBotInfo(
                lang_code=lang_code,
                name=name,
                about=about,
                description=description
            )
        )
    return result


def unparse_markdown(message: Message, client: Client = None) -> str:
    p = Parser(client=client)
    result = p.unparse(
        text=message.text,
        entities=message.entities,
        is_html=False
    )
    return result


async def get_chat_member_ids(client: Client, chat_id: int):
    chat_members = client.get_chat_members(chat_id)
    return [i.user.id async for i in chat_members]


def get_input_user_from_user(user: User) -> InputUser:
    if hasattr(user, 'raw'):
        user = user.raw
    return InputUser(
        user_id=user.id,
        access_hash=user.access_hash
    )


async def get_input_user_from_id(client: Client, user_id: int) -> InputUser:
    user = await client.resolve_peer(user_id)
    return InputUser(
        user_id=user.user_id,
        access_hash=user.access_hash
    )


async def get_user_bio(client: Client, user: User) -> Optional[str]:
    result: UserFull = await client.invoke(
        GetFullUser(
            id=get_input_user_from_user(user)
        )
    )
    return result.full_user.about
