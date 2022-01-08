import logging
from botSession import scheduler
from register import register_handlers, manager


def starting():
    register_handlers()
    manager()
    scheduler.start()
    logging.warning('Starting fine.')
