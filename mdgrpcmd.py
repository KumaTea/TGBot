from dataio import getchatid, getmsg, sendmsg, getmsgid, editmsg, getreply, delmsg, getusrinfo, getgrpadmin, sendfile, sendvideo, sendphoto,sendsticker
from mddebug import mddebug
from mdfunc import randomjoke, sysujoke, mars
from threading import Timer
from botinfo import selfid
from starting import getadminid


def mdgrpcmd(data):
    chatid = getchatid(data)
    command = getmsg(data)
    msgid = getmsgid(data)

    if command.startswith(('/rp', '/repeat')):
        cont = command.find(' ')
        rptext = command[cont:]
        if cont == -1:
            replyid = getreply(data)
            if replyid == 0:
                resp = sendmsg(chatid, command, msgid)
                return resp
            else:
                replytype = getreply(data, 'type')
                if replytype == 'text':
                    first = getreply(data, 'first')
                    last = getreply(data, 'last')
                    replytext = getreply(data, 'text')
                    rpword = first + ' ' + last + ': \n' + replytext
                    resp = sendmsg(chatid, rpword, msgid)
                else:
                    fileid = getreply(data, 'fileid')
                    if replytype == 'photo':
                        resp = sendphoto(chatid, fileid, msgid)
                    elif replytype == 'video':
                        resp = sendvideo(chatid, fileid, msgid)
                    elif replytype == 'sticker':
                        resp = sendsticker(chatid, fileid, msgid)
                    elif replytype == 'file':
                        resp = sendfile(chatid, fileid, msgid)
                return resp
        else:
            resp = sendmsg(chatid, rptext, msgid)
            return resp

    elif command.startswith(('/sysu', '/中', '/双鸭山')):
        joke = sysujoke()
        resp = sendmsg(chatid, joke, msgid)
        return resp

    elif command.startswith(('/joke', '/soviet')):
        joke = randomjoke()
        resp = sendmsg(chatid, joke, msgid)
        jokeid = getmsgid(resp)
        deljoke = Timer(3600, editmsg, [chatid, jokeid, '笑话已过期！请使用 /joke 再来一条。'])
        deljoke.start()
        return resp

    elif command.startswith(('/mars', '/old', '/火星', '/老')):
        marspic = mars()
        resp = sendphoto(chatid, marspic)
        return resp

    elif command.startswith('/del'):
        replyid = getreply(data)
        if replyid == 0:
            return 'Not reply'
        else:
            istome = getreply(data, 'id')
            if istome == selfid:
                usrid = getusrinfo(data)
                grpadmin = getgrpadmin(chatid)
                botadmin = getadminid()
                if usrid in grpadmin or usrid in botadmin:
                    resp = delmsg(chatid, replyid)
                    delinfo = sendmsg(chatid, 'Message deleted. This info will disappear in one minute.', msgid)
                    delinfoid = getmsgid(delinfo)
                    deldel = Timer(60, delmsg, [chatid, delinfoid])
                    deldel.start()
                    return resp
                else:
                    resp = sendmsg(chatid, 'You are not admin of this group or bot yet. This info will disappear in one minute.', msgid)
                    respid = getmsgid(resp)
                    deldel = Timer(60, delmsg, [chatid, respid])
                    deldel.start()
                    return resp
            else:
                return 'Not to me'

    elif command.startswith('/debug'):
        cont = command.find(' ')
        if cont == -1:
            resp = mddebug(data)
        else:
            resp = mddebug(data, True)
        return resp

    else:
        return 'Pass in group'
