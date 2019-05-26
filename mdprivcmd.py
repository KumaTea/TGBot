from dataio import getchatid, getmsg, sendmsg
from mddebug import mddebug
import botinfo
from starting import getadminid
from mdfunc import randomjoke


def mdprivcmd(data):
    chatid = getchatid(data)
    command = getmsg(data)

    if command.startswith('/start'):
        hellomsg = 'Thank you for using Kumatea bot!\nYou may see commands sending \"/help\".'
        resp = sendmsg(chatid, hellomsg)
        return resp

    elif command.startswith('/help'):
        helpmsg = '{}\n\nI\'am in my {} ({}) version.'.format(botinfo.cmds, botinfo.version, botinfo.channel)
        resp = sendmsg(chatid, helpmsg)
        return resp

    elif command.startswith(('/fw', '/forward')):
        cont = command.find(' ')
        lstnm = data['message']['from'].get('last_name', '')
        usrnm = data['message']['from'].get('username', 'No username')
        fwmsg = data['message']['from']['first_name'] + ' ' + lstnm + ' (@' + usrnm + ')\n\n' + command[cont:]
        okmsg = 'Message successfully sent.'
        errmsg = 'You haven\'t type in your message!'
        if cont == -1:
            resp = sendmsg(chatid, errmsg)
            return resp
        else:
            adminid = getadminid()
            sendmsg(adminid[0], fwmsg)
            resp = sendmsg(chatid, okmsg)
            return resp

    elif command.startswith(('/rp', '/repeat')):
        cont = command.find(' ')
        rptext = command[cont:]
        if cont == -1:
            resp = sendmsg(chatid, command)
            return resp
        else:
            resp = sendmsg(chatid, rptext)
            return resp

    elif command.startswith(('/joke', '/soviet')):
        joke = randomjoke()
        resp = sendmsg(chatid, joke)
        return resp

    elif command.startswith('/del'):
        helpmsg = 'This command is not available in private chats. Try it in groups!'
        resp = sendmsg(chatid, helpmsg)
        return resp

    elif command.startswith('/debug'):
        cont = command.find(' ')
        if cont == -1:
            resp = mddebug(data)
        else:
            resp = mddebug(data, True)
        return resp

    else:
        ukmsg = 'I can\'t understand your command. You may check the /help list.'
        resp = sendmsg(chatid, ukmsg)
        return resp

    """
        elif command.startswith('/stop') or command.startswith('/terminate'):
        adminid = getadminid()
        if chatid == adminid:
            mdexit()
            return 'Exiting'
        else:
            if chatid < 0:
                return 'Deny in group'
            else:
                denytext = 'You are not administrator and can\'t terminate me yet. However, you may use /fw to report problems and bugs to administrators.'
                resp = sendmsg(chatid, denytext)
                return resp
    """
