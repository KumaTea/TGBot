from dataIO import get_chat_id, get_msg, send_msg, get_msg_id, edit_msg, get_reply, del_msg, get_user_info, get_group_admin, send_file, send_video, send_photo, send_sticker
from mdDebug import md_debug
from mdFunc import random_joke, sysu_joke
from threading import Timer
from botInfo import self_id
from starting import getadminid


def md_group_cmd(data):
    chat_id = get_chat_id(data)
    command = get_msg(data)
    msg_id = get_msg_id(data)

    if command.startswith(('/rp', '/repeat')):
        cont = command.find(' ')
        rptext = command[cont:]
        if cont == -1:
            replyid = get_reply(data)
            if replyid == 0:
                resp = send_msg(chat_id, command, msg_id)
                return resp
            else:
                replytype = get_reply(data, 'type')
                if replytype == 'text':
                    first = get_reply(data, 'first')
                    last = get_reply(data, 'last')
                    replytext = get_reply(data, 'text')
                    rpword = first + ' ' + last + ': \n' + replytext
                    resp = send_msg(chat_id, rpword, msg_id)
                else:
                    fileid = get_reply(data, 'fileid')
                    if replytype == 'photo':
                        resp = send_photo(chat_id, fileid, msg_id)
                    elif replytype == 'video':
                        resp = send_video(chat_id, fileid, msg_id)
                    elif replytype == 'sticker':
                        resp = send_sticker(chat_id, fileid, msg_id)
                    elif replytype == 'file':
                        resp = send_file(chat_id, fileid, msg_id)
                return resp
        else:
            resp = send_msg(chat_id, rptext, msg_id)
            return resp

    elif command.startswith(('/sysu', '/中', '/双鸭山')):
        joke = sysu_joke()
        resp = send_msg(chat_id, joke, msg_id)
        return resp

    elif command.startswith(('/joke', '/soviet')):
        joke = random_joke()
        resp = send_msg(chat_id, joke, msg_id)
        jokeid = get_msg_id(resp)
        deljoke = Timer(3600, edit_msg, [chat_id, jokeid, '笑话已过期！请使用 /joke 再来一条。'])
        deljoke.start()
        return resp

    elif command.startswith('/del'):
        replyid = get_reply(data)
        if replyid == 0:
            return 'Not reply'
        else:
            istome = get_reply(data, 'id')
            if istome == self_id:
                usrid = get_user_info(data)
                grpadmin = get_group_admin(chat_id)
                botadmin = getadminid()
                if usrid in grpadmin or usrid in botadmin:
                    resp = del_msg(chat_id, replyid)
                    delinfo = send_msg(chat_id, 'Message deleted. This info will disappear in one minute.', msg_id)
                    delinfoid = get_msg_id(delinfo)
                    deldel = Timer(60, del_msg, [chat_id, delinfoid])
                    deldel.start()
                    return resp
                else:
                    resp = send_msg(chat_id, 'You are not admin of this group or bot yet. This info will disappear in one minute.', msg_id)
                    respid = get_msg_id(resp)
                    deldel = Timer(60, del_msg, [chat_id, respid])
                    deldel.start()
                    return resp
            else:
                return 'Not to me'

    elif command.startswith('/debug'):
        cont = command.find(' ')
        if cont == -1:
            resp = md_debug(data)
        else:
            resp = md_debug(data, True)
        return resp

    else:
        return 'Pass in group'
