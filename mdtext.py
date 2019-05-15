from dataio import getchatid, getmsg, sendmsg
from mdcmd import mdcmd


def mdtext(data):
    content = getmsg(data)
    if content.startswith('/'):
        resp = mdcmd(data)
        return resp
    else:
        resp = repeatmsg(data)
        return resp


def repeatmsg(data):
    chatid = getchatid(data)
    rptext = getmsg(data)
    resp = sendmsg(chatid, rptext)
    return resp
