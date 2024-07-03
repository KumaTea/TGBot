from bot.session import kuma
from pyrogram import filters
from handlers.functions import *
from admin.new import new_group_member
from handlers.callbacks import process_callback
from handlers.messages import group_msg, private_msg
from pyrogram.handlers import MessageHandler, CallbackQueryHandler


def register_handlers():
    # group commands
    kuma.add_handler(MessageHandler(repeat, filters.command(['rp', 'repeat', 'say']) & filters.group))
    kuma.add_handler(MessageHandler(title, filters.command(['title', 'entitle']) & filters.group))
    kuma.add_handler(MessageHandler(untitle, filters.command(['untitle', 'detitle']) & filters.group))
    kuma.add_handler(MessageHandler(enable_group, filters.command(['enable_group']) & filters.group))
    kuma.add_handler(MessageHandler(disable_group, filters.command(['disable_group']) & filters.group))
    kuma.add_handler(MessageHandler(apply_add_to_candidates, filters.command(['enroll_poll']) & filters.group))
    kuma.add_handler(MessageHandler(apply_delete_from_candidates, filters.command(['leave_poll']) & filters.group))
    kuma.add_handler(MessageHandler(view_candidates, filters.command(['view_poll']) & filters.group))
    kuma.add_handler(MessageHandler(view_bl, filters.command(['view_bl', 'view_blacklist']) & filters.group))
    kuma.add_handler(MessageHandler(group_help_cmd, filters.command(['help']) & filters.group))

    # private commands
    kuma.add_handler(MessageHandler(private_start, filters.command(['start']) & filters.private))
    kuma.add_handler(MessageHandler(private_forward, filters.command(['fw', 'forward']) & filters.private))
    kuma.add_handler(MessageHandler(private_help, filters.command(['help']) & filters.private))
    kuma.add_handler(MessageHandler(restart, filters.command(['restart', 'reboot']) & filters.private))
    kuma.add_handler(MessageHandler(command_get_users, filters.command(['get_users']) & filters.private))
    kuma.add_handler(MessageHandler(command_get_groups, filters.command(['get_groups']) & filters.private))
    # kuma.add_handler(MessageHandler(command_red_bag, filters.command(['red_bag', 'redbag', 'rb']) & filters.private))

    # universal commands
    kuma.add_handler(MessageHandler(debug, filters.command(['debug', 'dump'])))
    kuma.add_handler(MessageHandler(delay, filters.command(['delay', 'ping'])))
    kuma.add_handler(MessageHandler(mbti,  filters.command(['mbti'])))
    kuma.add_handler(MessageHandler(unparse, filters.command(['unparse'])))
    kuma.add_handler(MessageHandler(get_chat_id, filters.command(['chat_id', 'chatid'])))
    kuma.add_handler(MessageHandler(eval_code, filters.command(['raw', 'exec'])))

    # temporary or experimental

    # private messages
    kuma.add_handler(MessageHandler(private_msg, filters.private))

    # group messages
    kuma.add_handler(MessageHandler(new_group_member, filters.group & filters.new_chat_members))
    kuma.add_handler(MessageHandler(group_msg, filters.group))

    # callbacks
    kuma.add_handler(CallbackQueryHandler(process_callback))

    return logging.info('Registered handlers')


# def manager():
#     scheduler = session.scheduler
#     scheduler.add_job(func, 'cron', [arg1], hour=4)
#     return logging.info('Scheduler started')
