import os
import time
import logging
from session import kuma
from bot_db import restart_mark
from register import register_handlers


def starting():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    register_handlers()
    # manager()
    # scheduler.start()

    # try:
    #     shutil.rmtree('/tmp/screenshots')
    # except FileNotFoundError:
    #     pass
    # os.makedirs(db_dir, exist_ok=True)
    # init_db('NGA')

    # idle_mark.buf[0] = 1

    if os.path.isfile(restart_mark):
        timestamp = time.time()
        wait_time = 4  # run 'sleep 2' twice
        restarted_time = os.path.getmtime(restart_mark)
        time_cost = timestamp - restarted_time - wait_time
        with open(restart_mark, 'r') as f:
            restart_by = int(f.read())
        kuma.send_message(
            restart_by,
            f'Bot has been restarted!\nTime cost: {time_cost}'
        )
        os.remove(restart_mark)

    return logging.info("[TGBot] Initialized.")
