# Means unknown type
import json
from dataIO import get_chat_id, send_msg


def md_unknown(data):
    chatid = get_chat_id(data)
    rectext = 'I don\'t know what I\'ve received!'
    send_msg(chatid, rectext)
    uktpmsg = 'Unknown message received.\n' + json.dumps(data)
    resp = send_msg(345060487, uktpmsg)
    return resp
