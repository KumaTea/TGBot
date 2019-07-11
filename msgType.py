from dataIO import get_chat_id
from mdGroup import group_new_member, group_text, group_file, group_photo, group_sticker, group_video, group_gif
from mdPriv import priv_text, priv_file, priv_photo, priv_sticker, priv_video, priv_gif
from mdUnknown import md_unknown


def msg_type(data):
    chatid = get_chat_id(data)
    if chatid < 0:
        if 'message' in data:
            if 'new_chat_member' in data['message']:
                resp = group_new_member(data)
            elif 'text' in data['message']:
                resp = group_text(data)
            elif 'sticker' in data['message']:
                resp = group_sticker(data)
            elif 'photo' in data['message']:
                resp = group_photo(data)
            elif 'video' in data['message']:
                resp = group_video(data)
            elif 'animation' in data['message']:
                resp = group_gif(data)
            elif 'document' in data['message']:
                resp = group_file(data)
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

    elif chatid == 0:
        return 'Can\'t get chatid.'

    else:
        if 'message' in data:
            if 'text' in data['message']:
                resp = priv_text(data)
            elif 'sticker' in data['message']:
                resp = priv_sticker(data)
            elif 'photo' in data['message']:
                resp = priv_photo(data)
            elif 'video' in data['message']:
                resp = priv_video(data)
            elif 'animation' in data['message']:
                resp = priv_gif(data)
            elif 'document' in data['message']:
                resp = priv_file(data)
            elif 'sticker' in data['message']:
                resp = priv_sticker(data)
            else:
                resp = 'Unknown message.'
            return resp
        elif 'edited_message' in data:
            return 'ignore edited message.'

        resp = md_unknown(data)
        return resp
