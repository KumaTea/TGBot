import time
import logging
from bot_db import *
from session import kuma
from mod_poll import read_poll_groups
from register import register_handlers


def starting():
    os.makedirs(f'{pwd}/tmp', exist_ok=True)
    os.makedirs(f'{pwd}/data/poll', exist_ok=True)

    read_poll_groups()

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

    register_handlers()

    return logging.info("[TGBot] Initialized.")
