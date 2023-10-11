import sys
import random
from bot_info import *
from pyrogram import Client
from pyrogram.types import Message
from tools import get_file, get_user_name
from bot_db import restart_mark, nonsense_replies


async def private_start(client: Client, message: Message):
    return await message.reply(start_message)


async def private_help(client: Client, message: Message):
    help_msg = (f'{help_message}\n'
                f'\n'
                f'Version: {version} ({channel})')
    return await message.reply(help_msg)


async def private_forward(client: Client, message: Message):
    command = message.text
    content_index = command.find(' ')
    user = message.from_user
    if content_index == -1:
        resp = await message.reply('You haven\'t type in your message!')
    else:
        name = get_user_name(user)
        user_id = user.id
        if user.username:
            user_mention = '@' + user.username
        else:
            user_mention = str(user_id)
        forward_msg = f'{name} ({user_mention})\n\n{command[content_index+1:]}'

        await client.send_message(creator, forward_msg)
        resp = await message.reply('Message successfully sent.')
    return resp


def rand_reply():
    return random.choice(nonsense_replies)


async def private_get_file_id(client: Client, message: Message):
    if message.from_user.id == self_id:
        return None
    file_id, file_type = get_file(message)
    if file_type == 'text':
        return await message.reply(rand_reply())
    if file_id:
        return await message.reply(file_id)
    else:
        return await message.reply('Unknown type of media.')


async def private_unknown(client: Client, message: Message):
    return await message.reply(unknown_message)


async def restart(client: Client, message: Message):
    if message.from_user.id in administrators:
        # Do not use subprocess.run since we can't wait for it to finish
        # subprocess.Popen('sleep 2; docker stop tgbot; sleep 2; docker start tgbot', shell=True)
        with open(restart_mark, 'w') as f:
            f.write(str(message.from_user.id))
        await message.reply('Restarting...')
        return sys.exit(0)
    else:
        return None
