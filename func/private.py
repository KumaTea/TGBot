import sys
import random
import logging
from pyrogram import Client
from pyrogram.types import Message
from share.auth import ensure_auth
from share.common import no_preview
from bot.tools import get_file, get_user_name
from common.info import channel, creator, version
from common.data import restart_mark, nonsense_replies
from func.debugs import command_get_users, command_get_groups  # noqa
from share.local import a55h01e, bl_users, soft_block, class_enemies
from common.data import pwd, greet_message, administrators, unknown_message


@ensure_auth
async def private_start(client: Client, message: Message):
    # from func.tools import get_content
    if message.command and len(message.command) > 1:
        data = message.command[1]
        if data and data.split('_')[0] == 'r':
            user = message.from_user
            class_enemies.append(user.id)
            bl_users.reload(list(set(a55h01e + soft_block + class_enemies)))
            logging.warning(f'User {user.id} added to class enemies.')
            text = (
                '依据条款，本 bot 现在开始永久拒绝对你服务。'
                '其他 Kuma 系 bot 也会在最快1天内同步黑名单。'
            )

            if data == 'r_q':
                with open(f'{pwd}/jjdr.tmp.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{user.id}  # q: {user.first_name}\n')
                return await message.reply(f'你已登记自己为 qljj。{text}')
            elif data == 'r_f':
                with open(f'{pwd}/jjdr.tmp.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{user.id}  # f: {user.first_name}\n')
                return await message.reply(f'你已登记自己为 g/f2d。{text}')
    return await message.reply(greet_message, **no_preview)


@ensure_auth
async def private_help(client: Client, message: Message):
    help_msg = (f'{greet_message}\n'
                f'\n'
                f'Version: {version} ({channel})')
    return await message.reply(help_msg)


@ensure_auth
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


@ensure_auth
async def private_get_file_id(client: Client, message: Message):
    file_id, file_type = get_file(message)
    if file_type == 'text':
        return await message.reply(message.text)
    if file_id:
        return await message.reply(file_id)
    else:
        return await message.reply('Unknown type of media.')


@ensure_auth
async def private_unknown(client: Client, message: Message):
    if message.text:
        if message.text.startswith('/'):
            return await message.reply(unknown_message)
        else:
            return await message.reply(rand_reply())


# @ensure_auth
# already checked
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
