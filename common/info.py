import os


self_id = 781791363
creator = 5273618487
administrators = [345060487, creator]
version = '7.0.4.105'
username = 'KumaTea_bot'
self_name = 'KumaTea Bot'

if os.name == 'nt':
    debug_mode = True
    channel = 'local'
else:
    debug_mode = False
    channel = 'cloud'
