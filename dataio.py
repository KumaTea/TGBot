import requests
from starting import getapi

botapi = getapi()
# GET INFO


def getchatid(data):
    if data.get('message') is not None:
        chatid = data['message']['chat']['id']
    elif data.get('channel_post') is not None:
        chatid = data['channel_post']['chat']['id']
    return chatid


def getmsg(data):
    msgtxt = data['message']['text']
    return msgtxt


def getmsgid(data):
    msgid = data['message']['message_id']
    return msgid


def getfileid(data):
    if data['message'].get('photo') is not None:
        fileid = data['message']['photo'][-1]['file_id']
        return fileid
    elif data['message'].get('video') is not None:
        fileid = data['message']['video']['file_id']
        return fileid
    elif data['message'].get('sticker') is not None:
        fileid = data['message']['sticker']['file_id']
        return fileid
    elif data['message'].get('document') is not None:
        fileid = data['message']['document']['file_id']
        return fileid
    else:
        return 'Unknown Type'

# SEND ITEM


def sendmsg(chatid, msg, replyto=False):
    # should be json which includes at least `chat_id` and `text`
    if replyto:
        answer = {
            "chat_id": chatid,
            "text": msg,
            "reply_to_message_id": replyto,
        }
    else:
        answer = {
            "chat_id": chatid,
            "text": msg,
        }
    msgurl = botapi + 'sendMessage'
    orresp = requests.post(msgurl, json=answer)
    resp = orresp.json()
    return resp


def sendsticker(chatid, fileid, replyto=False):
    # should be json which includes at least `chat_id` and `text`
    if replyto:
        answer = {
            "chat_id": chatid,
            "sticker": fileid,
            "reply_to_message_id": replyto,
        }
    else:
        answer = {
            "chat_id": chatid,
            "sticker": fileid,
        }
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
        if replyto:
            answer = {
                "chat_id": chatid,
                "document": file,
                "reply_to_message_id": replyto,
            }
        else:
            answer = {
                "chat_id": chatid,
                "document": file,
            }
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
        if replyto:
            answer = {
                "chat_id": chatid,
                "photo": photo,
                "reply_to_message_id": replyto,
            }
        else:
            answer = {
                "chat_id": chatid,
                "photo": photo,
            }
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
        if replyto:
            answer = {
                "chat_id": chatid,
                "video": video,
                "reply_to_message_id": replyto,
            }
        else:
            answer = {
                "chat_id": chatid,
                "video": video,
            }
        msgurl = botapi + 'sendVideo'
        orresp = requests.post(msgurl, json=answer)
        resp = orresp.json()
        return resp
