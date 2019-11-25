from botSession import bot


def md_debug(chat_id, data):
    debug_msg = str(data)
    resp = bot.send(chat_id).message(f'```{debug_msg}```', parse='Markdown')
    """
    if log:
        sendfile(admin_id[0], 'log/log.csv', False, 'upload')
    if os.name == 'nt':
        scrst = scrshot.grab()
        scrst.save('log/screenshot.png')
        sendphoto(admin_id, 'log/screenshot.png', False, 'upload')
    """
    return resp


def delay(data):
    bot_getter = bot.get(data)
    chat_id = bot_getter.chat('id')
    msg_id = bot_getter.message('id')

    first_timestamp = bot.get(data).message('time')
    if chat_id < 0:
        second = bot.send(chat_id).message('Checking delay...', reply_to=msg_id)
    else:
        second = bot.send(chat_id).message('Checking delay...')
    second_getter = bot.get(second)
    second_timestamp = second_getter.message('time')
    second_msg_id = second_getter.message('id')
    delayed = second_timestamp - first_timestamp
    if delayed == 0:
        status = 'excellent'
    elif delayed == 1:
        status = 'good'
    else:
        status = 'bad'
    result = bot.edit(chat_id, second_msg_id).message(f'Delay is {delayed}s.\nThe connectivity is {status}.')
    return result
