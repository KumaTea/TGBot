import info
import json
import time
from link import look  # noqa
from title import title  # noqa
from session import kuma
from tools import trimmer, trim_key
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
    content_index = command.find(' ')

    if content_index == -1:
        reply = message.reply_to_message
        if reply:
            if reply.text:
                first = reply.from_user.first_name
                last = ' ' + reply.from_user.last_name if reply.from_user.last_name else ''
                repeat_message = first + last + ': \n' + reply.text
                resp = message.reply(repeat_message)
            else:
                if reply.sticker:
                    resp = message.reply_sticker(reply.sticker.file_id)
                elif reply.photo:
                    resp = message.reply_photo(reply.photo.file_id)
                elif reply.animation:
                    resp = message.reply_animation(reply.animation.file_id)
                elif reply.video:
                    resp = message.reply_video(reply.video.file_id)
                elif reply.document:
                    resp = message.reply_document(reply.document.file_id)
                else:
                    resp = None
        else:
            resp = message.reply(command)
    else:
        reply_text = command[content_index+1:]
        resp = message.reply(reply_text)
    return resp


def private_start(client, message):
    return message.reply(info.start_message)


def private_help(client, message):
    help_msg = f'{info.help_message}\n\nI\'m in my {info.version} ({info.channel}) version.'
    return message.reply(help_msg)


def private_forward(client, message):
    command = message.text
    content_index = command.find(' ')
    user = message.from_user
    if content_index == -1:
        resp = message.reply('You haven\'t type in your message!')
    else:
        first = user.first_name
        last = (' ' + user.last_name) if user.last_name else ''
        user_id = user.id
        username = ' (' + (('@' + user.username + ', ') if user.username else '') + str(user_id) + ')'
        forward_msg = first + last + username + '\n\n' + command[content_index+1:]

        kuma.send_message(info.creator, forward_msg)
        resp = message.reply('Message successfully sent.')
    return resp


def private_get_file_id(client, message):
    if message.from_user.id == info.self_id:
        return None
    file_id = 'Unknown type of media.'
    if message.text:
        file_id = message.text
    elif message.sticker:
        file_id = message.sticker.file_id
    elif message.photo:
        file_id = message.photo.file_id
    elif message.animation:
        file_id = message.animation.file_id
    elif message.video:
        file_id = message.video.file_id
    elif message.document:
        file_id = message.document.file_id
    return message.reply(file_id)


def private_unknown(client, message):
    return message.reply('I can\'t understand your message or command. You may try /help.')
