import os


firefox_profile_path = '/home/kuma/data/firefox'

notify_path = '/usr/local/bin/notify'

url_regex = r'https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|' \
            r'www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|' \
            r'https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|' \
            r'www\.[a-zA-Z0-9]+\.[^\s]{2,}'
nga_domains = ['nga.178.com', 'bbs.nga.cn', 'ngabbs.com']
weibo_domains = ['weibo.com', 'www.weibo.com', 'm.weibo.com',
                 'weibo.cn', 'www.weibo.cn', 'm.weibo.cn']

url_blacklist = [
    'nuke', 'setting', 'message', 'compose',
    'login', 'logout', 'sign', 'register'
]


loading_image = [
    'AgACAgQAAxkBAAIT_WHZvQrZzjlaEnD7HEafsgG2tPIKAAIFrTEb3yr8UUL62Xa-3X4dAQADAgADeAADIwQ',
    'AgACAgQAAxkBAAIT_mHZvQocFBcqgYAy3XwaKzos3mKgAAImrTEb9_z9Uf_XxrMyS3TKAQADAgADeAADIwQ',
    'AgACAgQAAxkBAAIT_2HZvQrTD0v74K_-jnUp1GXcPujZAAJXrDEbenoFUmIFYOu5h5QUAQADAgADeAADIwQ',
    'AgACAgQAAxkBAAIUAAFh2b0Kq_Ttt8_vATJe84A12Raf5QACEK0xG_sH_VFf2hBZgR4G7QEAAwIAA3gAAyME',
    'AgACAgQAAxkBAAIUAWHZvQo3SxlcxWgxwbVoIFjXUqGGAAIDrTEbQmX9UfL0xbTPuqvTAQADAgADeAADIwQ',
    'AgACAgQAAxkBAAIUAmHZvQrX09Vg2OE9x9nTWQ0N6QdaAAIFrTEbdjv8USf0nvVXeerxAQADAgADeAADIwQ',
    'AgACAgQAAxkBAAIUA2HZvQob6DrHnPWEBO9jjBjySyU8AALSrDEb1j_9UZfBrz-baZVGAQADAgADeAADIwQ',
    'AgACAgQAAxkBAAIUBGHZvQr2vS08lALKHpA2Tcr4NfOaAAL-rDEbuwX8UbD2Y5U7YAaIAQADAgADeAADIwQ'
]


if os.path.isdir('/home/kuma'):
    db_dir = '/home/kuma/data/db'
else:
    db_dir = 'data'
