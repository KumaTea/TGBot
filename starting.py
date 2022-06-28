import os
import time
import logging
from bot_db import *
from session import kuma
from register import register_handlers


def starting():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    # manager()
    # scheduler.start()

    # try:
    #     shutil.rmtree('/tmp/screenshots')
    # except FileNotFoundError:
    #     pass
    os.makedirs(f'{pwd}/tmp', exist_ok=True)
    # init_db('NGA')

    # idle_mark.buf[0] = 1

    if os.path.isfile(restart_mark):
        timestamp = time.time()
        wait_time = 4  # run 'sleep 2' twice
        restarted_time = os.path.getmtime(restart_mark)
        time_cost = timestamp - restarted_time - wait_time
        with open(restart_mark, 'r') as f:
            restart_by = int(f.read())
        with kuma:
            kuma.send_message(
                restart_by,
                f'Bot has been restarted!\nTime cost: {time_cost:.3f}s'
            )
        os.remove(restart_mark)

    register_handlers()

    return logging.info("[TGBot] Initialized.")
