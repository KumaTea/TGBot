from bot_db import *
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


options = webdriver.FirefoxOptions()

options.headless = True

# options.add_argument(f'-P kuma')
# options.add_argument(f'--user-data-dir={chrome_profile_path}')
# options.set_preference('profile', firefox_profile_path)
# options.profile = FirefoxProfile('/home/kuma/data/firefox')

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
