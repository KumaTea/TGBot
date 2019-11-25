from Tools import md_debug, delay
from threading import Timer
from botInfo import self_id
from starting import get_admin_id
from botSession import bot


def group_cmd(data):
    bot_getter = bot.get(data)
    chat_id = bot_getter.chat('id')
    command = bot_getter.message('text')[1:]
    msg_id = bot_getter.message('id')

    if command.startswith(('rp', 'repeat')):
        cont = command.find(' ')
        rp_text = command[cont:]
        if cont == -1:
            reply_id = bot_getter.reply('id')
            if reply_id == 0:
                resp = bot.send(chat_id).message(f'/{command}', msg_id)
            else:
                reply_type = bot_getter.reply('type')
                if reply_type == 'text':
                    first = bot_getter.reply('first')
                    last = bot_getter.reply('last')
                    reply_text = bot_getter.reply('text')
                    rp_word = first + ' ' + last + ': \n' + reply_text
                    resp = bot.send(chat_id).message(rp_word, msg_id)
                else:
                    fileid = bot_getter.reply('file')
                    if reply_type == 'photo':
                        resp = bot.send(chat_id).photo(fileid, reply_to=msg_id)
                    elif reply_type == 'video':
                        resp = bot.send(chat_id).video(fileid, reply_to=msg_id)
                    elif reply_type == 'sticker':
                        resp = bot.send(chat_id).sticker(fileid, reply_to=msg_id)
                    elif reply_type == 'file':
                        resp = bot.send(chat_id).file(fileid, reply_to=msg_id)
                    else:
                        resp = 'undefined type'
        else:
            resp = bot.send(chat_id).message(rp_text, msg_id)
        return resp

    elif command.startswith('del'):
        reply_id = bot_getter.reply('id')
        if reply_id == 0:
            return 'Not reply'
        else:
            try:
                to_whom = bot_getter.reply('user')
                grp_admin_list = bot.query(chat_id).group_admin()
                user_id = bot_getter.user()
                bot_admin_list = get_admin_id()
                if to_whom == self_id:
                    if user_id in grp_admin_list or user_id in bot_admin_list:
                        resp = bot.delete(chat_id).message(reply_id)
                        if self_id in grp_admin_list:
                            bot.delete(chat_id).message(msg_id)
                        del_info = bot.send(chat_id).message('Message deleted. This info will disappear in 30 seconds.')
                        del_info_id = bot.get(del_info).message('id')
                        del_del_info = Timer(30, bot.delete(chat_id).message, [del_info_id])
                        del_del_info.start()
                    else:
                        resp = bot.send(chat_id).message(
                            'You are not admin of this group or bot yet. This info will disappear in 30 seconds.',
                            reply_to=msg_id)
                        del_info_id = bot.get(resp).message('id')
                        del_del_info = Timer(30, bot.delete(chat_id).message, [del_info_id])
                        del_del_info.start()
                else:
                    if to_whom == user_id:
                        if self_id in grp_admin_list:
                            resp = bot.delete(chat_id).message(reply_id)
                            bot.delete(chat_id).message(msg_id)
                            del_info = bot.send(chat_id).message(
                                'Message deleted. This info will disappear in 30 seconds.')
                            del_info_id = bot.get(del_info).message('id')
                        else:
                            resp = bot.send(chat_id).message(
                                'DIY (*Delete* It Yourself)', reply_to=msg_id, parse='Markdown')
                            del_info_id = bot.get(resp).message('id')
                        del_del_info = Timer(30, bot.delete(chat_id).message, [del_info_id])
                        del_del_info.start()
                    elif user_id in grp_admin_list and self_id in grp_admin_list:
                        resp = bot.delete(chat_id).message(reply_id)
                        bot.delete(chat_id).message(msg_id)
                        del_info = bot.send(chat_id).message('Message deleted. This info will disappear in 30 seconds.',
                                                             reply_to=msg_id)
                        del_info_id = bot.get(del_info).message('id')
                        del_del_info = Timer(30, bot.delete(chat_id).message, [del_info_id])
                        del_del_info.start()
                    else:
                        resp = False
                return resp
            except KeyError:
                return False

    elif command.startswith('debug'):
        resp = md_debug(chat_id, data)
        return resp

    elif command.startswith(('ping', 'delay')):
        return delay(data)

    else:
        return 'Pass in group'
