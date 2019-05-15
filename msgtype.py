from mdgroup import newmem
from mdtext import mdtext
from mdphoto import mdphoto
from mdvideo import mdvideo
from mdsticker import mdsticker
from mddoc import mddoc
from mduktp import mduktp


def msgtype(data):
    try:
        data['message']['new_chat_member']
    except KeyError:
        pass
    else:
        resp = newmem(data)
        return resp

    try:
        data['message']['text']
    except KeyError:
        pass
    else:
        resp = mdtext(data)
        return resp

    try:
        data['message']['sticker']
    except KeyError:
        pass
    else:
        resp = mdsticker(data)
        return resp

    try:
        data['message']['photo']
    except KeyError:
        pass
    else:
        resp = mdphoto(data)
        return resp

    try:
        data['message']['video']
    except KeyError:
        pass
    else:
        resp = mdvideo(data)
        return resp

    try:
        data['message']['document']
    except KeyError:
        pass
    else:
        resp = mddoc(data)
        return resp

    try:
        data['message']['left_chat_member']
    except KeyError:
        pass
    else:
        return 'Left group'

    try:
        data['channel_post']
    except KeyError:
        pass
    else:
        return 'Channel post'

    try:
        data['edited_channel_post']
    except KeyError:
        pass
    else:
        return 'Channel post'

    resp = mduktp(data)
    return resp
