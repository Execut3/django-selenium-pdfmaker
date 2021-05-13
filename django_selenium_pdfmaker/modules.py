import base64
import json
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def send_devtools(driver, cmd, params=None):
    if params is None:
        params = {}
    resource = f"/session/{driver.session_id}/chromium/send_command_and_get_result"
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    if response.get('status'):
        raise Exception(response.get('value'))
    return response.get('value')


# CHROMIUM_DRIVER_PATH = os.path.join(BASE_DIR, 'assessment', 'html2pdf', 'chromedriver')
CHROMIUM_DRIVER_PATH = 'chromedriver'


def get_pdf_from_html(path, chromedriver=CHROMIUM_DRIVER_PATH, print_options=None, host='127.0.0.1:8000'):
    if print_options is None:
        print_options = {}

    webdriver_options = Options()
    webdriver_options.add_argument('--headless')
    webdriver_options.add_argument('--disable-gpu')
    webdriver_options.add_argument("--remote-debugging-port=9222")
    path = f'{host}{path}'
    driver = webdriver.Chrome(chromedriver, options=webdriver_options)
    driver.get(path)
    driver.set_window_size(1100, 1200)
    time.sleep(3)

    calculated_print_options = {
        'landscape': False,
        'displayHeaderFooter': False,
        'printBackground': True,
        'preferCSSPageSize': True,
    }
    calculated_print_options.update(print_options)
    result = send_devtools(driver, "Page.printToPDF", calculated_print_options)
    driver.quit()
    return base64.b64decode(result['data'])
