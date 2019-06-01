from dataio import getchatid
from mdgroup import grpnewmem, grptext, grpfile, grpphoto, grpsticker, grpvideo, grpgif
from mdpriv import privtext, privfile, privphoto, privsticker, privvideo, privgif
from mduktp import mduktp


def msgtype(data):
    chatid = getchatid(data)
    if chatid < 0:
        if 'message' in data:
            if 'new_chat_member' in data['message']:
                resp = grpnewmem(data)
            elif 'text' in data['message']:
                resp = grptext(data)
            elif 'sticker' in data['message']:
                resp = grpsticker(data)
            elif 'photo' in data['message']:
                resp = grpphoto(data)
            elif 'video' in data['message']:
                resp = grpvideo(data)
            elif 'animation' in data['message']:
                resp = grpgif(data)
            elif 'document' in data['message']:
                resp = grpfile(data)
            elif 'edited_message' in data:
                resp = 'ignore edited message.'
            else:
                resp = 'Unknown message.'
            return resp
        elif 'channel_post' or 'edited_channel_post' in data:
            return 'Channel post'
        elif 'left_chat_member' in data:
            return 'Left group'

        return 'Unknown group reply'

    else:
        if 'message' in data:
            if 'text' in data['message']:
                resp = privtext(data)
            elif 'sticker' in data['message']:
                resp = privsticker(data)
            elif 'photo' in data['message']:
                resp = privphoto(data)
            elif 'video' in data['message']:
                resp = privvideo(data)
            elif 'animation' in data['message']:
                resp = privgif(data)
            elif 'document' in data['message']:
                resp = privfile(data)
            elif 'sticker' in data['message']:
                resp = privsticker(data)
            else:
                resp = 'Unknown message.'
            return resp
        elif 'edited_message' in data:
            return 'ignore edited message.'

        resp = mduktp(data)
        return resp
