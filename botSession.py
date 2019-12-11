from telegram import Bot
from telegram.ext import Dispatcher
from botInfo import self_id
from botTools import query_token
from queue import Queue


kuma = Bot(query_token(self_id))
update_queue = Queue()
dp = Dispatcher(kuma, update_queue, use_context=True)
