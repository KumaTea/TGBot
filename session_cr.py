from data import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = webdriver.ChromeOptions()

# options.add_argument('-headless')
options.add_argument('--headless=chrome')
# use --headless=chrome to run headless mode using "actual chrome browser code"
# see https://bugs.chromium.org/p/chromium/issues/detail?id=706008

options.add_argument(f'--user-data-dir={chrome_profile_path}')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')

# iPhone_user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) ' \
#                     'AppleWebKit/605.1.15 (KHTML, like Gecko) ' \
#                     'Version/15.4 Mobile/15E148 Safari/604.1'
# options.add_argument(f'user-agent={iPhone_user_agent}')
options.mobile_options.mobile_emulation = {'deviceName': 'iPhone X'}


def get_driver():
    driver = webdriver.Chrome(
        executable_path=chrome_driver_path,
        chrome_options=options
    )
    return driver
