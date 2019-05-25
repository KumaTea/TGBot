import requests
from starting import getapi

botapi = getapi()

# GET INFO


def getchatid(data):
    if 'message' in data:
        chatid = data['message']['chat']['id']
    elif 'edited_message' in data:
        chatid = data['edited_message']['chat']['id']
    elif 'channel_post' in data:
        chatid = data['channel_post']['chat']['id']
    elif 'edited_channel_post' in data:
        chatid = data['edited_channel_post']['chat']['id']
    elif 'channel_post' in data:
        chatid = data['left_chat_member']['chat']['id']
    else:
        chatid = 0
    return chatid


def getmsg(data, prefix='message'):
    msgtxt = data[prefix]['text']
    return msgtxt


def getmsgid(data, prefix='message'):
    if 'message' in data:
        msgid = data['message']['message_id']
    elif 'result' in data:
        msgid = data['result']['message_id']
    else:
        msgid = data[prefix]['message_id']
    return msgid


def getreply(data, info='msgid'):
    """info:msgid, id, first, last, username, text, type: text/media, fileid"""
    if 'reply_to_message' in data['message']:
        if info == 'msgid':
            reply = data['message']['reply_to_message']['message_id']
        elif info == 'id':
            reply = data['message']['reply_to_message']['from']['id']
        elif info == 'text':
            reply = data['message']['reply_to_message']['text']
        elif info == 'type':
            reply = getmsgtype(data['message'], 'reply_to_message')
        elif info == 'fileid':
            reply = getfileid(data['message'], 'reply_to_message')
        elif info == 'first':
            reply = data['message']['reply_to_message']['from']['first_name']
        elif info == 'last':
            reply = data['message']['reply_to_message']['from'].get('last_name', '')
        elif info == 'username':
            reply = data['message']['reply_to_message']['from'].get('username', 'No username')
    else:
        reply = 0
    return reply


def getmsgtype(data, prefix='message'):
    if 'photo' in data[prefix]:
        return 'photo'
    elif 'video' in data[prefix]:
        return 'video'
    elif 'sticker' in data[prefix]:
        return 'sticker'
    elif 'document' in data[prefix]:
        return 'document'
    elif 'text' in data[prefix]:
        return 'text'
    else:
        return 'Unknown Type'


def getfileid(data, prefix='message'):
    if 'photo' in data[prefix]:
        fileid = data[prefix]['photo'][-1]['file_id']
        return fileid
    elif 'video' in data[prefix]:
        fileid = data[prefix]['video']['file_id']
        return fileid
    elif 'sticker' in data[prefix]:
        fileid = data[prefix]['sticker']['file_id']
        return fileid
    elif 'document' in data[prefix]:
        fileid = data[prefix]['document']['file_id']
        return fileid
    else:
        return 'Unknown Type'


def getusrinfo(data, info='id'):
    """info: id, first, last, username, language, bot"""
    if info == 'id':
        usrinfo = data['message']['from']['id']
    elif info == 'first':
        usrinfo = data['message']['from']['first_name']
    elif info == 'last':
        usrinfo = data['message']['from'].get('last_name', 'No last name')
    elif info == 'username':
        usrinfo = data['message']['from'].get('username', 'No username')
    elif info == 'language':
        usrinfo = data['message']['from']['language_code']
    elif info == 'bot':
        usrinfo = data['message']['from']['is_bot']
    else:
        usrinfo = 'Unknown argument'
    return usrinfo


def getgrpadmin(chatid):
    if type(chatid) == dict:
        chatid = getchatid(chatid)
    answer = {
        "chat_id": chatid,
    }
    msgurl = botapi + 'getChatAdministrators'
    orresp = requests.post(msgurl, json=answer)
    res = orresp.json()
    adm = []
    for admusr in res['result']:
        adm.append(admusr['user']['id'])
    resp = adm
    return resp


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
            "photo": photo,
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
            "video": video,
        }
        if replyto:
            answer['reply_to_message_id'] = replyto
        msgurl = botapi + 'sendVideo'
        orresp = requests.post(msgurl, json=answer)
        resp = orresp.json()
        return resp


# MESSAGE OPERATION


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


def delmsg(chatid, msgid):
    answer = {
        "chat_id": chatid,
        "message_id": msgid,
    }
    msgurl = botapi + 'deleteMessage'
    orresp = requests.post(msgurl, json=answer)
    resp = orresp.json()
    return resp
