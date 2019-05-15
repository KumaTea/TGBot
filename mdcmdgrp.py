from dataio import getchatid, getmsg, sendmsg, getmsgid
import json


def mdcmdgrp(data):
    chatid = getchatid(data)
    command = getmsg(data)
    msgid = getmsgid(data)

    if command.startswith('/rp') or command.startswith('/repeat'):
        cont = command.find(' ')
        rptext = command[cont:]
        if cont == -1:
            resp = sendmsg(chatid, command, msgid)
            return resp
        else:
            resp = sendmsg(chatid, rptext, msgid)
            return resp

    elif command.startswith('/debug'):
        debugmsg = json.dumps(data)
        resp = sendmsg(345060487, debugmsg)
        return resp

    else:
        return 'Pass in group'
