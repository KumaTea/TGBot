import os


start_message = (
    'Thank you for using KumaTea bot!\n'
    'You may see commands sending "/help".'
)
help_message = (
    '/start: wake me up\n'
    '/help: display this message\n'
    '/ping: check for delay\n'
    '/rp: repeat\n'
    '/say: say something\n'
)
unknown_message = "I can't understand your message or command. You may try /help."

self_id = 781791363
creator = 5273618487
administrators = [345060487, creator]
version = '6.0.0.8'
channel = 'local' if os.name == 'nt' else 'cloud'
username = 'KumaTea_bot'
