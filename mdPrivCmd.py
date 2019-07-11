from dataIO import get_chat_id, get_msg, send_msg
from mdDebug import md_debug
import botInfo
from starting import getadminid
from mdFunc import random_joke, sysu_joke


def md_priv_cmd(data):
    chatid = get_chat_id(data)
    command = get_msg(data)

    if command.startswith('/start'):
        hellomsg = 'Thank you for using Kumatea bot!\nYou may see commands sending \"/help\".'
        resp = send_msg(chatid, hellomsg)
        return resp

    elif command.startswith('/help'):
        helpmsg = '{}\n\nI\'am in my {} ({}) version.'.format(botInfo.help_msg, botInfo.version, botInfo.channel)
        resp = send_msg(chatid, helpmsg)
        return resp

    elif command.startswith(('/fw', '/forward')):
        cont = command.find(' ')
        lstnm = data['message']['from'].get('last_name', '')
        usrnm = data['message']['from'].get('username', 'No username')
        fwmsg = data['message']['from']['first_name'] + ' ' + lstnm + ' (@' + usrnm + ')\n\n' + command[cont:]
        okmsg = 'Message successfully sent.'
        errmsg = 'You haven\'t type in your message!'
        if cont == -1:
            resp = send_msg(chatid, errmsg)
            return resp
        else:
            adminid = getadminid()
            send_msg(adminid[0], fwmsg)
            resp = send_msg(chatid, okmsg)
            return resp

    elif command.startswith(('/rp', '/repeat')):
        cont = command.find(' ')
        rptext = command[cont:]
        if cont == -1:
            resp = send_msg(chatid, command)
            return resp
        else:
            resp = send_msg(chatid, rptext)
            return resp

    elif command.startswith(('/joke', '/soviet')):
        joke = random_joke()
        resp = send_msg(chatid, joke)
        return resp

    elif command.startswith(('/sysu', '/中', '/双鸭山')):
        joke = sysu_joke()
        resp = send_msg(chatid, joke)
        return resp

    elif command.startswith('/del'):
        helpmsg = 'This command is not available in private chats. Try it in groups!'
        resp = send_msg(chatid, helpmsg)
        return resp

    elif command.startswith('/debug'):
        cont = command.find(' ')
        if cont == -1:
            resp = md_debug(data)
        else:
            resp = md_debug(data, True)
        return resp

    else:
        ukmsg = 'I can\'t understand your command. You may check the /help list.'
        resp = send_msg(chatid, ukmsg)
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
