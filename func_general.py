import info
import json
import time
from title import title  # noqa
from session import kuma
from bot_db import restart_mark
from tools import trimmer, trim_key, get_file
from pyrogram.enums.parse_mode import ParseMode


def debug(client, message):
    debug_message = json.loads(str(message))
    if message.reply_to_message:
        debug_message = debug_message['reply_to_message']
    debug_message = trim_key(trimmer(debug_message))
    resp = message.reply(f'`{debug_message}`', parse_mode=ParseMode.MARKDOWN)
    return resp


def delay(client, message):
    chat_id = message.chat.id
    first_timestamp = time.perf_counter()

    checking_message = message.reply('Checking delay...')

    second_timestamp = time.perf_counter()
    second_msg_id = checking_message.id
    duration = second_timestamp - first_timestamp
    duration_str = '{:.3f} ms'.format(1000 * duration)
    if duration < 0.1:
        status = 'excellent'
    elif duration < 0.5:
        status = 'good'
    elif duration < 1:
        status = 'ok'
    else:
        status = 'bad'
    result = kuma.edit_message_text(chat_id, second_msg_id, f'Delay is {duration_str}.\nThe connectivity is {status}.')
    return result


def repeat(client, message):
    command = message.text
    chat_id = message.chat.id
    content_index = command.find(' ')

    reply = message.reply_to_message
    if content_index == -1:
        if reply:
            if reply.text:
                first = reply.from_user.first_name
                last = ' ' + reply.from_user.last_name if reply.from_user.last_name else ''
                repeat_message = first + last + ': \n' + reply.text
                resp = message.reply(repeat_message, quote=False)
            else:
                file_id, file_type = get_file(reply)
                if file_id:
                    resp = exec(f'message.reply_{file_type}(file_id, quote=False)')
                else:
                    resp = None
        else:
            resp = message.reply(command, quote=False)
    else:
        reply_text = command[content_index+1:]
        if reply:
            resp = kuma.send_message(chat_id, reply_text, reply_to_message_id=reply.id)
        else:
            resp = message.reply(reply_text, quote=False)
    return resp


def restart(client, message):
    if message.from_user.id in info.administrators:
        # Do not use subprocess.run since we can't wait for it to finish
        # subprocess.Popen('sleep 2; docker stop tgbot; sleep 2; docker start tgbot', shell=True)
        with open(restart_mark, 'w') as f:
            f.write(str(message.from_user.id))
        message.reply('Restarting...')
        return exit(0)
    else:
        return None  # 无事发生
