import logging
import session
import session_rq
from functions import *
from pyrogram import filters
from tools import session_update
from process_msg import process_msg
from screen_nga import check_nga_login
from pyrogram.handlers import MessageHandler


def register_handlers():
    # group commands
    kuma.add_handler(MessageHandler(repeat, filters.command(['rp', 'repeat']) & filters.group))  # & ~filters.edited))
    kuma.add_handler(MessageHandler(title, filters.command(['title', 'entitle']) & filters.group))  # & ~filters.edited))

    # private commands
    kuma.add_handler(MessageHandler(private_start, filters.command(['start']) & filters.private))  # & ~filters.edited))
    kuma.add_handler(MessageHandler(private_forward, filters.command(['fw', 'forward']) & filters.private))  # & ~filters.edited))
    kuma.add_handler(MessageHandler(private_help, filters.command(['help']) & filters.private))  # & ~filters.edited))

    # universal commands
    kuma.add_handler(MessageHandler(debug, filters.command(['debug', 'dump'])))  # & ~filters.edited))
    kuma.add_handler(MessageHandler(delay, filters.command(['delay', 'ping'])))  # & ~filters.edited))
    kuma.add_handler(MessageHandler(look, filters.command(['look', 'get', 'screenshot'])))  # & ~filters.edited))

    kuma.add_handler(MessageHandler(private_get_file_id, filters.private))  # & ~filters.edited))

    kuma.add_handler(MessageHandler(process_msg, filters.group))  # & ~filters.edited))
    kuma.add_handler(MessageHandler(private_unknown, filters.private))  # & ~filters.edited))

    return logging.info('Registered handlers')


def manager():
    scheduler = session.scheduler
    scheduler.add_job(session_update, 'cron', [session_rq.nga, session_rq.nga_token], hour=4)
    scheduler.add_job(check_nga_login, 'cron', minute=30)
    return logging.info('Scheduler started')
