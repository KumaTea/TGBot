from dataio import getchatid, getmsgid, getfileid, getmsg, sendmsg, sendsticker, sendfile, sendphoto, sendvideo
from mdgrpcmd import mdgrpcmd


def grpnewmem(data):
    if not data['message']['new_chat_member']['is_bot']:
        groupid = getchatid(data)
        sendmsg(groupid, '欢迎新大佬！')
        resp = sendsticker(groupid, 'CAADBQADgAADMwMcCJWbCk051Y0BAg')
        return resp


def grptext(data):
    msg = getmsg(data)
    if msg.startswith('/'):
        resp = mdgrpcmd(data)
        return resp
    else:
        chatid = getchatid(data)
        msgid = getmsgid(data)
        resp = sendmsg(chatid, msg, msgid)
        return resp


def grpsticker(data):
    chatid = getchatid(data)
    sticker = getfileid(data)
    msgid = getmsgid(data)
    resp = sendsticker(chatid, sticker, msgid)
    return resp


def grpphoto(data):
    chatid = getchatid(data)
    photo = getfileid(data)
    msgid = getmsgid(data)
    resp = sendphoto(chatid, photo, msgid)
    return resp


def grpvideo(data):
    chatid = getchatid(data)
    video = getfileid(data)
    msgid = getmsgid(data)
    resp = sendvideo(chatid, video, msgid)
    return resp


def grpfile(data):
    chatid = getchatid(data)
    file = getfileid(data)
    msgid = getmsgid(data)
    resp = sendfile(chatid, file, msgid)
    return resp
