import logging
import configparser
from pyrogram import Client


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

config = configparser.ConfigParser()
config.read('config.ini')
kuma = Client(
    'kuma',
    api_id=config['kuma']['api_id'],
    api_hash=config['kuma']['api_hash'],
    bot_token=config['kuma']['bot_token'],
    workdir='.'
)
