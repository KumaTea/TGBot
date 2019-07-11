from dataIO import get_chat_id, get_msg_id, get_file_id, get_msg, send_msg, send_sticker, send_file, send_photo, send_video, send_gif
from mdGroupCmd import md_group_cmd
from botDb import welcome_msg


def group_new_member(data):
    if not data['message']['new_chat_member']['is_bot']:
        group_id = get_chat_id(data)
        if welcome_msg.get(group_id) is not None:
            resp = 'Initialize'
            if welcome_msg[group_id].get('message') is not None:
                resp = send_msg(group_id, welcome_msg[group_id]['message'])
            if welcome_msg[group_id].get('sticker') is not None:
                resp = send_sticker(group_id, welcome_msg[group_id]['sticker'])
        else:
            resp = 'Not familiar using default'
        return resp
    else:
        return 'Is bot'


def group_text(data):
    msg = get_msg(data)
    if msg.startswith('/'):
        resp = md_group_cmd(data)
        return resp
    else:
        chat_id = get_chat_id(data)
        msg_id = get_msg_id(data)
        resp = send_msg(chat_id, msg, msg_id)
        return resp


def group_sticker(data):
    chat_id = get_chat_id(data)
    sticker = get_file_id(data)
    msg_id = get_msg_id(data)
    resp = send_sticker(chat_id, sticker, msg_id)
    return resp


def group_photo(data):
    chat_id = get_chat_id(data)
    photo = get_file_id(data)
    msg_id = get_msg_id(data)
    resp = send_photo(chat_id, photo, msg_id)
    return resp


def group_video(data):
    chat_id = get_chat_id(data)
    video = get_file_id(data)
    msg_id = get_msg_id(data)
    resp = send_video(chat_id, video, msg_id)
    return resp


def group_file(data):
    chat_id = get_chat_id(data)
    file = get_file_id(data)
    msg_id = get_msg_id(data)
    resp = send_file(chat_id, file, msg_id)
    return resp


def group_gif(data):
    chat_id = get_chat_id(data)
    file = get_file_id(data)
    msg_id = get_msg_id(data)
    resp = send_gif(chat_id, file, msg_id)
    return resp

