# Means unknown type
import json
from dataio import getchatid, sendmsg


def mduktp(data):
    chatid = getchatid(data)
    rectext = 'I don\'t know what I\'ve received!'
    sendmsg(chatid, rectext)
    lstnm = data['message']['from'].get('last_name', '')
    usrnm = data['message']['from'].get('username', 'NoUsername')
    uktpmsg = 'Unknown message received.\n' + data['message']['from']['first_name'] + ' ' + lstnm + ' (@' + usrnm + \
              ')\n\n' + json.dumps(data)
    resp = sendmsg(345060487, uktpmsg)
    return resp
