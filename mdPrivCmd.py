from mdDebug import md_debug
import botInfo
from starting import getadminid
from botSession import bot


def priv_cmd(data):
    chatid = bot.get(data).chat('id')
    command = bot.get(data).message('text')[1:]

    if command.startswith('start'):
        hellomsg = 'Thank you for using KumaTea bot!\nYou may see commands sending \"/help\".'
        resp = bot.send(chatid).message(hellomsg)
        return resp

    elif command.startswith('help'):
        try:
            from tgapi import __version__
            ver = __version__
            ver_info = f'using tgapi v{ver}'
        except ImportError:
            ver_info = 'using a deprecated version of tgapi'
        help_msg = f'{botInfo.help_msg}\n\nI\'m in my {botInfo.version} ({botInfo.channel}) version, {ver_info}.'
        resp = bot.send(chatid).message(help_msg)
        return resp

    elif command.startswith(('fw', 'forward')):
        cont = command.find(' ')
        lstnm = data['message']['from'].get('last_name', '')
        usrnm = data['message']['from'].get('username', 'No username')
        fwmsg = data['message']['from']['first_name'] + ' ' + lstnm + ' (@' + usrnm + ')\n\n' + command[cont:]
        okmsg = 'Message successfully sent.'
        errmsg = 'You haven\'t type in your message!'
        if cont == -1:
            resp = bot.send(chatid).message(errmsg)
        else:
            adminid = getadminid()
            bot.send(adminid[0]).message(fwmsg)
            resp = bot.send(chatid).message(okmsg)
        return resp

    elif command.startswith(('rp', 'repeat')):
        cont = command.find(' ')
        rptext = command[cont:]
        if cont == -1:
            resp = bot.send(chatid).message(command)
        else:
            resp = bot.send(chatid).message(rptext)
        return resp

    elif command.startswith('debug'):
        resp = md_debug(data)
        return resp

    else:
        ukmsg = 'I can\'t understand your command. You may check the /help list.'
        resp = bot.send(chatid).message(ukmsg)
        return resp
