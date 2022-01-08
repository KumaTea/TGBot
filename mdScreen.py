import logging
from io import BytesIO
from time import sleep
from botSessionWeb import get_driver


def get_screenshot(url, delay=1):
    try:
        logging.debug("Getting: %s" % url)
        driver = get_driver()
        driver.get(url)
        if 'nga' in url:
            images = driver.find_elements_by_xpath('//button[normalize-space()="显示图片"]')
            for image in images:
                try:
                    image.click()
                except:
                    logging.warning('An image failed to display.')
        sleep(delay)
        driver.execute_script("window.scrollTo(0, 0);")  # scroll to top
        screenshot = driver.get_screenshot_as_png()
        driver.quit()
        return BytesIO(screenshot)
    except Exception as e:
        logging.error(f'Error: {str(e)}')
        return None
