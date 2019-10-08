from mdDebug import md_debug
from threading import Timer
from botInfo import self_id
from starting import getadminid
from botSession import bot


def group_cmd(data):
    chat_id = bot.get(data).chat('id')
    command = bot.get(data).message('text')[1:]
    msg_id = bot.get(data).message('id')

    if command.startswith(('rp', 'repeat')):
        cont = command.find(' ')
        rptext = command[cont:]
        if cont == -1:
            replyid = bot.get(data).reply('id')
            if replyid == 0:
                resp = bot.send(chat_id).message(f'/{command}', msg_id)
            else:
                replytype = bot.get(data).reply('type')
                if replytype == 'text':
                    first = bot.get(data).reply('first')
                    last = bot.get(data).reply('last')
                    replytext = bot.get(data).reply('text')
                    rpword = first + ' ' + last + ': \n' + replytext
                    resp = bot.send(chat_id).message(rpword, msg_id)
                else:
                    fileid = bot.get(data).reply('file')
                    if replytype == 'photo':
                        resp = bot.send(chat_id).photo(fileid, reply_to=msg_id)
                    elif replytype == 'video':
                        resp = bot.send(chat_id).video(fileid, reply_to=msg_id)
                    elif replytype == 'sticker':
                        resp = bot.send(chat_id).sticker(fileid, reply_to=msg_id)
                    elif replytype == 'file':
                        resp = bot.send(chat_id).file(fileid, reply_to=msg_id)
                    else:
                        resp = 'undefined type'
        else:
            resp = bot.send(chat_id).message(rptext, msg_id)
        return resp

    elif command.startswith('del'):
        replyid = bot.get(data).reply('id')
        if replyid == 0:
            return 'Not reply'
        else:
            try:
                to_whom = bot.get(data).reply('user')
                grp_admin_list = bot.query(chat_id).group_admin()
                user_id = bot.get(data).user()
                bot_admin_list = getadminid()
                if to_whom == self_id:
                    if user_id in grp_admin_list or user_id in bot_admin_list:
                        resp = bot.delete(chat_id).message(replyid)
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
                            resp = bot.delete(chat_id).message(replyid)
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
                        resp = bot.delete(chat_id).message(replyid)
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
        resp = md_debug(data)
        return resp

    elif command.startswith(('ping', 'delay')):
        first_timestamp = bot.get(data).message('time')
        second = bot.send(chat_id).message('Checking delay...', reply_to=msg_id)
        second_timestamp = bot.get(second).message('time')
        second_msg_id = bot.get(second).message('id')
        delay = second_timestamp - first_timestamp
        if delay == 0:
            status = 'excellent'
        elif delay == 1:
            status = 'good'
        else:
            status = 'bad'
        result = bot.edit(chat_id, second_msg_id).message(f'Delay is {delay}s.\nThe connectivity is {status}.')
        return result

    else:
        return 'Pass in group'
