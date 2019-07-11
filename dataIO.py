import requests
from starting import getapi

bot_api = getapi()

# GET INFO


def get_chat_id(data):
    if 'message' in data:
        chat_id = data['message']['chat']['id']
    elif 'edited_message' in data:
        chat_id = data['edited_message']['chat']['id']
    elif 'channel_post' in data:
        chat_id = data['channel_post']['chat']['id']
    elif 'edited_channel_post' in data:
        chat_id = data['edited_channel_post']['chat']['id']
    elif 'channel_post' in data:
        chat_id = data['left_chat_member']['chat']['id']
    else:
        chat_id = 0
    return chat_id


def get_msg(data, prefix='message'):
    msg_text = data[prefix]['text']
    return msg_text


def get_msg_id(data, prefix='message'):
    if 'message' in data:
        msg_id = data['message']['message_id']
    elif 'result' in data:
        msg_id = data['result']['message_id']
    else:
        msg_id = data[prefix]['message_id']
    return msg_id


def get_reply(data, info='msgid'):
    """info:msgid, id, first, last, username, text, type: text/media, fileid"""
    if 'reply_to_message' in data['message']:
        if info == 'msgid':
            reply = data['message']['reply_to_message']['message_id']
        elif info == 'id':
            reply = data['message']['reply_to_message']['from']['id']
        elif info == 'text':
            reply = data['message']['reply_to_message']['text']
        elif info == 'type':
            reply = get_msg_type(data['message'], 'reply_to_message')
        elif info == 'fileid':
            reply = get_file_id(data['message'], 'reply_to_message')
        elif info == 'first':
            reply = data['message']['reply_to_message']['from']['first_name']
        elif info == 'last':
            reply = data['message']['reply_to_message']['from'].get('last_name', '')
        elif info == 'username':
            reply = data['message']['reply_to_message']['from'].get('username', 'No username')
    else:
        reply = 0
    return reply


def get_msg_type(data, prefix='message'):
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


def get_file_id(data, prefix='message'):
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


def get_user_info(data, info='id'):
    """info: id, first, last, username, language, bot"""
    if info == 'id':
        user_info = data['message']['from']['id']
    elif 'first' in info:
        user_info = data['message']['from']['first_name']
    elif 'last' in info:
        user_info = data['message']['from'].get('last_name', 'No last name')
    elif info == 'username':
        user_info = data['message']['from'].get('username', 'No username')
    elif 'lang' in info:
        user_info = data['message']['from'].get('language_code', 'zh-Hans')
    elif info == 'bot':
        user_info = data['message']['from']['is_bot']
    else:
        user_info = 'Unknown argument'
    return user_info


def get_group_admin(chat_id):
    if type(chat_id) == dict:
        chat_id = get_chat_id(chat_id)
    answer = {
        "chat_id": chat_id,
    }
    msg_url = bot_api + 'getChatAdministrators'
    ori_resp = requests.post(msg_url, json=answer)
    res = ori_resp.json()
    adm = []
    for admin_user in res['result']:
        adm.append(admin_user['user']['id'])
    resp = adm
    return resp


# SEND ITEM


def send_msg(chat_id, msg, reply_to=False, parse=False):
    """
    sendmsg(chatid, msg, replyto=False, parse=False)
    parse = 'Markdown'
    """
    # should be json which includes at least `chat_id` and `text`
    answer = {
        "chat_id": chat_id,
        "text": msg,
    }
    if reply_to:
        answer['reply_to_message_id'] = reply_to
    if parse:
        answer['parse_mode'] = parse
    msg_url = bot_api + 'sendMessage'
    ori_resp = requests.post(msg_url, json=answer)
    resp = ori_resp.json()
    return resp


def send_sticker(chat_id, fileid, reply_to=False):
    """sendsticker(chatid, fileid, replyto=False)"""
    # should be json which includes at least `chat_id` and `text`
    answer = {
        "chat_id": chat_id,
        "sticker": fileid,
    }
    if reply_to:
        answer['reply_to_message_id'] = reply_to
    msgurl = bot_api + 'sendSticker'
    orresp = requests.post(msgurl, json=answer)
    resp = orresp.json()
    return resp


def send_file(chat_id, file, reply_to=False, upload=False):
    """sendfile(chatid, file, replyto=False, upload=False)"""
    if upload:
        with open(file, 'rb') as fl:
            sending = {'document': fl}
            if reply_to:
                newurl = bot_api + 'sendDocument?chat_id=' + str(chat_id) + '&' + str(reply_to)
            else:
                newurl = bot_api + 'sendDocument?chat_id=' + str(chat_id)
            orresp = requests.post(newurl, files=sending)
            resp = orresp.json()
        return resp
    else:
        answer = {
            "chat_id": chat_id,
            "document": file,
        }
        if reply_to:
            answer['reply_to_message_id'] = reply_to
        msgurl = bot_api + 'sendDocument'
        orresp = requests.post(msgurl, json=answer)
        resp = orresp.json()
        return resp


def send_photo(chat_id, photo, reply_to=False, upload=False):
    """sendphoto(chatid, photo, replyto=False, upload=False)"""
    if upload:
        with open(photo, 'rb') as fl:
            sending = {'photo': fl}
            if reply_to:
                newurl = bot_api + 'sendPhoto?chat_id=' + str(chat_id) + '&' + str(reply_to)
            else:
                newurl = bot_api + 'sendPhoto?chat_id=' + str(chat_id)
            orresp = requests.post(newurl, files=sending)
            resp = orresp.json()
            return resp
    else:
        answer = {
            "chat_id": chat_id,
            "photo": photo,
        }
        if reply_to:
            answer['reply_to_message_id'] = reply_to
        msgurl = bot_api + 'sendPhoto'
        orresp = requests.post(msgurl, json=answer)
        resp = orresp.json()
        return resp


def send_video(chat_id, video, reply_to=False, upload=False):
    """sendvideo(chatid, video, replyto=False, upload=False)"""
    if upload:
        with open(video, 'rb') as fl:
            sending = {'video': fl}
            if reply_to:
                newurl = bot_api + 'sendVideo?chat_id=' + str(chat_id) + '&' + str(reply_to)
            else:
                newurl = bot_api + 'sendVideo?chat_id=' + str(chat_id)
            orresp = requests.post(newurl, files=sending)
            resp = orresp.json()
            return resp
    else:
        answer = {
            "chat_id": chat_id,
            "video": video,
        }
        if reply_to:
            answer['reply_to_message_id'] = reply_to
        msgurl = bot_api + 'sendVideo'
        orresp = requests.post(msgurl, json=answer)
        resp = orresp.json()
        return resp


def send_gif(chat_id, gif, reply_to=False, upload=False):
    """sendgif(chatid, video, replyto=False, upload=False)"""
    if upload:
        with open(gif, 'rb') as fl:
            sending = {'animation': fl}
            if reply_to:
                newurl = bot_api + 'sendAnimation?chat_id=' + str(chat_id) + '&' + str(reply_to)
            else:
                newurl = bot_api + 'sendAnimation?chat_id=' + str(chat_id)
            orresp = requests.post(newurl, files=sending)
            resp = orresp.json()
            return resp
    else:
        answer = {
            "chat_id": chat_id,
            "animation": gif,
        }
        if reply_to:
            answer['reply_to_message_id'] = reply_to
        msgurl = bot_api + 'sendAnimation'
        orresp = requests.post(msgurl, json=answer)
        resp = orresp.json()
        return resp


# MESSAGE OPERATION


def edit_msg(chat_id, msg_id, text):
    """editmessage(chatid, msgid, text)"""
    answer = {
        "chat_id": chat_id,
        "message_id": msg_id,
        "text": text,
    }
    msgurl = bot_api + 'editMessageText'
    orresp = requests.post(msgurl, json=answer)
    resp = orresp.json()
    return resp


def del_msg(chat_id, msg_id):
    answer = {
        "chat_id": chat_id,
        "message_id": msg_id,
    }
    msgurl = bot_api + 'deleteMessage'
    orresp = requests.post(msgurl, json=answer)
    resp = orresp.json()
    return resp
