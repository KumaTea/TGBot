import info
from session import kuma
from tools import get_file


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
    file_id, file_type = get_file(message)
    if file_id:
        return message.reply(file_id)
    else:
        return message.reply('Unknown type of media.')


def private_unknown(client, message):
    return message.reply("I can't understand your message or command. You may try /help.")
