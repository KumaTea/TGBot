from pyrogram import Client
from multiprocessing import shared_memory
from apscheduler.schedulers.background import BackgroundScheduler


kuma = Client('kuma')

scheduler = BackgroundScheduler(misfire_grace_time=60, timezone='Asia/Shanghai')

try:
    idle_mark = shared_memory.SharedMemory(name='tg_idle', create=True, size=1)
except FileExistsError:
    idle_mark = shared_memory.SharedMemory(name='tg_idle', create=False)
