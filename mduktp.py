# Means unknown type
import json
from dataio import getchatid, sendmsg


def mduktp(data):
    chatid = getchatid(data)
    rectext = 'I don\'t know what I\'ve received!'
    sendmsg(chatid, rectext)
    uktpmsg = 'Unknown message received.\n' + json.dumps(data)
    resp = sendmsg(345060487, uktpmsg)
    return resp
