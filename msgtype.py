from dataio import getchatid
from mdgroup import grpnewmem, grptext, grpfile, grpphoto, grpsticker, grpvideo
from mdpriv import privtext, privfile, privphoto, privsticker, privvideo
from mduktp import mduktp


def msgtype(data):
    chatid = getchatid(data)
    if chatid < 0:
        try:
            data['message']['new_chat_member']
        except KeyError:
            pass
        else:
            resp = grpnewmem(data)
            return resp
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

        try:
            data['message']['text']
        except KeyError:
            pass
        else:
            resp = grptext(data)
            return resp
        try:
            data['message']['sticker']
        except KeyError:
            pass
        else:
            resp = grpsticker(data)
            return resp
        try:
            data['message']['photo']
        except KeyError:
            pass
        else:
            resp = grpphoto(data)
            return resp
        try:
            data['message']['video']
        except KeyError:
            pass
        else:
            resp = grpvideo(data)
            return resp
        try:
            data['message']['document']
        except KeyError:
            pass
        else:
            resp = grpfile(data)
            return resp

        try:
            data['message']['left_chat_member']
        except KeyError:
            pass
        else:
            return 'Left group'

        return 'Unknown group reply'

    else:
        try:
            data['message']['text']
        except KeyError:
            pass
        else:
            resp = privtext(data)
            return resp
        try:
            data['message']['sticker']
        except KeyError:
            pass
        else:
            resp = privsticker(data)
            return resp
        try:
            data['message']['photo']
        except KeyError:
            pass
        else:
            resp = privphoto(data)
            return resp
        try:
            data['message']['video']
        except KeyError:
            pass
        else:
            resp = privvideo(data)
            return resp
        try:
            data['message']['document']
        except KeyError:
            pass
        else:
            resp = privfile(data)
            return resp

        resp = mduktp(data)
        return resp
