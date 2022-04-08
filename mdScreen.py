import logging
from time import time
from io import BytesIO
from botSession import kuma
from botSessionWeb import get_driver
from multiprocessing import Process
from telegram import InputMediaPhoto
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait


def load_complete(driver):
    return driver.execute_script("return document.readyState") == "complete"


def load_tweet_complete(driver):
    return 'data-testid="tweet"' in driver.page_source


def get_screenshot(url, timeout=30):
    t0 = time()
    try:
        logging.info("{:.3f}s: Task: {}".format(time() - t0, url))
        driver = get_driver()
        logging.info("{:.3f}s: Got: driver".format(time() - t0))
        driver.get(url)
        logging.info("{:.3f}s: Got: {}".format(time()-t0, url))
        if 'nga' in url:
            images = driver.find_elements_by_xpath('//button[normalize-space()="显示图片"]')
            for image in images:
                try:
                    image.click()
                except:
                    logging.warning('An image failed to display.')
        if 'twitter' in url:
            WebDriverWait(driver, timeout).until(load_tweet_complete)
        else:
            WebDriverWait(driver, timeout).until(load_complete)
            # lambda drv: drv.execute_script("return document.readyState") == "complete"
            driver.execute_script("window.scrollTo(0, 0);")  # scroll to top

        logging.info("{:.3f}s: Loaded.".format(time() - t0))
        screenshot = driver.get_screenshot_as_png()
        logging.info("{:.3f}s: Got: screenshot".format(time() - t0))
        driver.quit()
        logging.info("{:.3f}s: Quit".format(time() - t0))
        return BytesIO(screenshot)
    except TimeoutException as e:
        if 'driver' in locals():
            driver.quit()  # noqa
        logging.error(f'Timeout: {str(e)}')
        return f'Timeout: {str(e)}'
    except Exception as e:
        if 'driver' in locals():
            driver.quit()  # noqa
        logging.error(f'Error: {str(e)}')
        return f'Error: {str(e)}'


def update_inform(chat_id, inform_id, url, error_msg='Error!', parse_mode='Markdown'):
    screenshot = get_screenshot(url)
    if screenshot and type(screenshot) != str:
        return kuma.edit_message_media(chat_id, inform_id, media=InputMediaPhoto(screenshot))
    return kuma.edit_message_caption(
        chat_id, inform_id, caption=error_msg, parse_mode=parse_mode)


def screenshot_mp(chat_id, inform_id, url, error_msg='Error!', parse_mode='Markdown'):
    p = Process(target=update_inform, args=(chat_id, inform_id, url, error_msg, parse_mode))
    p.start()
