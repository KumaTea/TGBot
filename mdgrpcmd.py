from dataio import getchatid, getmsg, sendmsg, getmsgid, editmsg
from mdemergency import mddebug
from mdfunc import randomjoke
from threading import Timer


def mdgrpcmd(data):
    chatid = getchatid(data)
    command = getmsg(data)
    msgid = getmsgid(data)

    if command.startswith('/rp') or command.startswith('/repeat'):
        cont = command.find(' ')
        rptext = command[cont:]
        if cont == -1:
            resp = sendmsg(chatid, command, msgid)
            return resp
        else:
            resp = sendmsg(chatid, rptext, msgid)
            return resp

    elif command.startswith('/joke') or command.startswith('/soviet'):
        joke = randomjoke()
        resp = sendmsg(chatid, joke, msgid)
        jokeid = getmsgid(resp)
        deljoke = Timer(3600, editmsg, [chatid, jokeid, '笑话过期了！请使用 /joke 再来一条。'])
        deljoke.start()
        return resp

    elif command.startswith('/debug'):
        resp = mddebug(data)
        return resp

    else:
        return 'Pass in group'
