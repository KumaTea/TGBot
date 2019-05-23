import requests
from starting import getapi

botapi = getapi()
# GET INFO


def getchatid(data):
    if 'message' in data:
        chatid = data['message']['chat']['id']
    elif 'channel_post' in data:
        chatid = data['channel_post']['chat']['id']
    return chatid


def getmsg(data):
    msgtxt = data['message']['text']
    return msgtxt


def getmsgid(data):
    if 'message' in data:
        msgid = data['message']['message_id']
    elif 'result' in data:
        msgid = data['result']['message_id']
    return msgid


def getfileid(data):
    if 'photo' in data['message']:
        fileid = data['message']['photo'][-1]['file_id']
        return fileid
    elif 'video' in data['message']:
        fileid = data['message']['video']['file_id']
        return fileid
    elif 'sticker' in data['message']:
        fileid = data['message']['sticker']['file_id']
        return fileid
    elif 'document' in data['message']:
        fileid = data['message']['document']['file_id']
        return fileid
    else:
        return 'Unknown Type'

# SEND ITEM


def sendmsg(chatid, msg, replyto=False, parse=False):
    """
    sendmsg(chatid, msg, replyto=False, parse=False)
    parse = 'Markdown'
    """
    # should be json which includes at least `chat_id` and `text`
    answer = {
        "chat_id": chatid,
        "text": msg,
    }
    if replyto:
        answer['reply_to_message_id'] = replyto
    if parse:
        answer['parse_mode'] = parse
    msgurl = botapi + 'sendMessage'
    orresp = requests.post(msgurl, json=answer)
    resp = orresp.json()
    return resp


def sendsticker(chatid, fileid, replyto=False):
    """sendsticker(chatid, fileid, replyto=False)"""
    # should be json which includes at least `chat_id` and `text`
    answer = {
        "chat_id": chatid,
        "sticker": fileid,
    }
    if replyto:
        answer['reply_to_message_id'] = replyto
    msgurl = botapi + 'sendSticker'
    orresp = requests.post(msgurl, json=answer)
    resp = orresp.json()
    return resp


def sendfile(chatid, file, replyto=False, upload=False):
    """sendfile(chatid, file, replyto=False, upload=False)"""
    if upload:
        with open(file, 'rb') as fl:
            sending = {'document': fl}
            if replyto:
                newurl = botapi + 'sendDocument?chat_id=' + str(chatid) + '&' + str(replyto)
            else:
                newurl = botapi + 'sendDocument?chat_id=' + str(chatid)
            orresp = requests.post(newurl, files=sending)
            resp = orresp.json()
        return resp
    else:
        answer = {
            "chat_id": chatid,
            "document": file,
        }
        if replyto:
            answer['reply_to_message_id'] = replyto
        msgurl = botapi + 'sendDocument'
        orresp = requests.post(msgurl, json=answer)
        resp = orresp.json()
        return resp


def sendphoto(chatid, photo, replyto=False, upload=False):
    """sendphoto(chatid, photo, replyto=False, upload=False)"""
    if upload:
        with open(photo, 'rb') as fl:
            sending = {'photo': fl}
            if replyto:
                newurl = botapi + 'sendPhoto?chat_id=' + str(chatid) + '&' + str(replyto)
            else:
                newurl = botapi + 'sendPhoto?chat_id=' + str(chatid)
            orresp = requests.post(newurl, files=sending)
            resp = orresp.json()
            return resp
    else:
        answer = {
            "chat_id": chatid,
            "document": photo,
        }
        if replyto:
            answer['reply_to_message_id'] = replyto
        msgurl = botapi + 'sendPhoto'
        orresp = requests.post(msgurl, json=answer)
        resp = orresp.json()
        return resp


def sendvideo(chatid, video, replyto=False, upload=False):
    """sendvideo(chatid, video, replyto=False, upload=False)"""
    if upload:
        with open(video, 'rb') as fl:
            sending = {'video': fl}
            if replyto:
                newurl = botapi + 'sendVideo?chat_id=' + str(chatid) + '&' + str(replyto)
            else:
                newurl = botapi + 'sendVideo?chat_id=' + str(chatid)
            orresp = requests.post(newurl, files=sending)
            resp = orresp.json()
            return resp
    else:
        answer = {
            "chat_id": chatid,
            "document": video,
        }
        if replyto:
            answer['reply_to_message_id'] = replyto
        msgurl = botapi + 'sendVideo'
        orresp = requests.post(msgurl, json=answer)
        resp = orresp.json()
        return resp


def editmsg(chatid, msgid, text):
    """editmessage(chatid, msgid, text)"""
    answer = {
        "chat_id": chatid,
        "message_id": msgid,
        "text": text,
    }
    msgurl = botapi + 'editMessageText'
    orresp = requests.post(msgurl, json=answer)
    resp = orresp.json()
    return resp
