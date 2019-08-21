from mdDebug import md_debug
from mdFunc import random_joke, sysu_joke
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
            resp = bot.send(chat_id).message(rptext, msg_id)
        return resp

    elif command.startswith(('sysu', '中', '双鸭山')):
        joke = sysu_joke()
        resp = bot.send(chat_id).message(joke, msg_id)
        return resp

    elif command.startswith(('joke', 'soviet')):
        joke = random_joke()
        resp = bot.send(chat_id).message(joke, msg_id)
        jokeid = bot.get(resp).message('id')
        deljoke = Timer(3600, bot.edit(chat_id, jokeid).message, ['笑话已过期！请使用 /joke 再来一条。'])
        deljoke.start()
        return resp

    elif command.startswith('del'):
        replyid = bot.get(data).reply('id')
        if replyid == 0:
            return 'Not reply'
        else:
            istome = bot.get(data).reply('user')
            grpadmin = bot.get(data).group_admin(chat_id)
            usrid = bot.get(data).user()
            botadmin = getadminid()
            if istome == self_id:
                if usrid in grpadmin or usrid in botadmin:
                    resp = bot.delete(chat_id).message(replyid)
                    delinfo = bot.send(chat_id).message('Message deleted. This info will disappear in one minute.', reply_to=msg_id)
                    delinfoid = bot.get(delinfo).message('id')
                    deldel = Timer(60, bot.delete(chat_id).message, [delinfoid])
                    deldel.start()
                else:
                    resp = bot.send(chat_id).message('You are not admin of this group or bot yet. This info will disappear in one minute.', reply_to=msg_id)
                    respid = bot.get(resp).message('id')
                    deldel = Timer(60, bot.delete(chat_id).message, [respid])
                    deldel.start()
            else:
                if usrid in grpadmin and self_id in grpadmin:
                    resp = bot.delete(chat_id).message(replyid)
                    delinfo = bot.send(chat_id).message('Message deleted. This info will disappear in one minute.', reply_to=msg_id)
                    delinfoid = bot.get(delinfo).message('id')
                    deldel = Timer(60, bot.delete(chat_id).message, [delinfoid])
                    deldel.start()
                else:
                    resp = False
        return resp

    elif command.startswith('debug'):
        resp = md_debug(data)
        return resp

    else:
        return 'Pass in group'
