from mdgroup import newmem
from mdtext import dealtext
from mdphoto import dealphoto
from mdvideo import dealvideo
from mdsticker import dealsticker
from mddoc import dealdoc
from mduktp import dealuktp


def dealtype(data):
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
        resp = dealtext(data)
        return resp

    try:
        data['message']['sticker']
    except KeyError:
        pass
    else:
        resp = dealsticker(data)
        return resp

    try:
        data['message']['photo']
    except KeyError:
        pass
    else:
        resp = dealphoto(data)
        return resp

    try:
        data['message']['video']
    except KeyError:
        pass
    else:
        resp = dealvideo(data)
        return resp

    try:
        data['message']['document']
    except KeyError:
        pass
    else:
        resp = dealdoc(data)
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

    resp = dealuktp(data)
    return resp