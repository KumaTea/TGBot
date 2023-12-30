import asyncio
from typing import Optional
from pyrogram import Client
from datetime import datetime
from common.info import creator
from bot.session import logging
from pyrogram.types import Message
from bot.auth import ensure_not_bl
from common.local import LOCAL_URL
from bot.tools import get_user_name
from common.tools import get_url_str
from common.data import pwd, administrators
from bot.store import IntListStore, DictStore


known_user_ids = IntListStore(f'{pwd}/data/ku.p')
red_bag_users = DictStore(f'{pwd}/data/rb.p')

RED_BAG_IMG_ID = get_url_str(f'{LOCAL_URL}/rbi.txt')
logging.warning(f'RB_IMG_ID: {RED_BAG_IMG_ID}')
RED_BAG_MSG = get_url_str(f'{LOCAL_URL}/rbm.txt')
logging.warning(f'RB_MSG: {RED_BAG_MSG}')


async def get_chat_member_ids(client: Client, chat_id: int):
    chat_members = client.get_chat_members(chat_id)
    return [i.user.id async for i in chat_members]


async def command_get_known(client: Client, message: Message) -> Optional[Message]:
    if message.from_user.id not in administrators:
        return None
    if known_user_ids.data:
        return await message.reply_text('Already known.')
    else:
        chat_id = -1001932978232  # Dic
        known_user_ids.data = await get_chat_member_ids(client, chat_id)
        known_user_ids.write_data()
        return await message.reply_text('Data: ' + str(known_user_ids.data))


@ensure_not_bl
async def command_red_bag(client: Client, message: Message) -> Optional[Message]:
    if not known_user_ids.data:
        chat_id = -1001932978232  # Dic
        known_user_ids.data = await get_chat_member_ids(client, chat_id)

    user = message.from_user
    name = get_user_name(user)
    user_id = message.from_user.id
    if user.username:
        user_mention = '@' + user.username
    else:
        user_mention = str(user_id)

    if user_id not in known_user_ids.data:
        unknown, inform = await asyncio.gather(
            message.reply_text('未知错误'),
            client.send_message(
                creator,
                '未知用户请求：\n' + f'{name} ({user_mention})'
            )
        )
        return unknown

    if user_id in red_bag_users.data:
        return await message.reply_text('你已经领过了！')

    order = len(red_bag_users.data) + 1
    info = {
        'order': order,
        'user_id': user_id,
        'time': datetime.now()
    }
    red_bag_users.add_item(user_id, info)

    if order < 10:
        reply = '你是第{}个领取红包的人！'.format(order)
    else:
        reply = '你是第{}个领取红包的人，可能已经被领光了哦'.format(order)

    result, rep, inform = await asyncio.gather(
        message.reply_photo(RED_BAG_IMG_ID, caption=RED_BAG_MSG),
        message.reply_text(reply),
        client.send_message(
            creator,
            '第{}个红包领取者：\n'.format(order) + f'{name} ({user_mention})'
        )
    )
    return result
