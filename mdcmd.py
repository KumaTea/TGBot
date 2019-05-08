from dataio import getchatid, getmsg, sendmsg, ifexists
import json


def dealcmd(data):
    chatid = getchatid(data)
    command = getmsg(data)

    if command.startswith('/start'):
        hellomsg = 'Thank you for using Kumatea bot!\nYou may see commands sending \"/help\".'
        resp = sendmsg(chatid, hellomsg)
        return resp

    elif command.startswith('/help'):
        helpmsg = '/start: wake me up\n/help: display this message\n/fw: forward messages to @kumatea\n' \
                  '/rp: repeat messages\n\nI am in my 1.0.2.8 version.'
        ingrp = 'Hey! I can\'t display help info in group!'
        if chatid < 0:
            resp = sendmsg(chatid, ingrp)
            return resp
        else:
            resp = sendmsg(chatid, helpmsg)
            return resp

    elif command.startswith('/fw') or command.startswith('/forward'):
        cont = command.find(' ')
        lstnm = ifexists(data['message']['from']['last_name'], KeyError, ' ')
        usrnm = ifexists(data['message']['from']['username'], KeyError, 'NoUsername')
        fwmsg = data['message']['from']['first_name'] + ' ' + lstnm + ' (@' + usrnm + ')\n\n' + command[cont:]
        okmsg = 'Message successfully sent.'
        errmsg = 'You haven\'t type in your message!'
        if cont == -1:
            resp = sendmsg(chatid, errmsg)
            return resp
        else:
            sendmsg(345060487, fwmsg)
            resp = sendmsg(chatid, okmsg)
            return resp

    elif command.startswith('/rp') or command.startswith('/repeat'):
        cont = command.find(' ')
        rptext = command[cont:]
        if cont == -1:
            resp = sendmsg(chatid, command)
            return resp
        else:
            resp = sendmsg(chatid, rptext)
            return resp

    elif command.startswith('/debug'):
        debugmsg = json.dumps(data)
        resp = sendmsg(345060487, debugmsg)
        return resp

    elif command.startswith('/stop') or command.startswith('/terminate'):
        if chatid == 345060487:
            return 'Exiting'
        else:
            if chatid < 0:
                return 'Deny in group'
            else:
                denytext = 'You are not administrator and can\'t terminate me yet. However, you may use /fw to report problems and bugs to administrators.'
                resp = sendmsg(chatid, denytext)
                return resp

    else:
        if chatid < 0:
            return 'Pass in group'
        else:
            ukmsg = 'I can\'t understand your command. You may check the /help list.'
            resp = sendmsg(chatid, ukmsg)
            return resp
