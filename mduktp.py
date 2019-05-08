# Means unknown type
import json
from dataio import getchatid, sendmsg, ifexists


def dealuktp(data):
    chatid = getchatid(data)
    rectext = 'I don\'t know what I\'ve received!'
    sendmsg(chatid, rectext)
    lstnm = ifexists(data['message']['from']['last_name'], KeyError, ' ')
    usrnm = ifexists(data['message']['from']['username'], KeyError, 'NoUsername')
    uktpmsg = 'Unknown message received.\n' + data['message']['from']['first_name'] + ' ' + lstnm + ' (@' + usrnm + \
              ')\n\n' + json.dumps(data)
    resp = sendmsg(345060487, uktpmsg)
    return resp
