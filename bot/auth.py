from typing import Union
from pyrogram import Client
from bot.session import logging
from bot.store import IntListStore, DictStore
from common.local import bl_users, known_group
from pyrogram.types import Message, CallbackQuery
from common.data import poll_groups_file, poll_candidates_file


def ensure_not_bl(func):
    async def wrapper(client: Client, obj: Union[Message, CallbackQuery]):
        if isinstance(obj, CallbackQuery):
            msg = obj.message
        else:
            msg = obj
        if msg.chat and msg.chat.id < 0 and msg.chat.id not in known_group:
            logging.warning(f'Chat id={msg.chat.id} name={msg.chat.title} not known!')
            known_group.append(msg.chat.id)
        if msg.from_user:
            user_id = msg.from_user.id
            if user_id in bl_users:
                logging.warning(f'User {user_id} is in blacklist! Ignoring message.')
                return None
            user_pic = msg.from_user.photo
            if not user_pic:
                logging.warning(f'User {user_id} has no profile picture! Ignoring message.')
                return None
        if msg.reply_to_message and msg.reply_to_message.from_user:
            user_id = msg.reply_to_message.from_user.id
            if user_id in bl_users:
                logging.warning(f'Replied user {user_id} is in blacklist! Ignoring message.')
                return None
        if msg.forward_from:
            user_id = msg.forward_from.id
            if user_id in bl_users:
                logging.warning(f'Forwarded user {user_id} is in blacklist! Ignoring message.')
                return None
        return await func(client, obj)
    return wrapper


enabled_groups = IntListStore(poll_groups_file)
poll_candidates = DictStore(poll_candidates_file)
