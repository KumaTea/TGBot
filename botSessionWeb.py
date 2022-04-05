import json
from botDB import *
from requests import Session
from selenium import webdriver
from botTools import query_token
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


nga = Session()
nga_token = json.loads(query_token('nga'))
headers = nga_token['headers']
cookies = nga_token['cookies']
nga.headers.update(headers)
nga.cookies.update(cookies)


options = webdriver.FirefoxOptions()

options.headless = True
# options.add_argument('-headless')
# options.add_argument('--headless=chrome')
# use --headless=chrome to run headless mode using "actual chrome browser code"
# see https://bugs.chromium.org/p/chromium/issues/detail?id=706008

# options.add_argument(f'-P kuma')
# options.add_argument(f'--user-data-dir={chrome_profile_path}')
# options.set_preference('profile', firefox_profile_path)
# options.profile = FirefoxProfile('/home/kuma/data/firefox')

# options.add_argument('--disable-gpu')
# options.add_argument('--disable-dev-shm-usage')

iPhone_user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) ' \
                    'AppleWebKit/605.1.15 (KHTML, like Gecko) ' \
                    'Version/15.4 Mobile/15E148 Safari/604.1'
options.set_preference("general.useragent.override", iPhone_user_agent)
# options.set_capability("deviceName", "iPhone 12 Mini")
options.set_preference("layout.css.devPixelsPerPx", '2.4')  # 1080 / 450


def get_driver():
    driver = webdriver.Firefox(
        firefox_profile=FirefoxProfile(firefox_profile_path),
        options=options)
    driver.set_window_size(450, 975)
    return driver
