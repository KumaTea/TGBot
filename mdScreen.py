import logging
from time import time
from io import BytesIO
from botSessionWeb import get_driver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait


def load_complete(driver):
    return driver.execute_script("return document.readyState") == "complete"


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
        WebDriverWait(driver, timeout).until(load_complete)
        # lambda drv: drv.execute_script("return document.readyState") == "complete"
        logging.info("{:.3f}s: Loaded.".format(time() - t0))
        driver.execute_script("window.scrollTo(0, 0);")  # scroll to top
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
