from session import kuma
from pyrogram import Client
from bot_info import username
from pyrogram.types import User, Message
from pyrogram.enums import ChatMemberStatus


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


async def is_admin(chat_id: int, user_id: int, client: Client = kuma):
    user = await client.get_chat_member(chat_id, user_id)
    if user.privileges:
        return True
    elif user.status == ChatMemberStatus.OWNER:
        return True
    else:
        return False
