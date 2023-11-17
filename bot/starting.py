import time
import logging
from common.data import *
from bot.session import kuma
from handlers.register import register_handlers
from bot.tools import set_bot_info


def report_restart():
    # yes, sync
    if os.path.isfile(restart_mark):
        timestamp = time.time()
        restarted_time = os.path.getmtime(restart_mark)
        time_cost = timestamp - restarted_time
        with open(restart_mark, 'r') as f:
            restart_by = int(f.read())
        with kuma:
            kuma.send_message(
                restart_by,
                f'Bot has been restarted!\n'
                f'Time cost: {time_cost:.3f}s'
            )
        os.remove(restart_mark)


def set_debug_tag():
    if debug_mode:
        set_bot_info(client=kuma, name='KumaBot (Debug)')
    else:
        set_bot_info(client=kuma, name=self_name)


def starting():
    os.makedirs(f'{pwd}/tmp', exist_ok=True)
    os.makedirs(f'{pwd}/data/poll', exist_ok=True)

    report_restart()
    set_debug_tag()

    register_handlers()

    return logging.info("[TGBot] Initialized.")
