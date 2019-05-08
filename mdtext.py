from dataio import getchatid, getmsg, sendmsg
from mdcmd import dealcmd


def dealtext(data):
    content = getmsg(data)
    if content.startswith('/'):
        resp = dealcmd(data)
        return resp
    else:
        resp = repeatmsg(data)
        return resp


def repeatmsg(data):
    chatid = getchatid(data)
    rptext = getmsg(data)
    resp = sendmsg(chatid, rptext)
    return resp
