from dataio import getchatid, getmsg, sendmsg, getmsgid
from mdemergency import mddebug
from mdfunc import randomjoke


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
        return resp

    elif command.startswith('/debug'):
        resp = mddebug(data)
        return resp

    else:
        return 'Pass in group'
