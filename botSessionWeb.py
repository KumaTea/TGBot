import json
from botDB import *
from requests import Session
from selenium import webdriver
from botTools import query_token
from selenium.webdriver.chrome.service import Service


nga = Session()
nga_token = json.loads(query_token('nga'))
headers = nga_token['headers']
cookies = nga_token['cookies']
nga.headers.update(headers)
nga.cookies.update(cookies)


options = webdriver.ChromeOptions()

# options.add_argument('--headless')
options.add_argument('--headless=chrome')
# use --headless=chrome to run headless mode using "actual chrome browser code"
# see https://bugs.chromium.org/p/chromium/issues/detail?id=706008

options.add_argument(f'--user-data-dir={chrome_profile_path}')
# options.add_argument('--disable-gpu')
# options.add_argument('--disable-dev-shm-usage')

mobile_emulation = {'deviceName': 'iPhone X'}
options.add_experimental_option('mobileEmulation', mobile_emulation)

preferences = {'download_restrictions': 3}
# disable all downloads: https://chromeenterprise.google/policies/?policy=DownloadRestrictions
options.add_experimental_option('prefs', preferences)


def get_driver():
    return webdriver.Chrome(service=Service(chromedriver_path), options=options)
