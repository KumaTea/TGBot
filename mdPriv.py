from dataIO import get_chat_id, get_file_id, get_msg, send_msg  # get_msg_id, sendsticker, sendfile, sendphoto, sendvideo
from mdPrivCmd import md_priv_cmd


def priv_text(data):
    msg = get_msg(data)
    if msg.startswith('/'):
        resp = md_priv_cmd(data)
        return resp
    else:
        chatid = get_chat_id(data)
        resp = send_msg(chatid, msg)
        return resp


def priv_sticker(data):
    chatid = get_chat_id(data)
    sticker = get_file_id(data)
    resp = send_msg(chatid, sticker)
    return resp


def priv_photo(data):
    chatid = get_chat_id(data)
    photo = get_file_id(data)
    resp = send_msg(chatid, photo)
    return resp


def priv_video(data):
    chatid = get_chat_id(data)
    video = get_file_id(data)
    resp = send_msg(chatid, video)
    return resp


def priv_file(data):
    chatid = get_chat_id(data)
    file = get_file_id(data)
    resp = send_msg(chatid, file)
    return resp


def priv_gif(data):
    chatid = get_chat_id(data)
    file = get_file_id(data)
    resp = send_msg(chatid, file)
    return resp

