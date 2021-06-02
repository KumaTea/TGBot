from botSession import dp
from mdNewMember import welcome
from mdFunctions import *
from telegram.ext import MessageHandler, CommandHandler, Filters


def register_handlers():
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    dp.add_handler(CommandHandler(['debug', 'dump'], debug))
    dp.add_handler(CommandHandler(['delay', 'ping'], delay))
    dp.add_handler(CommandHandler(['rp', 'repeat'], repeat, Filters.chat_type.groups))
    dp.add_handler(CommandHandler(['title', 'entitle'], title, Filters.chat_type.groups))

    dp.add_handler(CommandHandler('start', private_start, Filters.chat_type.private))
    dp.add_handler(CommandHandler(['fw', 'forward'], private_forward, Filters.chat_type.private))
    dp.add_handler(CommandHandler('help', private_help, Filters.chat_type.private))

    dp.add_handler(MessageHandler((Filters.command & Filters.chat_type.private), private_unknown))

    dp.add_handler(MessageHandler(Filters.chat_type.private, private_get_file_id))
    return True
