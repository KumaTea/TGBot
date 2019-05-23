from dataio import getchatid
from mdgroup import grpnewmem, grptext, grpfile, grpphoto, grpsticker, grpvideo
from mdpriv import privtext, privfile, privphoto, privsticker, privvideo
from mduktp import mduktp


def msgtype(data):
    chatid = getchatid(data)
    if chatid < 0:
        if 'message' in data:
            if 'new_chat_member' in data['message']:
                resp = grpnewmem(data)
                return resp
            elif 'text' in data['message']:
                resp = grptext(data)
                return resp
            elif 'sticker' in data['message']:
                resp = grpsticker(data)
                return resp
            elif 'photo' in data['message']:
                resp = grpphoto(data)
                return resp
            elif 'video' in data['message']:
                resp = grpvideo(data)
                return resp
            elif 'document' in data['message']:
                resp = grpfile(data)
                return resp
        elif 'channel_post' or 'edited_channel_post' in data:
            return 'Channel post'
        elif 'left_chat_member' in data:
            return 'Left group'

        return 'Unknown group reply'

    else:
        if 'text' in data['message']:
            resp = privtext(data)
            return resp
        elif 'sticker' in data['message']:
            resp = privsticker(data)
            return resp
        elif 'photo' in data['message']:
            resp = privphoto(data)
            return resp
        elif 'video' in data['message']:
            resp = privvideo(data)
            return resp
        elif 'document' in data['message']:
            resp = privfile(data)
            return resp
        elif 'sticker' in data['message']:
            resp = privsticker(data)
            return resp

        resp = mduktp(data)
        return resp
