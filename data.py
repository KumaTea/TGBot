import os


chrome_profile_path = '/home/kuma/data/chrome'
chrome_driver_path = '/snap/bin/chromedriver'

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
    'AgACAgQAAxkBAAIWeWJlA76sVbamSH0npmT600zGxapoAAIFrTEb3yr8UUL62Xa-3X4dAAgBAAMCAAN4AAceBA',
    'AgACAgQAAxkBAAIWe2JlA76k-FX9fbKSQOQ56Cz1r9R0AAJXrDEbenoFUmIFYOu5h5QUAAgBAAMCAAN4AAceBA',
    'AgACAgQAAxkBAAIWfmJlA74E8kMqEbSx63FCIRCrbtgLAAIFrTEbdjv8USf0nvVXeerxAAgBAAMCAAN4AAceBA',
    'AgACAgQAAxkBAAIWf2JlA77YW5fPLWmq91iP_j9BRWM6AALSrDEb1j_9UZfBrz-baZVGAAgBAAMCAAN4AAceBA',
    'AgACAgQAAxkBAAIWfGJlA75-ZfGaLGrEZRbeEH4i7usMAAIQrTEb-wf9UV_aEFmBHgbtAAgBAAMCAAN4AAceBA',
    'AgACAgQAAxkBAAIWgGJlA76mv4Kzn47Zs33-q90FEGFBAAL-rDEbuwX8UbD2Y5U7YAaIAAgBAAMCAAN4AAceBA',
    'AgACAgQAAxkBAAIWfWJlA77UcSK7LvGUGwcQ0dnIHMx9AAIDrTEbQmX9UfL0xbTPuqvTAAgBAAMCAAN4AAceBA',
    'AgACAgQAAxkBAAIWemJlA77QvRGWBBdk6eZ8-A5VBnaRAAImrTEb9_z9Uf_XxrMyS3TKAAgBAAMCAAN4AAceBA',
]


if os.path.isdir('/home/kuma'):
    db_dir = '/home/kuma/data/db'
else:
    db_dir = 'data'
