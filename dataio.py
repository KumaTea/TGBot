import requests

botapi = 'None'


def setapi():
    global botapi
    botapi = 'https://api.telegram.org/' + input(
        'Please input your bot API.\nIt should start with \"bot\", include \":\" and without \"/\".\n') + '/'


def getchatid(data):
    if data.get('message') is not None:
        chatid = data['message']['chat']['id']
    elif data.get('channel_post') is not None:
        chatid = data['channel_post']['chat']['id']
    return chatid


def getmsg(data):
    msgtxt = data['message']['text']
    return msgtxt


def sendmsg(chatid, msg):
    # should be json which includes at least `chat_id` and `text`
    answer = {
        "chat_id": chatid,
        "text": msg,
    }
    msgurl = botapi + 'sendMessage'
    orresp = requests.post(msgurl, json=answer)
    resp = orresp.json()
    return resp


def sendsticker(chatid, fileid):
    # should be json which includes at least `chat_id` and `text`
    answer = {
        "chat_id": chatid,
        "sticker": fileid,
    }
    msgurl = botapi + 'sendSticker'
    orresp = requests.post(msgurl, json=answer)
    resp = orresp.json()
    return resp


def ifexists(obj, typ, empty='None'):
    try:
        obj
    except typ:
        result = empty
    else:
        result = obj
    return result


def getmsgid(data):
    msgid = data['message']['message_id']
    return msgid
