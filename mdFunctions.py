import botInfo
from mdTitle import title  # noqa: yes it is used by register
from botSession import kuma
from datetime import datetime
from botTools import trimmer, trim_key


def debug(update, context):
    debug_message = update.to_dict()
    if update.message.reply_to_message:
        debug_message = debug_message['message']['reply_to_message']
    debug_message = trim_key(trimmer(debug_message))
    resp = update.message.reply_text(f'`{debug_message}`', parse_mode='Markdown', quote=False)
    return resp


def delay(update, context):
    chat_id = update.message.chat_id
    first_timestamp = datetime.timestamp(datetime.now())

    checking_message = update.message.reply_text('Checking delay...')

    second_timestamp = datetime.timestamp(datetime.now())
    second_msg_id = checking_message.message_id
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
    result = kuma.edit_message_text(f'Delay is {duration_str}.\nThe connectivity is {status}.', chat_id, second_msg_id)
    return result


def repeat(update, context):
    command = update.message.text
    content_index = command.find(' ')

    if content_index == -1:
        reply = update.message.reply_to_message
        if reply:
            if reply.text:
                first = reply.from_user.first_name
                last = ' ' + reply.from_user.last_name if reply.from_user.last_name else ''
                repeat_message = first + last + ': \n' + reply.text
                resp = update.message.reply_text(repeat_message)
            else:
                if reply.sticker:
                    resp = update.message.reply_sticker(reply.sticker.file_id)
                elif reply.photo:
                    resp = update.message.reply_photo(reply.photo[-1].file_id)
                elif reply.animation:
                    resp = update.message.reply_animation(reply.animation.file_id)
                elif reply.video:
                    resp = update.message.reply_video(reply.video.file_id)
                elif reply.document:
                    resp = update.message.reply_document(reply.document.file_id)
                else:
                    resp = None
        else:
            resp = update.message.reply_text(command)
    else:
        reply_text = command[content_index+1:]
        resp = update.message.reply_text(reply_text)
    return resp


def private_start(update, context):
    return update.message.reply_text(botInfo.start_message)


def private_help(update, context):
    message = f'{botInfo.help_message}\n\nI\'m in my {botInfo.version} ({botInfo.channel}) version.'
    return update.message.reply_text(message)


def private_forward(update, context):
    command = update.message.text
    content_index = command.find(' ')
    user = update.message.from_user
    if content_index == -1:
        resp = update.message.reply_text('You haven\'t type in your message!')
    else:
        first = user.first_name
        last = (' ' + user.last_name) if user.last_name else ''
        user_id = user.id
        username = ' (' + (('@' + user.username + ', ') if user.username else '') + str(user_id) + ')'
        forward_msg = first + last + username + '\n\n' + command[content_index+1:]
        
        kuma.send_message(botInfo.creator, forward_msg)
        resp = update.message.reply_text('Message successfully sent.')
    return resp


def private_get_file_id(update, context):
    file_id = 'Unknown type of media.'
    if update.message.text:
        file_id = update.message.text
    elif update.message.sticker:
        file_id = update.message.sticker.file_id
    elif update.message.photo:
        file_id = update.message.photo[-1].file_id
    elif update.message.animation:
        file_id = update.message.animation.file_id
    elif update.message.video:
        file_id = update.message.video.file_id
    elif update.message.document:
        file_id = update.message.document.file_id
    return update.message.reply_text(file_id)


def private_unknown(update, context):
    return update.message.reply_text('I can\'t understand your message or command. You may try /help.')
