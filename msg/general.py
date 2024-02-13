import asyncio
import logging
from pyrogram import Client
from bot.tools import is_admin
from common.info import creator
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from common.local import trusted_group
from common.data import cue_prob, cue_exact


special_ids = [
    100, 1000, 10000, 100000, 1000000
]
for i in special_ids.copy():
    for j in range(1, 10):
        special_ids.append(i*j)
special_ids.extend([114514, 1919, 810, 1919810])
MENTION_ALL_MSG = ['@all', '@全体成员']


async def process_id(message: Message):
    message_id = message.id
    if message_id in special_ids:
        await message.reply_text(f'祝贺本群第**{message_id}**条消息达成！ 🎉', parse_mode=ParseMode.MARKDOWN, quote=False)
    return True


async def unpin_channel_post(client: Client, message: Message):
    try:
        await asyncio.sleep(2)
        await client.unpin_chat_message(message.chat.id, message.id)
    except Exception as e:
        logging.warning(f'Failed to unpin channel post: {e}')
        logging.warning(f'{message=}')


async def mention_all(client: Client, message: Message):
    text = message.text or message.caption
    if not text:
        return None
    if not any(match in text for match in MENTION_ALL_MSG):
        return False
    if not await is_admin(message.chat.id, message.from_user.id, client):
        return False

    if message.reply_to_message:
        message = message.reply_to_message
    try:
        await message.pin(disable_notification=False)
    except Exception as e:
        logging.warning(f'Failed to pin message: {e}')
        return False


async def cue_remind(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in trusted_group:
        # no need to remind
        return None
    if chat_id > 0:
        # do not remind private chat
        return None

    text = message.text or message.caption
    if not text:
        return None

    exact_match = False
    prob_match = False

    for word in cue_exact:
        if word in text.lower():
            exact_match = True
            break
    # else:
    # use for else is more elegant
    # but here for better readability
    # we use if
    if not exact_match:
        for word in cue_prob:
            if word in text.lower():
                prob_match = True
                break

    if not any([exact_match, prob_match]):
        return None

    if message.chat.username:
        msg_link = f'https://t.me/{message.chat.username}/{message.id}'
    else:
        link_chat_id = str(message.chat.id)[4:]
        msg_link = f'https://t.me/c/{link_chat_id}/{message.id}'

    maybe = '好像' if prob_match else ''
    text = f'{maybe}有人 cue 你被我听见了！\n{msg_link}'
    await client.send_message(creator, text)
