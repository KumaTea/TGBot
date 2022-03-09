from queue import Queue
from telegram import Bot
from botInfo import self_id
from botTools import query_token
from telegram.ext import Dispatcher
from apscheduler.schedulers.background import BackgroundScheduler


kuma = Bot(query_token(self_id))
update_queue = Queue()
dp = Dispatcher(kuma, update_queue, use_context=True)

scheduler = BackgroundScheduler(misfire_grace_time=60, timezone='Asia/Shanghai')
