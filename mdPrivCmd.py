from Tools import md_debug, delay
import botInfo
from starting import get_admin_id
from botSession import bot


def priv_cmd(data):
    bot_getter = bot.get(data)
    chat_id = bot_getter.chat('id')
    command = bot_getter.message('text')[1:]

    if command.startswith('start'):
        hello_msg = 'Thank you for using KumaTea bot!\nYou may see commands sending \"/help\".'
        resp = bot.send(chat_id).message(hello_msg)
        return resp

    elif command.startswith('help'):
        try:
            from tgapi import __version__
            ver = __version__
            ver_info = f'using tgapi v{ver}'
        except ImportError:
            ver_info = 'using a deprecated version of tgapi'
        help_msg = f'{botInfo.help_msg}\n\nI\'m in my {botInfo.version} ({botInfo.channel}) version, {ver_info}.'
        resp = bot.send(chat_id).message(help_msg)
        return resp

    elif command.startswith(('fw', 'forward')):
        cont = command.find(' ')
        lst_nm = data['message']['from'].get('last_name', '')
        usr_nm = data['message']['from'].get('username', 'No username')
        fw_msg = data['message']['from']['first_name'] + ' ' + lst_nm + ' (@' + usr_nm + ')\n\n' + command[cont:]
        ok_msg = 'Message successfully sent.'
        errmsg = 'You haven\'t type in your message!'
        if cont == -1:
            resp = bot.send(chat_id).message(errmsg)
        else:
            admin_id = get_admin_id()
            bot.send(admin_id[0]).message(fw_msg)
            resp = bot.send(chat_id).message(ok_msg)
        return resp

    elif command.startswith('debug'):
        resp = md_debug(chat_id, data)
        return resp

    elif command.startswith(('ping', 'delay')):
        return delay(data)

    else:
        uk_msg = 'I can\'t understand your command. You may check the /help list.'
        resp = bot.send(chat_id).message(uk_msg)
        return resp
