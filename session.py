import configparser
from pyrogram import Client
# from multiprocessing import shared_memory
# from apscheduler.schedulers.background import BackgroundScheduler


config = configparser.ConfigParser()
config.read('config.ini')
kuma = Client(
    'kuma',
    api_id=config['kuma']['api_id'],
    api_hash=config['kuma']['api_hash'],
    bot_token=config['kuma']['bot_token'],
)

# scheduler = BackgroundScheduler(misfire_grace_time=60, timezone='Asia/Shanghai')

# try:
#     idle_mark = shared_memory.SharedMemory(name='tg_idle', create=True, size=1)
# except FileExistsError:
#     idle_mark = shared_memory.SharedMemory(name='tg_idle', create=False)
