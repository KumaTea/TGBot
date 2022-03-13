import logging
from botDB import db_dir
from botSession import scheduler
from botTools import mkdir, init_db
from register import register_handlers, manager


def starting():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    register_handlers()
    manager()
    scheduler.start()

    mkdir(db_dir)
    init_db('NGA')

    logging.info('Starting fine.')
