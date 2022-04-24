import shutil
import logging
from data import db_dir
from tools import mkdir, init_db
from session import scheduler, idle_mark
from register import register_handlers, manager


def starting():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    register_handlers()
    manager()
    scheduler.start()

    try:
        shutil.rmtree('/tmp/screenshots')
    except FileNotFoundError:
        pass
    mkdir([db_dir, '/tmp/screenshots'])
    init_db('NGA')

    # idle_mark.buf[0] = 1

    return logging.info("[TGBot] Initialized.")
